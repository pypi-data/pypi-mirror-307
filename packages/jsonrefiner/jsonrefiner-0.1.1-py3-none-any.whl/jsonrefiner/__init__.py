from dataclasses import dataclass
from typing import List, Union, Optional, Callable, Any
from functools import reduce
from hashlib import sha256

def OptionalStr(value: Any) -> Optional[str]:
    return str(value) if value is not None else None

def OptionalInt(value: Any) -> Optional[int]:
    return int(value) if value is not None else None

def OptionalFloat(value: Any) -> Optional[float]:
    return float(value) if value is not None else None

def OptionalBool(value: Any) -> Optional[bool]:
    return bool(value) if value is not None else None

def OptionalList(value: Any) -> Optional[list]:
    return list(value) if value is not None else None

def OptionalDict(value: Any) -> Optional[dict]:
    return dict(value) if value is not None else None

def get_value_or_none(data, path) -> Optional[Any]:
    try:
        return reduce(lambda x, y: x[y], path, data)
    except (KeyError, TypeError):
        return None

@dataclass
class PropertyRefiner:

    name: str
    dtype: type
    path: List[str]

    def __call__(self, data: dict) -> Optional[dict]:
        return {self.name: self.dtype(get_value_or_none(data, self.path))}
        
    def sha256(self) -> str:
        return sha256((self.name + str(self.dtype) + "".join(self.path)).encode()).hexdigest()
        
@dataclass
class ListRefiner:

    name: str
    refiner: Union["DictRefiner", "ListRefiner", "PropertyRefiner"]
    path: List[str]
    agg: Optional[Callable[[list], Any]] = lambda x: x

    def __call__(self, data: dict) -> dict:
        return {
            self.name: self.agg(
                list(
                    map(
                        self.refiner, 
                        get_value_or_none(data, self.path)
                    )
                )
            )
        }
    
    def sha256(self) -> str:
        return sha256((self.name + self.refiner.sha256() + "".join(self.path)).encode()).hexdigest()
    
@dataclass
class DictRefiner:

    name: str
    children: List[Union["DictRefiner", "ListRefiner", "PropertyRefiner"]]
    agg: Optional[Callable[[dict], Any]] = lambda x: x

    def __call__(self, data: dict) -> dict:
        return {
            self.name: self.agg(
                reduce(
                    lambda acc, x: {**acc, **x},
                    filter(
                        lambda x: x is not None,
                        map(
                            lambda refine: refine(data),
                            self.children
                        )
                    ),
                    {}
                )
            )
        }
    
    def sha256(self) -> str:
        return sha256((self.name + "".join(map(lambda x: x.sha256(), self.children))).encode()).hexdigest()
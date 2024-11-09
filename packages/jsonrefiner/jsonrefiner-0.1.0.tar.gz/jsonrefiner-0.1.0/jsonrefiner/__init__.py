from dataclasses import dataclass
from typing import List, Union, Optional, Callable, Any
from functools import reduce
from hashlib import sha256

@dataclass
class PropertyRefiner:

    name: str
    dtype: type
    path: List[str]

    def __call__(self, data: dict) -> Optional[dict]:
        return {self.name: self.dtype(reduce(lambda x,y: x[y], self.path, data))}
        
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
                        reduce(lambda x,y: x[y], self.path, data)
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
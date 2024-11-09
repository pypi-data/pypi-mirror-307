# JsonRefiner

JsonRefiner is a lightweight Python package designed for transforming dictionaries into other dictionaries with converted data types, aggregations, different paths, and rearrangements of certain properties. It allows you to refine and restructure JSON-like data with ease.

## Install
```bash
pip install -U jsonrefiner
```

## How to
There are three classes that are used for transforming your input dict.

### PropertyRefiner
The basic refiner function object
```python
# Changing the name of the user_id field
PropertyRefiner(

    # Create a new property called "id" to your output dict
    name="id",

    # Convert/ensure the data type from the input dict to be `str`
    # (Any function is allowed here)
    dtype=str, 

    # Point to where, in the original dict, the data is.
    # It works like a folder path to a file. This example
    # is for when {"user_id": "..."} is input.
    path=["user_id"]
)
```

### ListRefiner
The refiner object for transforming lists. Let's say an object has a list of address information and you'd like to apply one transformation to all of the items
```python
ListRefiner(

    # The new name in the output dict
    name="phone",

    # The refiner function object to apply on each item in the list
    refiner=PropertyRefiner(
        name="city", 
        dtype=str, 

        # NOTE that this path is referring from the list object,
        # not from the input object itself.
        path=["city"]
    ),

    # The path in the input object to where we fine the list items
    path=["addresses"]
)
```

### DictRefiner
The refiner object for transforming dicts/objects. This is usually the starting point refiner in most cases.

```python
DictRefiner(

    # The name of the new object. The output from running this
    # refiner function object would have one property "user"
    name="user",

    # Sub refiners applied to the input object's content
    refiners=[

        # Any refiner goes here
        PropertyRefiner(...),
        ListRefiner(...),
        DictRefiner(...),
    ]
)
```


## Full Example
```python

from jsonrefiner import DictRefiner, ListRefiner, PropertyRefiner

# We'd like to convert and reassemble some data from 
# this type of structure:
input_data = {
    "user_id": "12345",
    "name": {
        "first": "Jane",
        "last": "Doe"
    },
    "age": "29",
    "email": "janedoe@example.com",
    "address": {
        "street": "123 Maple Street",
        "city": "Springfield",
        "state": "IL",
        "postal_code": "62704"
    },
    "phone_numbers": [
        {
            "number": "123-456-7890"
        }
    ]
}

# We'd use the Refiner classes to construct a transformation
# as a function that can be applied to the input data.
refiner = DictRefiner(
    name="user",
    children=[

        # Changing the name of the user_id field
        PropertyRefiner(
            name="id",
            dtype=str, 
            path=["user_id"]
        ),

        # Converting the age to an integer
        PropertyRefiner(
            name="age",
            dtype=int, 
            path=["age"]
        ),

        # Turning name into a single string
        DictRefiner(
            name="name",
            children=[
                PropertyRefiner(
                    name="first name", 
                    dtype=str, 
                    path=["name", "first"],
                ),
                PropertyRefiner(
                    name="last name", 
                    dtype=str, 
                    path=["name", "last"]
                )
            ],
            agg=lambda x: f"{x['first name']} {x['last name']}"
        ),
        
        # Turning address into a single string
        DictRefiner(
            name="address",
            children=[
                PropertyRefiner(
                    name="street", 
                    dtype=str, 
                    path=["address", "street"]
                ),
                PropertyRefiner(
                    name="city", 
                    dtype=str, 
                    path=["address", "city"]
                ),
                PropertyRefiner(
                    name="state", 
                    dtype=str, 
                    path=["address", "state"]
                ),
                PropertyRefiner(
                    name="postal_code", 
                    dtype=str, 
                    path=["address", "postal_code"]
                )
            ],
            agg=lambda x: f"{x['street']}, {x['city']}, {x['state']} {x['postal_code']}",
        ),
    ],
)

# We can then apply the refiner to the input data
actual_output_object = refiner(input_data)
expected_output_object = {
    "user": {
        "id": "12345", 
        "age": 29, 
        "name": "Jane Doe", 
        "address": "123 Maple Street, Springfield, IL 62704"
    }
}
assert actual_output_object == expected_output_object
```
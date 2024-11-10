import json
from typing import Type, TypeVar, Optional

T = TypeVar('T')

def serialize(class_instance, save_file: bool = False, file_path: Optional[str] = None) -> str:
    """_summary_
    Method to serialize class into json string
    Args:
        class_instance (_type_): _description_
        save_file (bool, optional): _description_. Defaults to False.
        file_path (Optional[str], optional): _description_. Defaults to None.

    Returns:
        str: The json string representation of the class.
    """
    json_string = json.dumps(class_instance.__dict__)
    if (save_file):
        file = open(file_path, "w", encoding="utf-8")
        file.write(json_string)
        file.close
    return json_string

def deserialize(class_type: Type[T], file_path: str) -> T:
    """Method to deserialize json file and return class instance.
    Args:
        class_type (Type[T]): class type which should be returned
        file_path (str): the json file path

    Returns:
        T: the instance of class T
    """
    with open(file_path, "r", encoding="utf-8") as file:
        json_data = json.load(file)
    return class_type(**json_data)
    
import hashlib
import inspect
import re
from ast import literal_eval
from functools import wraps
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Type,
    Union,
)

from docstring_parser import parse
from loguru import logger
from pydantic import BaseModel


def extract_code_block(text: str) -> str:
    """
    Extracts code blocks from the given text.

    Args:
    text (str): The input text containing code blocks.

    Returns:
    str: The text with code blocks extracted.
    """
    pattern = re.compile(r"^```[\w\s]*\n([\s\S]*?)^```$", re.MULTILINE)
    result = pattern.sub(r"\1", text)
    return result.strip()


def generate_output_schema(cls: Type[BaseModel]) -> dict:
    """
    Generates the schema compatible with the LLM function-call API for a given Pydantic model.

    Args:
        cls (Type[BaseModel]): The Pydantic model class to generate the schema for.

    Returns:
        dict: The schema as a dictionary.
    """
    schema = cls.model_json_schema()
    docstring = parse(cls.__doc__ or "")
    parameters = {k: v for k, v in schema.items() if k not in ("title", "description")}

    # Use docstring for the description
    description = (
        docstring.short_description if docstring.short_description else f"{cls.__name__} function"
    )

    parameters["properties"] = {
        field: details for field, details in parameters["properties"].items()
    }
    parameters["required"] = sorted(
        k for k, v in parameters["properties"].items() if "default" not in v
    )
    recursive_purge_dict_key(parameters, "additionalProperties")
    recursive_purge_dict_key(parameters, "title")

    return {
        "name": cls.__name__,
        "description": description,
        "parameters": parameters,
    }


def log_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise

    return wrapper


def hash(obj: Any) -> str:
    if isinstance(obj, (str, int, float, bool, type(None))):
        return hashlib.sha256(str(obj).encode()).hexdigest()
    elif isinstance(obj, (list, tuple)):
        return hashlib.sha256(str(tuple(hash(i) for i in obj)).encode()).hexdigest()
    elif isinstance(obj, set):
        return hashlib.sha256(str(sorted(hash(i) for i in obj)).encode()).hexdigest()
    elif isinstance(obj, dict):
        return hashlib.sha256(
            str(sorted((hash(k), hash(v)) for k, v in obj.items())).encode()
        ).hexdigest()
    elif callable(obj):
        return hashlib.sha256(inspect.getsource(obj).encode()).hexdigest()
    else:
        return hashlib.sha256(str(type(obj)).encode()).hexdigest()


def recursive_purge_dict_key(d: Any, k: str) -> None:
    """Remove a key from a dictionary recursively."""
    if isinstance(d, dict):
        keys_to_delete = [key for key, value in d.items() if key == k]
        for key in keys_to_delete:
            del d[key]
        for value in d.values():
            recursive_purge_dict_key(value, k)
    elif isinstance(d, list):
        for item in d:
            recursive_purge_dict_key(item, k)


def function_to_dict(input_function: Callable[..., Any]) -> Dict[str, Any]:
    """
    Convert a function with docstring to a dictionary usable for OpenAI function calling.

    This function supports multiple docstring styles: Google, reStructuredText (reST), and NumPy.

    Parameters
    ----------
    input_function : Callable[..., Any]
        A function with a docstring

    Returns
    -------
    Dict[str, Any]
        A dictionary to add to the list passed to `functions` parameter of `litellm.completion`

    Raises
    ------
    ImportError
        If required dependencies are not installed
    """
    try:
        from docstring_parser import parse
    except ImportError:
        raise ImportError("Please install docstring_parser: pip install docstring_parser")

    def json_schema_type(type_name: str) -> str:
        type_map = {
            "int": "integer",
            "float": "number",
            "str": "string",
            "bool": "boolean",
            "list": "array",
            "dict": "object",
        }
        return type_map.get(type_name.lower(), type_name.lower())

    name = input_function.__name__
    docstring = inspect.getdoc(input_function)
    parsed_docstring = parse(docstring)

    description = parsed_docstring.short_description
    if parsed_docstring.long_description:
        description += "\n" + parsed_docstring.long_description

    parameters: Dict[str, Dict[str, Union[str, List[str]]]] = {}
    required_params: List[str] = []
    param_info = inspect.signature(input_function).parameters

    for param_name, param in param_info.items():
        param_type = (
            json_schema_type(param.annotation.__name__)
            if param.annotation != inspect.Parameter.empty
            else None
        )
        param_description = None
        param_enum = None

        # Extract param description from parsed docstring
        for docstring_param in parsed_docstring.params:
            if docstring_param.arg_name == param_name:
                if docstring_param.type_name:
                    param_type = docstring_param.type_name
                    if "optional" in param_type.lower():
                        param_type = param_type.split(",")[0]
                    elif "{" in param_type:
                        try:
                            param_enum = list(literal_eval(param_type))
                            param_type = "string"
                        except Exception:
                            pass
                    param_type = json_schema_type(param_type)
                param_description = docstring_param.description

        param_dict: Dict[str, Optional[Union[str, List[str]]]] = {
            "type": param_type,
            "description": param_description,
        }
        if param_enum:
            param_dict["enum"] = param_enum

        parameters[param_name] = {k: v for k, v in param_dict.items() if v is not None}

        if param.default == param.empty:
            required_params.append(param_name)

    result = {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": parameters,
        },
    }

    if required_params:
        result["parameters"]["required"] = required_params

    return result

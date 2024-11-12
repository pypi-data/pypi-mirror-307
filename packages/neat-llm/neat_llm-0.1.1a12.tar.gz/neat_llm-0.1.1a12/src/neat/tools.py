import asyncio
import inspect
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    List,
    Optional,
    ParamSpec,
    TypeVar,
    Union,
    overload,
)

from loguru import logger
from pydantic import Field, create_model
from pydantic.json_schema import model_json_schema

from neat.utils import function_to_dict, recursive_purge_dict_key

T = TypeVar("T")
P = ParamSpec("P")


class ToolManager:
    def __init__(self):
        self.registered_tools: Dict[str, Dict[str, Any]] = {}

    def _register_tool(
        self,
        func: Union[Callable[..., Any], classmethod],
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        if isinstance(func, classmethod):
            func = func.__func__

        tool_name = name or func.__name__
        tool_description = description or func.__doc__

        try:
            parameters = function_to_dict(func)["parameters"]
            print(parameters)
        except Exception as e:
            logger.warning(f"Error using litellm.utils.function_to_dict: {e}")
            logger.warning("Falling back to Pydantic schema generation.")
            parameters = self.generate_schema(func)

        self.registered_tools[tool_name] = {
            "function": func,
            "description": tool_description,
            "parameters": parameters,
            "is_async": asyncio.iscoroutinefunction(func),
            "is_classmethod": isinstance(func, classmethod),
        }

        logger.debug(f"Tool '{tool_name}' registered successfully.")

    def add_tool(
        self,
        func: Union[Callable[..., Any], classmethod],
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        self._register_tool(func, name, description)

    @overload
    def tool(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Callable[[Callable[P, T]], Callable[P, T]]: ...

    @overload
    def tool(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]: ...

    def tool(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Union[
        Callable[[Callable[P, T]], Callable[P, T]],
        Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]],
    ]:
        def decorator(
            func: Callable[P, Union[T, Awaitable[T]]],
        ) -> Callable[P, Union[T, Awaitable[T]]]:
            self._register_tool(func, name, description)
            return func

        return decorator

    def generate_schema(self, func: Callable[..., Any]) -> Dict[str, Any]:
        signature = inspect.signature(func)
        fields: Dict[str, Any] = {}
        for name, param in signature.parameters.items():
            if name == "self" or name == "cls":
                continue
            annotation = (
                param.annotation if param.annotation != inspect.Parameter.empty else Any
            )
            default = ... if param.default == inspect.Parameter.empty else param.default
            fields[name] = (annotation, Field(default=default))

        model = create_model(f"{func.__name__}Model", **fields)
        schema = model_json_schema(model)

        recursive_purge_dict_key(schema, "title")
        recursive_purge_dict_key(schema, "additionalProperties")

        return schema

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": tool_info["description"],
                    "parameters": tool_info["parameters"],
                },
            }
            for tool_name, tool_info in self.registered_tools.items()
        ]

    async def use_tool(self, function_name: str, function_args: Dict[str, Any]) -> Any:
        if function_name not in self.registered_tools:
            logger.error(f"Tool '{function_name}' not found")
            return f"Error: Tool '{function_name}' not found"

        tool_info = self.registered_tools[function_name]
        function_to_call = tool_info["function"]
        is_async = tool_info["is_async"]
        is_classmethod = tool_info["is_classmethod"]

        try:
            logger.debug(
                f"Calling function '{function_to_call.__name__}' with args: {function_args}"
            )
            if is_classmethod:
                # If it's a classmethod, we need to get the class and call the method on it
                cls = function_to_call.__self__
                if is_async:
                    function_response = await getattr(cls, function_to_call.__name__)(
                        **function_args
                    )
                else:
                    function_response = await asyncio.to_thread(
                        getattr(cls, function_to_call.__name__), **function_args
                    )
            else:
                if is_async:
                    function_response = await function_to_call(**function_args)
                else:
                    function_response = await asyncio.to_thread(
                        function_to_call, **function_args
                    )
            logger.debug(f"Function result: {function_response}")
            return function_response
        except Exception as e:
            error_message = f"Error executing {function_name}: {str(e)}"
            logger.error(f"Error in function call: {error_message}")
            return error_message

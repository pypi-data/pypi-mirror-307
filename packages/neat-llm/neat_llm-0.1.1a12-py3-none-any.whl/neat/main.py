import asyncio
import inspect
import json
import time
from functools import wraps
from textwrap import dedent
from typing import (
    Any,
    AsyncGenerator,
    AsyncIterator,
    Awaitable,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    ParamSpec,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)

import litellm
from loguru import logger
from pydantic import BaseModel
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from neat.config import STRUCTURED_OUTPUT_MODELS, UNSUPPORTED_TOOL_MODELS, settings
from neat.constants import LLMModel
from neat.database import init_db, load_prompt, save_execution, save_prompt
from neat.exceptions import (
    IncompatibleArgumentsError,
    TemperatureRangeError,
    UnsupportedModelFeaturesError,
)
from neat.models import ExecutionData, Message, PromptData, UsageData
from neat.tools import ToolManager
from neat.utils import extract_code_block, generate_output_schema, hash

litellm.set_verbose = False # type: ignore
litellm.telemetry = False
litellm.drop_params = True
litellm.add_function_to_prompt = False
console = Console()
ResponseContent = TypeVar('ResponseContent', bound=BaseModel)
StreamChunk = Union[str, ResponseContent, Dict[str, Any], UsageData]
T = TypeVar("T", bound=BaseModel)
P = ParamSpec("P")
MessageType = Union[Message, Dict[str, str]]
LLMResponse = Union[ResponseContent, str]
StreamResponse = AsyncGenerator[StreamChunk, None]
class Neat:
    def __init__(self):
        self.tool_manager: ToolManager = ToolManager()

    def _validate_inputs(
        self,
        model: Union[LLMModel, str],
        temp: float,
        tools: List[Callable],
        response_model: Optional[Type[T]],
    ) -> str:
        if isinstance(model, LLMModel):
            model = model.model_name
        elif isinstance(model, str):
            model = model
        if not isinstance(temp, (int, float)) or temp < 0 or temp > 1:
            raise TemperatureRangeError("Temperature must be a float between 0 and 1")

        if model in UNSUPPORTED_TOOL_MODELS and (tools or response_model):
            raise UnsupportedModelFeaturesError(
                f"Tool calling or structured outputs are not supported for the {model} model."
            )

        if tools and response_model:
            raise IncompatibleArgumentsError(
                "Cannot set both 'tools' and 'response_model'. Please choose one or the other."
            )
        return model

    def _get_environment_representation(
        self, func: Callable
    ) -> Dict[str, Dict[str, Any]]:
        closure = inspect.getclosurevars(func)
        return {
            "nonlocals": {
                k: v for k, v in closure.nonlocals.items() if not k.startswith("__")
            },
            "globals": {
                k: v
                for k, v in closure.globals.items()
                if not k.startswith("__") and k != "ell"
            },
        }

    def _handle_database_operations(
        self,
        func: Callable,
        func_name: str,
        model: str,
        temperature: float,
        messages: List[Message],
    ) -> Tuple[Optional[int], Optional[PromptData], List[Message]]: 
        init_db()
        env_repr = self._get_environment_representation(func)
        func_hash = hash(inspect.getsource(func))
        env_hash = hash(json.dumps(env_repr, sort_keys=True))
        version_hash = hash(func_hash + env_hash)

        existing_prompt = load_prompt(func_name)

        if existing_prompt and existing_prompt.hash == version_hash:
            logger.debug(
                f"Using existing prompt version for '{func_name}': v{existing_prompt.version}"
            )
            return (
                existing_prompt.id,
                existing_prompt,
                [Message(**m) for m in json.loads(existing_prompt.prompt)],
            )

        new_version = (existing_prompt.version + 1) if existing_prompt else 1
        prompt_content = json.dumps(
            [m.model_dump(exclude_none=True, exclude_unset=True) for m in messages]
        )

        prompt_data = PromptData(
            func_name=func_name,
            version=new_version,
            hash=version_hash,
            model=model,
            temperature=temperature,
            prompt=prompt_content,
            environment=json.dumps(env_repr, default=str),
        )
        prompt_id = save_prompt(prompt_data)
        logger.debug(f"New prompt version created for '{func_name}': v{new_version}")

        return prompt_id, prompt_data, messages

    def _generate_api_params(
        self,
        model: str,
        messages: List[Message],
        temperature: float,
        response_model: Optional[Type[T]],
        tool_definitions: List[Dict[str, Any]],
        stream: bool = False,
    ) -> Dict[str, Any]:
        api_params: Dict[str, Any] = {
            "model": model,
            "messages": [
                m.model_dump(exclude_none=True, exclude_unset=True) for m in messages
            ],
            "temperature": temperature,
            "max_tokens": 7000,
            "stream": stream,
        }

        if response_model:
            if model in STRUCTURED_OUTPUT_MODELS:
                api_params["response_format"] = response_model
            else:
                api_params["tools"] = [
                    {
                        "type": "function",
                        "function": generate_output_schema(response_model),
                    }
                ]
                api_params["tool_choice"] = "auto"
                api_params["messages"].append(
                    {
                        "role": "user",
                        "content": f"Call the {response_model.__name__} function to answer the question above.",
                    }
                )
        elif tool_definitions:
            api_params["tools"] = tool_definitions
            api_params["tool_choice"] = "auto"

        if stream:
            api_params["stream_options"] = {"include_usage": True}

        return api_params

    async def _stream_llm_response(
        self,
        messages: List[Message],
        model: str,
        temperature: float,
        tool_definitions: List[Dict[str, Any]],
        response_model: Optional[Type[ResponseContent]],
    ) -> AsyncGenerator[StreamChunk, None]:
        api_params = self._generate_api_params(
            model, messages, temperature, response_model, tool_definitions, stream=True
        )
        api_params["stream_options"] = {"include_usage": True}
        
        accumulated_content = ""
        accumulated_function_args = ""
        current_function_name = None
        final_cost = None
        
        async for chunk in await litellm.acompletion(**api_params): # type: ignore
            delta = chunk.choices[0].delta
            
            # Handle usage data if present
            if hasattr(chunk, 'usage') and chunk.usage:
                # Calculate costs using litellm's helper function
                prompt_cost, completion_cost = litellm.cost_calculator.cost_per_token(
                    model=model,
                    prompt_tokens=chunk.usage.prompt_tokens,
                    completion_tokens=chunk.usage.completion_tokens
                )
                
                total_cost = (prompt_cost or 0) + (completion_cost or 0)
                
                usage_data = UsageData(
                    prompt_tokens=chunk.usage.prompt_tokens,
                    completion_tokens=chunk.usage.completion_tokens,
                    total_tokens=chunk.usage.total_tokens,
                    cost_usd=total_cost
                )
                yield usage_data
                continue
                
            if delta.content is not None:
                accumulated_content += delta.content
                yield delta.content
                
            if delta.tool_calls:
                for tool_call in delta.tool_calls:
                    if tool_call.function.name and not current_function_name:
                        current_function_name = tool_call.function.name
                    if tool_call.function.arguments:
                        accumulated_function_args += tool_call.function.arguments
                        
                    if accumulated_function_args:
                        try:
                            # Try to parse as complete JSON
                            parsed_args = json.loads(accumulated_function_args)
                            if response_model:
                                validated_content = response_model.model_validate(parsed_args)
                                yield validated_content
                            else:
                                yield {
                                    "function": current_function_name,
                                    "arguments": parsed_args
                                }
                        except json.JSONDecodeError:
                            # If not complete JSON, continue accumulating
                            continue

    @overload
    async def _interact_with_llm(
        self,
        messages: List[Message],
        model: str,
        temperature: float,
        tool_definitions: List[Dict[str, Any]],
        response_model: Optional[Type[ResponseContent]],
        stream: Literal[False] = False,
    ) -> Tuple[Any, Optional[LLMResponse], UsageData]: ...

    @overload
    async def _interact_with_llm(
        self,
        messages: List[Message],
        model: str,
        temperature: float,
        tool_definitions: List[Dict[str, Any]],
        response_model: Optional[Type[ResponseContent]],
        stream: Literal[True],
    ) -> AsyncGenerator[StreamChunk, None]: ...

    async def _interact_with_llm(
        self,
        messages: List[Message],
        model: str,
        temperature: float,
        tool_definitions: List[Dict[str, Any]],
        response_model: Optional[Type[ResponseContent]],
        stream: bool = False,
    ) -> Union[Tuple[Any, Optional[LLMResponse], UsageData], AsyncGenerator[StreamChunk, None]]:
        if stream:
            return self._stream_llm_response(
                messages, model, temperature, tool_definitions, response_model
            )
            
        api_params = self._generate_api_params(
            model, messages, temperature, response_model, tool_definitions
        )
        llm_response: Any = await litellm.acompletion(**api_params)
        llm_message = llm_response.choices[0].message
        
        # Calculate cost using litellm's helper function
        prompt_cost, completion_cost = litellm.cost_calculator.cost_per_token(
            model=model,
            prompt_tokens=llm_response.usage.prompt_tokens,
            completion_tokens=llm_response.usage.completion_tokens
        )
        total_cost = (prompt_cost or 0) + (completion_cost or 0)
        
        # Create usage data object with calculated cost
        usage_data = UsageData(
            prompt_tokens=llm_response.usage.prompt_tokens,
            completion_tokens=llm_response.usage.completion_tokens,
            total_tokens=llm_response.usage.total_tokens,
            cost_usd=total_cost
        )
        
        if llm_message.content:
            pass
        else:
            llm_message.content = ""  # !FIXME hack to patch litellm+cohere compatibility issues, remove when fixed
            
        if response_model:
            try:
                if llm_message.tool_calls:
                    tool_call_arguments = llm_message.tool_calls[0].function.arguments
                    parsed_content = (
                        json.loads(tool_call_arguments)
                        if isinstance(tool_call_arguments, str)
                        else tool_call_arguments
                    )
                else:
                    parsed_content = json.loads(extract_code_block(llm_message.content))

                validated_content = response_model.model_validate(parsed_content)
                return llm_response, validated_content, usage_data

            except json.JSONDecodeError as e:
                logger.error(f"Error parsing response: {e}")
                raise
                
        return llm_response, llm_message.content, usage_data

    async def _process_messages(
        self,
        messages: Union[Sequence[MessageType], List[Message]],
        model: str,
        temperature: float,
        tools: List[Callable],
        response_model: Optional[Type[ResponseContent]],
        use_db: bool,
        max_iterations: int,
        conversation: bool,
        prompt_id: Optional[int],
        stream: bool = False,
    ) -> Union[Tuple[LLMResponse, UsageData], StreamResponse]:
        processed_messages: List[Message] = [
            message if isinstance(message, Message) else Message.from_dict(cast(Dict[str, str], message))
            for message in messages
        ]
                
        tool_definitions: List[Dict[str, Any]] = (
            self.tool_manager.get_tool_definitions()
            if tools and not response_model
            else []
        )

        start_time: float = time.time()
        total_prompt_tokens: int = 0
        total_completion_tokens: int = 0

        try:
            if stream:
                async def stream_processor() -> AsyncGenerator[StreamChunk, None]:
                    llm_response = await self._interact_with_llm(
                        processed_messages,
                        model,
                        temperature,
                        tool_definitions,
                        response_model,
                        stream=True
                    ) # type: ignore
                    async for chunk in llm_response:
                        if isinstance(chunk, UsageData):
                            nonlocal total_prompt_tokens, total_completion_tokens
                            total_prompt_tokens = chunk.prompt_tokens or 0
                            total_completion_tokens = chunk.completion_tokens or 0
                            if use_db and prompt_id is not None:
                                execution_data = ExecutionData(
                                    version_id=prompt_id,
                                    prompt_tokens=total_prompt_tokens,
                                    completion_tokens=total_completion_tokens,
                                    execution_time=time.time() - start_time,
                                    usage=chunk
                                )
                                await asyncio.to_thread(save_execution, execution_data)
                        yield chunk

                return stream_processor()

            final_content: Optional[Union[ResponseContent, str]] = None
            final_usage: Optional[UsageData] = None
            
            while True:
                for iteration in range(max_iterations):
                    llm_response, content, usage_data = await self._interact_with_llm(
                        processed_messages,
                        model,
                        temperature,
                        tool_definitions,
                        response_model,
                    )
                    
                    # Update token counts
                    total_prompt_tokens = usage_data.prompt_tokens or 0
                    total_completion_tokens = usage_data.completion_tokens or 0
                    final_usage = usage_data
                    
                    llm_message = llm_response.choices[0].message
                    
                    if not llm_message:
                        raise ValueError("No message returned from LLM")
                        
                    processed_messages.append(
                        Message(**llm_message.model_dump(exclude_none=False))
                    )

                    if llm_message.content is None:
                        llm_message.content = ""

                    if response_model:
                        final_content = content
                        break

                    if not llm_message.tool_calls:
                        final_content = content
                        break
                        
                    for tool_call in llm_message.tool_calls:
                        function_name: str = str(tool_call.function.name)
                        function_args: Dict[str, Any] = json.loads(
                            tool_call.function.arguments
                        )
                        logger.debug(f"Calling tool: {function_name}")

                        function_response: Any = await self.tool_manager.use_tool(
                            function_name, function_args
                        )
                        logger.debug(f"function response: {function_response}")

                        processed_messages.append(
                            Message(
                                tool_call_id=tool_call.id,
                                role="tool",
                                name=function_name,
                                content=str(function_response),
                            )
                        )
                else:
                    logger.warning(
                        f"Reached maximum iterations ({max_iterations}) without resolution"
                    )
                    break

                if conversation:
                    console.print(
                        Panel(
                            Markdown(str(final_content) or ""),
                            title="AI",
                            border_style="cyan",
                        )
                    )
                    user_input: str = console.input()
                    console.print(f"[bold green]{user_input}[/bold green]")

                    if user_input.lower() in ["exit", "quit"]:
                        console.print("[bold red]Exiting conversation...[/bold red]")
                        break
                    if user_input == "":
                        user_input = " "
                    processed_messages.append(Message(role="user", content=user_input))
                    continue
                else:
                    break

            execution_time: float = time.time() - start_time

            if use_db and prompt_id is not None and final_usage:
                execution_data = ExecutionData(
                    version_id=prompt_id,
                    prompt_tokens=total_prompt_tokens,
                    completion_tokens=total_completion_tokens,
                    execution_time=execution_time,
                    usage=final_usage
                )
                await asyncio.to_thread(save_execution, execution_data)

            if final_content is None:
                raise ValueError("No content generated from LLM")
                
            if final_usage is None:
                raise ValueError("No usage data available")
                
            return final_content, final_usage

        except Exception as e:
            logger.error(f"Error in LLM completion: {str(e)}")
            raise

    def lm(
        self,
        model: Union[LLMModel, str] = settings.default_model,
        temperature: float = settings.default_temperature,
        tools: List[Callable] = [],
        response_model: Optional[Type[ResponseContent]] = None,
        use_db: bool = False,
        max_iterations: int = 20,
        conversation: bool = False,
        stream: bool = False,
    ) -> Callable[
        [Callable[P, Awaitable[Union[List[Message], List[Dict[str, str]]]]]],
        Callable[P, Awaitable[Union[LLMResponse, StreamResponse]]]
    ]:
        """
        Async decorator for language model interactions.
        
        Args:
            model: The language model to use
            temperature: Sampling temperature
            tools: Optional list of tool functions to use
            response_model: Optional Pydantic model for structured output
            use_db: Whether to use database logging
            max_iterations: Maximum number of tool call iterations
            conversation: Whether to enable conversation mode
            stream: Whether to stream the response
        
        Returns:
            A decorated function that returns either:
            - A single response (when stream=False)
            - An async generator yielding response chunks (when stream=True)
        """
        model = self._validate_inputs(model, temperature, tools, response_model)

        def decorator(
            func: Callable[P, Awaitable[Union[List[Message], List[Dict[str, str]]]]]
        ) -> Callable[P, Awaitable[Union[LLMResponse, StreamResponse]]]:
            if not asyncio.iscoroutinefunction(func):
                raise TypeError("The decorated function must be async. Use 'async def'.")

            @wraps(func)
            async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Union[LLMResponse, StreamResponse]:
                messages = await func(*args, **kwargs)
                prompt_id, prompt_data = None, None

                if use_db:
                    prompt_id, prompt_data, messages = await asyncio.to_thread(
                        self._handle_database_operations,
                        func,
                        func.__name__,
                        model,
                        temperature,
                        messages,
                    )

                return await self._process_messages(
                    messages,
                    model,
                    temperature,
                    tools,
                    response_model,
                    use_db,
                    max_iterations,
                    conversation,
                    prompt_id,
                    stream,
                )

            return wrapper

        return decorator

    def add_tool(
        self,
        func: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        """Add a tool function to the tool manager."""
        self.tool_manager.add_tool(func, name, description)

    def tool(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Callable[[Callable], Callable]:
        """Decorator to register a tool function."""
        return self.tool_manager.tool(name, description)

    @staticmethod
    def system(content: str) -> Message:
        """Create a system message."""
        return Message(role="system", content=dedent(content.strip()))

    @staticmethod
    def user(content: str) -> Message:
        """Create a user message."""
        return Message(role="user", content=dedent(content.strip()))

    @staticmethod
    def assistant(content: str) -> Message:
        """Create an assistant message."""
        return Message(role="assistant", content=dedent(content.strip()))


neat = Neat()
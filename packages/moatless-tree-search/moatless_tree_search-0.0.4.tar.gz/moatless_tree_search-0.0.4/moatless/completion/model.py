import json
import logging
from typing import Optional, Any, Union

import litellm
from litellm import cost_per_token, NotFoundError
from pydantic import BaseModel, model_validator, Field

logger = logging.getLogger(__name__)


class Message(BaseModel):
    role: str = Field(..., description="The role of the sender")
    content: Optional[str] = Field(None, description="The message content")


class ToolCall(BaseModel):
    name: str = Field(..., description="The name of the tool being called")
    type: Optional[str] = Field(None, description="The type of tool call")
    input: Optional[dict[str, Any]] = Field(None, description="The input parameters for the tool")


class AssistantMessage(Message):
    role: str = Field("assistant", description="The role of the assistant")
    content: Optional[str] = Field(None, description="The assistant's message content")
    tool_call: Optional[ToolCall] = Field(None, description="Tool call made by the assistant")


class UserMessage(Message):
    role: str = Field("user", description="The role of the user")
    content: str = Field(..., description="The user's message content")


class Usage(BaseModel):
    completion_cost: float = 0
    completion_tokens: int = 0
    prompt_tokens: int = 0
    cached_tokens: int = 0

    @classmethod
    def from_completion_response(
        cls, completion_response: dict | BaseModel, model: str
    ) -> Union["Usage", None]:
        if isinstance(completion_response, BaseModel) and hasattr(
            completion_response, "usage"
        ):
            usage = completion_response.usage.model_dump()
        elif isinstance(completion_response, dict) and "usage" in completion_response:
            usage = completion_response["usage"]
        else:
            logger.warning(
                f"No usage info available in completion response: {completion_response}"
            )
            return None

        logger.debug(f"Usage: {json.dumps(usage, indent=2)}")

        prompt_tokens = usage.get("prompt_tokens") or usage.get("input_tokens", 0)

        if usage.get("cache_creation_input_tokens"):
            prompt_tokens += usage["cache_creation_input_tokens"]

        completion_tokens = usage.get("completion_tokens") or usage.get(
            "output_tokens", 0
        )

        if usage.get("prompt_cache_hit_tokens"):
            cached_tokens = usage["prompt_cache_hit_tokens"]
        elif usage.get("cache_read_input_tokens"):
            cached_tokens = usage["cache_read_input_tokens"]
        else:
            cached_tokens = 0

        try:
            cost = litellm.completion_cost(
                completion_response=completion_response, model=model
            )
        except Exception:
            # If cost calculation fails, fall back to calculating it manually
            try:
                prompt_cost, completion_cost = cost_per_token(
                    model=model,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                )
                cost = prompt_cost + completion_cost
            except NotFoundError as e:
                logger.debug(
                    f"Failed to calculate cost for completion response: {completion_response}. Error: {e}"
                )
                cost = 0
            except Exception as e:
                logger.error(
                    f"Failed to calculate cost for completion response: {completion_response}. Error: {e}"
                )
                cost = 0

        return cls(
            completion_cost=cost,
            completion_tokens=completion_tokens,
            prompt_tokens=prompt_tokens,
            cached_tokens=cached_tokens
        )

    def __add__(self, other: "Usage") -> "Usage":
        return Usage(
            completion_cost=self.completion_cost + other.completion_cost,
            completion_tokens=self.completion_tokens + other.completion_tokens,
            prompt_tokens=self.prompt_tokens + other.prompt_tokens,
            cached_tokens=self.cached_tokens + other.cached_tokens,
        )

    def __str__(self) -> str:
        return (
            f"Usage(cost: ${self.completion_cost:.4f}, "
            f"completion tokens: {self.completion_tokens}, "
            f"prompt tokens: {self.prompt_tokens}, "
            f"cached tokens: {self.cached_tokens})"
        )

    @model_validator(mode='before')
    @classmethod
    def fix_null_tokens(cls, data: Any) -> Any:
        if isinstance(data, dict):
            for key, value in data.items():
                if not value:
                    data[key] = 0

        return data

class Completion(BaseModel):
    model: str
    input: list[dict] | None = None
    response: dict[str, Any] | None = None
    usage: Usage | None = None

    @classmethod
    def from_llm_completion(
        cls, input_messages: list[dict], completion_response: Any, model: str
    ) -> Optional["Completion"]:
        if isinstance(completion_response, BaseModel):
            response = completion_response.model_dump()
        elif isinstance(completion_response, dict):
            response = completion_response
        else:
            logger.error(
                f"Unexpected completion response type: {type(completion_response)}"
            )
            return None

        usage = Usage.from_completion_response(completion_response, model)

        return cls(
            model=model,
            input=input_messages,
            response=response,
            usage=usage,
        )

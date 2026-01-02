"""Type definitions for LLM infrastructure."""
from typing import Literal
from pydantic import BaseModel, Field
from enum import Enum


class MessageRole(str, Enum):
    """Enum for chat message roles."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(BaseModel):
    """Represents a single message in a chat conversation."""
    
    role: Literal["system", "user", "assistant"] = Field(
        description="The role of the message sender"
    )
    content: str = Field(
        description="The content of the message"
    )
    
    class Config:
        frozen = True  # Make immutable
        json_schema_extra = {
            "examples": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": "Hello, how are you?"
                },
                {
                    "role": "assistant",
                    "content": "I'm doing well, thank you!"
                }
            ]
        }

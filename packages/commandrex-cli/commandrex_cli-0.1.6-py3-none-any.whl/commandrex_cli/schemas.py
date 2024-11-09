from typing import List, Optional
from pydantic import BaseModel, Field


class Command(BaseModel):
    """Represents a parsed command with its components and metadata."""
    executable: str = Field(..., description="The main command to execute")
    args: List[str] = Field(default_factory=list, description="Command arguments")
    is_dangerous: bool = Field(
        default=False, 
        description="Flag indicating if command might be dangerous"
    )
    explanation: str = Field(
        default="No explanation provided", 
        description="Human-readable explanation of what the command does"
    )
    platform_specific: bool = Field(
        default=False,
        description="Whether this command is platform-specific"
    )

class TranslationResponse(BaseModel):
    """Response from the command translator."""
    command: Command
    confidence: float = Field(
        default=1.0,
        description="Confidence score of the translation"
    )
    alternatives: List[Command] = Field(
        default_factory=list,
        description="Alternative command suggestions"
    )

class CommandResult(BaseModel):
    """Result of executing a command."""
    success: bool
    output: str
    error: Optional[str] = None
    exit_code: int
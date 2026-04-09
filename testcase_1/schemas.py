from pydantic import BaseModel, Field
from typing import List, Optional

class Event(BaseModel):
    event_id: str = Field(..., description="A unique identifier for the event (e.g., event_001).")
    summary: str = Field(..., description="A brief one-sentence summary of what happened in the event.")
    characters: List[str] = Field(..., description="A list of characters involved in this event.")
    description: str = Field(..., description="A highly detailed and exhaustive description of the event and its impact.")

class EventList(BaseModel):
    events: List[Event] = Field(..., description="A list of multiple events extracted from the text.")

class Character(BaseModel):
    character_id: str = Field(..., description="A unique identifier for the character (e.g., character_001).")
    name: str = Field(..., description="The primary name of the character.")
    aliases: List[str] = Field(default=[], description="Other names or nicknames the character is known by.")
    description: Optional[str] = Field(None, description="A short description of the character's background or role.")
    traits: List[str] = Field(default=[], description="Key personality traits or characteristics.")
    abilities: List[str] = Field(default=[], description="Special skills, powers, or abilities.")
    event_ids: List[str] = Field(default=[], description="List of Event IDs this character is involved in.")

class CharacterList(BaseModel):
    characters: List[Character] = Field(..., description="A list of characters extracted from the text.")

class RelevantEvents(BaseModel):
    event_ids: List[str] = Field(..., description="A list of Event IDs that are relevant to the user's query.")
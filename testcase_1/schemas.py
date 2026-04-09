from pydantic import BaseModel
from typing import List, Optional

class Event(BaseModel):
    event_id: str              # unique id (E1, E2...)
    summary: str               # what happened
    characters: List[str]      # names or character_ids
    description: str           # full description of event

class EventList(BaseModel):
    events: List[Event]

class Character(BaseModel):
    character_id: str          # unique id (C1, C2...)
    name: str                  # main name
    aliases: List[str] = []    # other names (Harry, Mr. Potter)
    description: Optional[str] = None   # short description
    traits: List[str] = []     # e.g., brave, smart
    abilities: List[str] = []  # e.g., magic, fighting
    event_ids: List[str] = []  # linked events

class CharacterList(BaseModel):
    characters: List[Character]
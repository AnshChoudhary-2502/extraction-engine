from llm import model
from schemas import EventList
from langchain_core.prompts import ChatPromptTemplate

def extract_events(text_chunk: str) -> EventList:
    """Extract events from a given text chunk using the simplified Event schema."""

    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an expert literary analyst. Extract all significant events from the provided text chunk.\n\n"
            "An event is a specific occurrence, milestone, or thematic development in the story.\n\n"
            "For each event, create a separate object in the 'events' list with these fields:\n"
            "1. event_id: A unique ID (e.g., E1, E2...).\n"
            "2. summary: A brief one-sentence summary.\n"
            "3. characters: A list of names or IDs of characters involved.\n"
            "4. description: A highly detailed and exhaustive description of what happened and its impact.\n\n"
            "IMPORTANT: Do not merge events. Each event MUST be a separate item in the 'events' list. Never repeat field names within a single object."
        )),
        ("human", "{input}")
    ])
    
    structured_llm = model.with_structured_output(EventList)
    chain = prompt | structured_llm
    
    try:
        response = chain.invoke({"input": text_chunk})
        return response
    except Exception as e:
        print(f"Error during event extraction: {e}")
        return EventList(events=[])

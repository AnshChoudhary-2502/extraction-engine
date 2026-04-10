import time
import re
from llm import extraction_model
from schemas import EventList
from langchain_core.prompts import ChatPromptTemplate

def extract_events(text_chunk: str, max_retries: int = 5) -> EventList:
    """Extract events from a given text chunk using the simplified Event schema with retry logic for rate limits."""

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
    
    structured_llm = extraction_model.with_structured_output(EventList)
    chain = prompt | structured_llm
    
    for attempt in range(max_retries):
        try:
            response = chain.invoke({"input": text_chunk})
            return response
        except Exception as e:
            error_msg = str(e)
            
            # Check for Rate Limit errors (HTTP 429 or 'rate_limit_exceeded')
            if "429" in error_msg or "rate_limit" in error_msg.lower():
                # Attempt to extract suggested wait time from the error message (e.g., "try again in 4.48s")
                wait_time = 10  # Default fallback wait time
                match = re.search(r"try again in ([\d\.]+)s", error_msg)
                if match:
                    wait_time = float(match.group(1)) + 1.0  # Add a little buffer
                
                print(f"⚠️  Rate limit hit (Attempt {attempt+1}/{max_retries}). Retrying in {wait_time:.2f}s...")
                time.sleep(wait_time)
                continue
            else:
                print(f"❌ Error during event extraction: {e}")
                break # Non-retryable error
                
    return EventList(events=[])

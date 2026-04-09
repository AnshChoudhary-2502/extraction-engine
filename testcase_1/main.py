import json
from text_chunking import load_txt, chunk_text
from agents import extract_events
from schemas import Event, EventList, Character, CharacterList
import os

def main():
    file_path = "testcase_1/story.txt"
    print(f"Loading text from {file_path}...")
    text = load_txt(file_path)
    
    print("Chunking text...")
    chunks = chunk_text(text)
    print(f"Total chunks: {len(chunks)}")
    
    all_extracted_events = []
    global_event_counter = 1
    
    for i, chunk in enumerate(chunks):
        chunk_id = f"chunk_{i+1}"
        print(f"Processing {chunk_id}...")
        
        result = extract_events(chunk)
        if result and result.events:
            for event in result.events:
                # Override the local ID with a global one
                event_data = event.model_dump()
                event_data["event_id"] = f"event_{global_event_counter:03d}"
                all_extracted_events.append(event_data)
                global_event_counter += 1
    
    output_file = "events.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_extracted_events, f, indent=4)
        
    print(f"Successfully saved {len(all_extracted_events)} events to {output_file}")

if __name__ == "__main__":
    main()

import json
import os
import glob
from concurrent.futures import ThreadPoolExecutor, as_completed
from text_chunking import load_txt, chunk_text
from agents import extract_events
from schemas import EventList


def process_chunk(chunk, chunk_index, file_name):
    """Worker function to process a single chunk from a specific file."""
    print(f"    > [{file_name}] Processing chunk {chunk_index+1}...")
    result = extract_events(chunk)
    return result.events if result else []


def main():
    # Configuration
    # Input: Any .txt inside testcase_1/stories/
    # Output: Saved as testcase_1/events.json
    data_dir = os.path.dirname(os.path.abspath(__file__))
    stories_dir = os.path.join(data_dir, "stories")
    output_file = os.path.join(data_dir, "events.json")

    # 1. Find all .txt files recursively in the stories directory
    search_pattern = os.path.join(stories_dir, "**", "*.txt")
    file_paths = glob.glob(search_pattern, recursive=True)

    if not file_paths:
        print(f"Error: No .txt files found in {stories_dir}")
        return

    print(f"🚀 Found {len(file_paths)} files in stories folder.")

    all_extracted_events = []
    global_event_counter = 1

    # 2. Process each file
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        print(f"\n📖 Processing file: {file_path}")
        text = load_txt(file_path)

        print(f"✂️  Chunking {file_name}...")
        chunks = chunk_text(text)
        total_chunks = len(chunks)
        print(f"   Total chunks: {total_chunks}")

        file_results = {}

        # 3. Parallel Extraction per file
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(process_chunk, chunk, i, file_name): i
                for i, chunk in enumerate(chunks)
            }

            for future in as_completed(futures):
                idx = futures[future]
                try:
                    events = future.result()
                    file_results[idx] = events
                    print(f"    ✅ Chunk {idx+1}/{total_chunks} done")
                except Exception as exc:
                    print(f"    ❌ Chunk {idx+1} failed: {exc}")

        # 4. Aggregate events and assign global IDs
        for i in range(total_chunks):
            if i in file_results:
                for event in file_results[i]:
                    event_data = event.model_dump()
                    event_data["event_id"] = f"event_{global_event_counter:03d}"
                    event_data["source_path"] = file_path
                    all_extracted_events.append(event_data)
                    global_event_counter += 1

    # 5. Save all events inside testcase_1/
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_extracted_events, f, indent=4)

    print(
        f"\n✨ Successfully saved {len(all_extracted_events)} events to {output_file}"
    )


if __name__ == "__main__":
    main()

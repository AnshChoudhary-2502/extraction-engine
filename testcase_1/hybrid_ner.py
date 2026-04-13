import spacy
import json
import os
import sys
from typing import List, Dict

# Ensure we can import from the current directory for llm.py
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from llm import search_model
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from schemas import CharacterList, Character
from langchain_core.prompts import ChatPromptTemplate


def get_context_for_names(text: str, names: List[str], window: int = 500) -> str:
    """Extract small snippets of text around where names appear to give the LLM context."""
    context_chunks = []
    for name in names[:10]:  # Limit to top 10 raw names to keep prompt manageable
        idx = text.lower().find(name.lower())
        if idx != -1:
            start = max(0, idx - window)
            end = min(len(text), idx + window)
            context_chunks.append(
                f"--- Context for '{name}' ---\n...{text[start:end]}..."
            )
    return "\n\n".join(context_chunks)


def validation_phase(raw_names: List[str], story_text: str) -> List[Dict]:
    """Phase 2: LLM Validation, Deduplication, and Enrichment."""
    print(f"🧠 [PHASE 2] Enriching {len(raw_names)} raw entries with LLM...")

    # Get some context so the LLM knows traits/abilities
    context = get_context_for_names(story_text, raw_names)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are a Character Specialist. I will provide a list of names and some context snippets from a story.\n"
                    "Your task:\n"
                    "1. Filter out noise (locations, objects).\n"
                    "2. Group aliases into one Character object.\n"
                    "3. Fill in 'description', 'traits', and 'abilities' based on the context.\n"
                    "4. Assign a unique character_id (e.g., char_001)."
                ),
            ),
            ("human", "CONTEXT:\n{context}\n\nRAW NAMES: {names}"),
        ]
    )

    structured_llm = search_model.with_structured_output(CharacterList)
    chain = prompt | structured_llm

    response = chain.invoke({"names": ", ".join(raw_names), "context": context})

    # Note: event_ids will stay empty for now as they are backfilled after main.py runs
    return [c.model_dump() for c in response.characters]


def load_text(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def discovery_phase(text: str) -> List[str]:
    """Phase 1: Local NER discovery using spaCy."""
    print("🔍 [PHASE 1] Running Local NER (spaCy)...")
    nlp = spacy.load("en_core_web_sm")
    # Process text in chunks to avoid spaCy memory limits if story is huge
    chunk_size = 100000
    all_names = set()

    # spaCy's small model frequently misclassifies fictional character names:
    #   - "Stephen Strange" -> WORK_OF_ART
    #   - "the Ancient One" -> ORG
    # Cast a wider net here; the LLM validation phase (Phase 2) will filter
    # out non-characters (locations, objects, etc.) with much higher accuracy.
    candidate_labels = {"PERSON", "ORG", "WORK_OF_ART"}

    for i in range(0, len(text), chunk_size):
        doc = nlp(text[i : i + chunk_size])
        for ent in doc.ents:
            if ent.label_ in candidate_labels:
                all_names.add(ent.text)

    return sorted(list(all_names))


from llm import search_model, answer_model  # Import both for flexibility


def resolve_duplicates(registry: List[Dict]) -> List[Dict]:
    """Phase 3: Final Entity Resolution to merge duplicates and noise-wrapped names."""
    print(
        f"🧹 [PHASE 3] Consolidating {len(registry)} entries into unique characters (Using Mistral Large)..."
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are a Master Entity Resolver. I have a character list with noise-wrapped duplicates and false positives.\n\n"
                    "CRITICAL RULES:\n"
                    "1. If two or more entries refer to the same person, you MUST merge them into ONE single object.\n"
                    "2. Combine all aliases, traits, and abilities into unique, non-repeating lists.\n"
                    "3. If an entry is NOT a character (e.g., 'noisy', 'error', 'glitch'), you MUST DELETE it.\n"
                    "4. Return exactly ONE object per unique person.\n"
                    "5. Ensure ALL fields (character_id, name, aliases, description, traits, abilities, event_ids) are present."
                ),
            ),
            ("human", "REGISTRY DATA: {data}"),
        ]
    )

    # Use answer_model (Mistral Large) as it is more robust for entity resolution
    structured_llm = answer_model.with_structured_output(CharacterList)
    chain = prompt | structured_llm

    response = chain.invoke({"data": json.dumps(registry)})

    # Final cleanup of results
    final_list = []
    seen_names = set()
    for c in response.characters:
        name_key = c.name.lower().strip()
        if name_key not in seen_names:
            final_list.append(c.model_dump())
            seen_names.add(name_key)

    return final_list


def main():
    story_path = os.path.join(current_dir, "stories", "doctorstrange.txt")
    if not os.path.exists(story_path):
        print(f"Error: {story_path} not found.")
        return

    text = load_text(story_path)

    # Step 1: Discover
    raw_names = discovery_phase(text)
    print(f"Found {len(raw_names)} potential names locally.")

    # Step 2: Validate & Enrich
    initial_registry = validation_phase(raw_names, text)

    # Step 3: Resolve & Clean
    clean_registry = resolve_duplicates(initial_registry)

    print("\n✨ [FINAL CLEAN CHARACTER REGISTRY]")
    print(json.dumps(clean_registry, indent=4))

    # Save registry
    output_path = os.path.join(current_dir, "character_registry.json")
    with open(output_path, "w") as f:
        json.dump(clean_registry, f, indent=4)
    print(f"\nRegistry saved to {output_path}")


if __name__ == "__main__":
    main()

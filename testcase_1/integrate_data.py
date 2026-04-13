import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

def integrate():
    events_path = os.path.join(current_dir, "events.json")
    registry_path = os.path.join(current_dir, "character_registry.json")

    if not os.path.exists(events_path) or not os.path.exists(registry_path):
        print("Error: Missing events.json or character_registry.json. Please run main.py and hybrid_ner.py first.")
        return

    with open(events_path, "r", encoding="utf-8") as f:
        events = json.load(f)
    
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)

    print(f"🔗 Linking {len(events)} events to {len(registry)} characters...")

    for character in registry:
        # Create a set of all names/aliases for this character to check against
        search_names = {character["name"].lower()}
        for alias in character.get("aliases", []):
            search_names.add(alias.lower())
        
        # Track linked event IDs
        linked_events = []
        
        for event in events:
            # Check if any of the event's characters match our character's names/aliases
            event_characters = [c.lower() for c in event.get("characters", [])]
            
            # Simple intersection check
            if any(name in event_characters for name in search_names):
                linked_events.append(event["event_id"])
        
        character["event_ids"] = sorted(list(set(linked_events)))
        print(f"   ✅ {character['name']}: Linked to {len(character['event_ids'])} events.")

    # Save the updated registry
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=4)

    print(f"\n✨ Integration complete! Updated {registry_path}")

if __name__ == "__main__":
    integrate()

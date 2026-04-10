import json
import os
import sys
import re

# Ensure we can import from the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from llm import search_model, answer_model
from schemas import RelevantEvents
from langchain_core.prompts import ChatPromptTemplate

def load_events(file_name="events.json"):
    """Loads events from the JSON file located in the same directory as this script."""
    file_path = os.path.join(current_dir, file_name)
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    raise FileNotFoundError(f"{file_name} not found in {current_dir}. Please run main.py first.")

def find_relevant_event_ids(query, events):
    """Phase 1: Search - Identify relevant event IDs."""
    light_events = []
    for e in events:
        light_events.append({
            "event_id": e["event_id"],
            "summary": e["summary"],
            "characters": e["characters"]
        })
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a Search Assistant. Your task is to identify Event IDs relevant to a user query.\n"
            "Respond ONLY with the relevant Event IDs from the list provided.\n\n"
            "EVENT SUMMARIES:\n{summaries}"
        )),
        ("human", "{query}")
    ])
    
    try:
        structured_llm = search_model.with_structured_output(RelevantEvents)
        chain = prompt | structured_llm
        response = chain.invoke({
            "summaries": json.dumps(light_events, indent=2),
            "query": query
        })
        return response.event_ids
    except Exception as e:
        print(f"  ⚠️ Search fallback used.")
        chain = prompt | search_model
        raw_response = chain.invoke({
            "summaries": json.dumps(light_events, indent=2),
            "query": query
        }).content
        ids = re.findall(r"event_\d+", raw_response)
        return list(set(ids))

def generate_answer(query, relevant_ids, events):
    """Phase 2: Answer - Use the full descriptions."""
    selected_events = [e for e in events if e["event_id"] in relevant_ids]
    
    if not selected_events:
        return "I couldn't find enough specific details in the story events to answer that."
    
    context = ""
    for e in selected_events:
        context += f"Event Summary: {e['summary']}\nDetailed Description: {e['description']}\n\n"
        
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a precise Story Analyst. Answer the user's question using the provided context.\n"
            "CONTEXT:\n{context}"
        )),
        ("human", "{query}")
    ])
    
    chain = prompt | answer_model
    response = chain.invoke({"context": context, "query": query})
    return response.content

def main():
    try:
        events = load_events()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    print("\n" + "🚀" + " "*2 + "STORY QUERY ENGINE")
    print("-" * 40)
    
    while True:
        try:
            query = input("\n💬 Ask anything (or 'exit'): ").strip()
            if query.lower() == 'exit': break
            if not query: continue

            print("🔍 Searching...")
            relevant_ids = find_relevant_event_ids(query, events)
            
            if not relevant_ids:
                print("🤷 No matching events found.")
                continue
                
            print(f"📍 Context: {len(relevant_ids)} events found. Reading details...")
            answer = generate_answer(query, relevant_ids, events)
            print(f"\n💡 [ANSWER]:\n{answer}")
            print("\n" + "-"*40)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

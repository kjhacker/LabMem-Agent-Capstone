import os
import json
import datetime
import google.generativeai as genai
from typing import List, Optional
from dataclasses import dataclass

# --- 1. CONFIGURATION & SETUP ---
# CRITERIA: Technical Implementation - Setup
try:
    # 🚨 DO NOT PUT YOUR KEY HERE! The key must be set in PowerShell using $env:GEMINI_API_KEY
    genai.configure() 
except Exception:
    print("Warning: API Key not configured. Please set GEMINI_API_KEY.")
    
DB_FILE = "lab_memory.json"
model_name = 'gemini-2.5-flash' 

# The structured schema used by the Ingestion Agent (Context Engineering)
creation_schema_def = {
    "type": "OBJECT",
    "properties": {
        "user": {"type": "STRING"},
        "project": {"type": "STRING"},
        "screenID": {"type": "STRING"},
        "hypothesis": {"type": "STRING"},
        "protocol": {"type": "STRING"},
        "conditions": {"type": "STRING"},
        "results": {"type": "STRING"},
        "issues": {"type": "STRING"},
        "follow_ups": {"type": "STRING"},
        "tags": {"type": "ARRAY", "items": {"type": "STRING"}}
    },
    "required": ["user", "project", "results"]
}

# ----------------------------------------------------
# 2. THE PERSISTENCE LAYER (CUSTOM TOOLS)
# ----------------------------------------------------

def save_to_memory(data_dict):
    """Custom Tool: Saves the structured note to a JSON file (our DB)."""
    data_dict["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            try:
                if os.path.getsize(DB_FILE) > 0:
                    memory = json.load(f)
                else:
                    memory = []
            except:
                memory = []
    else:
        memory = []

    memory.append(data_dict)
    
    with open(DB_FILE, 'w') as f:
        json.dump(memory, f, indent=4)
    return f"Note successfully saved to Lab Memory. Total entries: {len(memory)}"

def search_memory(query=""):
    """Custom Tool: Reads the entire JSON file contents for the Retrieval Agent's context."""
    if not os.path.exists(DB_FILE) or os.path.getsize(DB_FILE) == 0:
        return "Memory is empty."
    with open(DB_FILE, 'r') as f:
        return f.read()

# ----------------------------------------------------
# 3. THE AGENTS (Multi-Agent System)
# ----------------------------------------------------

def IngestionAgent(raw_text, creation_schema):
    """
    AGENT 1 (IngestionAgent): Responsible for data normalization.
    """
    print("\n[IngestionAgent] Working...")
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""
    You are a strict Data Normalization Agent for a lab. 
    Extract information from the raw lab note below into the specified JSON schema.
    If a field is missing, use "N/A".
    
    Raw Text: {raw_text}
    """
    response = model.generate_content(
        contents=prompt,
        generation_config=genai.types.GenerationConfig(
            # CRITERIA: Context Engineering - Enforcing Structured Output
            response_mime_type="application/json",
            response_schema=creation_schema
        )
    )
    
    try:
        structured_data = json.loads(response.text)
        print(f"\n[IngestionAgent] Extracted Data:\n{json.dumps(structured_data, indent=2)}")
        
        save_result = save_to_memory(structured_data)
        print(f"[IngestionAgent] Tool Execution Result: {save_result}")
        return True
    except Exception as e:
        print(f"[IngestionAgent] ERROR: Failed to parse structured data. {e}")
        return False


def RetrievalAgent():
    """
    AGENT 2 (RetrievalAgent): Responsible for natural language querying and analysis.
    """
    print("\n[RetrievalAgent] Initializing session with Lab Memory context...")
    
    # 1. Fetch ALL lab notes to populate agent context
    all_notes_context = search_memory("") 
    
    # Define the system prompt
    system_prompt = f"""
        You are a helpful and concise Lab Assistant. 
        Your task is to answer user questions about lab activities by synthesizing information 
        from the provided Lab Notes Database below. Maintain conversation history.
        
        Lab Notes Database:
        {all_notes_context}
        """

    # CRITERIA: Sessions & Memory - State Management (chat history)
    # FINAL FIX: Pass system_instruction directly into GenerativeModel initialization.
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_prompt  # PASSED HERE, NOT IN CONFIG
    )
    
    # Start a chat session (memory enabled)
    chat = model.start_chat()

    print("🤖 Lab Assistant ready. Ask me a question about your experiments.")
    print(" (Type 'back' to return to main menu.)")

    while True:
        query = input("Ask Memory: ")
        if query.lower() == 'back':
            print("[RetrievalAgent] Session ended.")
            break
        
        response = chat.send_message(query)
        print(f"\n🤖 Agent: {response.text}")


# ----------------------------------------------------
# 4. THE ORCHESTRATOR
# CRITERIA: Architecture - Sequential Multi-Agent Flow
# ----------------------------------------------------

def run_lab_agent():
    """The main control loop that orchestrates the flow between the two Agents."""
    print("🧪 Lab Memory Agent System Initialized (Sequential Multi-Agent Mode)...")
    
    while True:
        print("\n--- LabMem Orchestrator ---")
        print("Options: [1] RUN IngestionAgent  [2] RUN RetrievalAgent  [3] Exit")
        choice = input("Select option: ")

        if choice == "1":
            raw_text = input("Paste your raw lab note here:\n")
            IngestionAgent(raw_text, creation_schema_def)

        elif choice == "2":
            RetrievalAgent()

        elif choice == "3":
            print("Shutting down LabMem...")
            break

# --- RUN APP ---
if __name__ == "__main__":
    run_lab_agent()
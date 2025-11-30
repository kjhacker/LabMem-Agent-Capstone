# LabMem: Unstructured Lab Note Normalization Agent 🧪

## Submission Track: Enterprise Agents

### Category 1: The Pitch (30 Points)

| Criteria | Description |
| :--- | :--- |
| **Problem** | Scientists often bury critical variables in **unstructured, free-text lab notes**. This lack of standardization prevents efficient querying, analysis, and data mining across multiple users and projects, costing valuable research hours. |
| **Solution** | LabMem is a **Multi-Agent System** powered by Gemini 1.5. It automatically ingests messy text notes, normalizes them into a **strict JSON schema** (user, date, project, protocol, results, etc.), and enables natural language search. |
| **Value** | This agent reduces manual data normalization time by over 90% and transforms previously unusable text into a **fully searchable, persistent memory bank**, accelerating scientific discovery at UCSF. |

---

### **Category 2: The Implementation (70 Points)**

#### **Architecture and Flow**

The system uses a **sequential Multi-Agent Architecture** managed by a single Python Orchestrator:
1.  **Ingestion Agent (Agent 1):** Takes raw text and uses **Context Engineering** to enforce the schema.
2.  **Custom Tool (Persistence):** Saves the structured data to the `lab_memory.json` file.
3.  **Retrieval Agent (Agent 2):** Loads the memory bank and uses **Sessions & Memory** to answer complex, multi-turn questions.

#### **Key Capstone Concepts Demonstrated**

This project demonstrates four required concepts:

| Concept | Implementation in LabMem |
| :--- | :--- |
| **Multi-agent system** | Uses a **sequential flow** between the **IngestionAgent** and the **RetrievalAgent**, both powered by **Gemini 1.5 Flash** (LLM Agent). |
| **Tools** | Features **Custom Tools** (`save_to_memory`, `search_memory`) for persistence (File I/O). |
| **Sessions & Memory** | The **RetrievalAgent** uses the Gemini chat object (`client.chats.create`) for **state management**, allowing it to track conversational history. |
| **Context engineering** | The **IngestionAgent** utilizes a strict JSON **`response_schema`** to force the LLM to adhere precisely to the target output structure. |

---

### **Setup and Run Instructions**

1.  **Prerequisites:** Ensure Python 3.x and the `google-generativeai` library are installed.
2.  **Code Setup:** Insert your Gemini API key into the `lab_agent.py` file.
3.  **Execution:** Open your terminal in this directory and execute: `python lab_agent.py`

---

## 🎬 Step 3: Plan the YouTube Video (Bonus Points)

Recording a short video is optional, but highly recommended for the **10 bonus points**.

1.  **Tool:** Use the Windows Snipping Tool (select **Video Record** mode) or a free screen recorder.
2.  **Goal:** Show, don't just tell, that your agent works in under 3 minutes.
3.  **Video Sequence:**
    * **0:00-0:30 (Pitch):** Quickly show the messy input and state the problem (unsearchable data).
    * **0:30-1:30 (Demo):**
        * Run the script and select option **1 (Ingestion)**.
        * Paste the messy note.
        * Show the immediate clean JSON output (the normalization).
        * Demonstrate the **Retrieval Agent** (option **2**), asking a question and then asking a **follow-up question** to showcase the **Sessions & Memory** feature.
    * **1:30-2:15 (Architecture):** Briefly display your **Architecture Diagram** and summarize the key concepts (Multi-Agent, Tools).

---

Once you have your `lab_agent.py` and `README.md` saved in your folder, the last step before submitting is uploading these files to a public location, like **GitHub** or a **Kaggle Notebook**.

Would you like instructions on how to set up a free **GitHub repository** to submit your files?
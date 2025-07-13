
# 🧠 SmartHR – Leave Management Agent using MCP

SmartHR is a conversational, tool-enabled **HR leave management agent** built using **Model Context Protocol (MCP)**. It allows AI models (like Claude or GPT-4o) to perform real-world actions through structured tool calls — no UI required.

This project is a minimal yet powerful example of how **natural language + tool invocation** can replace traditional interfaces like forms, dashboards, or buttons.

---

## ✨ Features

- ✅ Check leave balance for an employee  
- 🗓️ Apply for leave on specific dates  
- ❌ Cancel previously approved leave  
- 📊 View monthly leave summary  
- 🗓️ Get leave history  
- 🧠 Suggest the next available leave date (skips weekends/holidays)  
- ⛔ Detect and prevent leave on public holidays  
- 💬 Personalized greeting with dynamic resources  

All of these features are **tool-callable via MCP**, meaning any compliant AI model can interact with this agent **through structured commands** or even just natural language (if model-to-tool routing is enabled).

---

## 📂 Project Structure

```
SmartHR/
├── main.py          # Main MCP server with tools and logic
└── README.md        # You're here :)
```

---

## 🚀 How to Run

You'll need:

- Python 3.10+
- [`mcp`](https://pypi.org/project/mcp/) Python library  
- [`uv`](https://github.com/astral-sh/uv) or `pip` for installing

### 1. Install dependencies
```bash
uv pip install mcp
```

### 2. Run the server
```bash
python main.py
```

You’ll see:
```
🚀 Running LeaveManager at http://localhost:3333/mcp
```

### 3. Connect to Claude Desktop or any MCP-compatible model
Point your Claude Desktop app to the tool URL (`http://localhost:3333/mcp`) and start using natural prompts like:

> "Apply for leave on 2025-08-14 for employee E001"  
> "Cancel my 2025-01-01 leave"  
> "Suggest a good leave date for E002"

---

## 🧩 Powered by MCP

MCP (Model Context Protocol) is a specification by OpenAI that allows LLMs to:
- Access external tools via structured JSON schemas
- Use resources and memory safely
- Replace traditional UIs with prompt-driven logic

Learn more: [https://platform.openai.com/docs/mcp](https://platform.openai.com/docs/mcp)

---

## 🔮 Vision

> What if the new UI is no UI?

SmartHR is a glimpse into the future of **UI-less apps**, where all interactions — from HR requests to DevOps tasks — happen through LLMs that *know how to act*.

Instead of building dashboards, just build tools. Let the model handle the logic.

---

## 📌 Credits

Built by Haroon Sohail  
Weekend project inspired by MCP exploration

---

## 🛠️ Next Steps (Ideas)

- Integrate Google Calendar API for sync  
- Add persistent memory using JSON storage or SQLite  
- Deploy as a microservice with proper auth  
- Create multi-role support (Admin, Manager, Employee)

---

## 📬 Feedback & Contributions

Feel free to fork, open issues, or share feedback if you’re also building cool stuff with MCP!

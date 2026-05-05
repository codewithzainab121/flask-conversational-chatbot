# 🍕 Cheezious Chatbot — Step-by-Step Guide

## Project Structure
```
cheezious_chatbot/
│
├── app.py              ← Python Flask backend (brain of chatbot)
├── requirements.txt    ← Python packages needed
└── static/
    └── index.html      ← Frontend UI (HTML + CSS + JS)
```

---

## STEP 1 — Install Python & VS Code

1. Download Python from: https://www.python.org/downloads/
2. During install → ✅ CHECK "Add Python to PATH"
3. Download VS Code from: https://code.visualstudio.com/

---

## STEP 2 — Open Project in VS Code

1. Create a folder: `cheezious_chatbot`
2. Inside it, create another folder: `static`
3. Place files:
   - `app.py` → inside `cheezious_chatbot/`
   - `requirements.txt` → inside `cheezious_chatbot/`
   - `index.html` → inside `cheezious_chatbot/static/`

---

## STEP 3 — Install Flask

Open Terminal in VS Code (Ctrl + `)

```bash
python -m venv venv
venv\Scripts\activate
pip install flask
```

---

## STEP 4 — Run the Chatbot

In VS Code terminal, make sure you're in the project folder:

```bash
cd cheezious_chatbot
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

---

## STEP 5 — Open in Browser

Open your browser and go to:
```
http://localhost:5000
```

Your chatbot is LIVE! 🎉

---

## How the Chatbot Works (For Teaching)

### Rule-Based Logic (app.py)
```
User Message → detect_intent() → match keywords → return response
```

### Intent Detection (Simple Rules):
| User says...        | Intent detected |
|---------------------|-----------------|
| "hi", "hello"       | greeting        |
| "menu", "food"      | show_menu       |
| "suggest", "best"   | suggest         |
| "2", "4 people"     | people_count    |
| "order"             | order           |
| "bye"               | bye             |

### Conversation Flow:
```
1. Bot asks name
2. User gives name → saved in session
3. Bot greets with name
4. User asks menu → menu shown
5. User says how many people → meal suggested
```

### Session (Memory):
```python
session = {
    "stage": "chat",        # where in conversation
    "name": "Ahmed",        # user's name
    "people_count": 4       # group size
}
```
This is sent back and forth between frontend and backend
with every message — this is how the bot "remembers"!

---

## Adding to a Website Later

Just copy the `static/index.html` content into your website.
Change the fetch URL from `/api/chat` to your deployed backend URL.

---

## Free Tools Used:
- **Flask** — Python web framework (free, open source)
- **Vanilla JS** — No paid libraries
- **Google Fonts** — Free fonts
- Everything runs 100% locally on your machine!

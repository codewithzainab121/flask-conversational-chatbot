from flask import Flask, request, jsonify, send_from_directory
import re
import os

app = Flask(__name__, static_folder='static')

# ─────────────────────────────────────────
#  CHEEZIOUS MENU DATA
# ─────────────────────────────────────────
MENU = {
    "Burgers": [
        {"name": "Classic Beef Burger",       "price": 450,  "serves": 1},
        {"name": "Zinger Burger",             "price": 550,  "serves": 1},
        {"name": "Double Decker Burger",      "price": 699,  "serves": 1},
        {"name": "Crispy Chicken Burger",     "price": 499,  "serves": 1},
        {"name": "BBQ Smoky Burger",          "price": 620,  "serves": 1},
    ],
    "Pizzas": [
        {"name": "Margherita Pizza (Medium)", "price": 999,  "serves": 2},
        {"name": "BBQ Chicken Pizza (Medium)","price": 1199, "serves": 2},
        {"name": "Mighty Meat Pizza (Large)", "price": 1799, "serves": 4},
        {"name": "Veggie Supreme (Medium)",   "price": 1099, "serves": 2},
        {"name": "Cheezious Special (Large)", "price": 1999, "serves": 4},
    ],
    "Sides & Snacks": [
        {"name": "Loaded Fries",              "price": 349,  "serves": 1},
        {"name": "Chicken Nuggets (6 pcs)",   "price": 399,  "serves": 1},
        {"name": "Onion Rings",               "price": 299,  "serves": 1},
        {"name": "Coleslaw",                  "price": 199,  "serves": 1},
        {"name": "Garlic Bread",              "price": 249,  "serves": 1},
    ],
    "Deals & Meals": [
        {"name": "Solo Deal (1 person)",      "price": 799,  "serves": 1},
        {"name": "Duo Deal (2 persons)",      "price": 1399, "serves": 2},
        {"name": "Family Deal (4 persons)",   "price": 2499, "serves": 4},
        {"name": "Party Deal (6 persons)",    "price": 3799, "serves": 6},
        {"name": "Mega Party (10 persons)",   "price": 5999, "serves": 10},
    ],
    "Drinks": [
        {"name": "Soft Drink (Regular)",      "price": 150,  "serves": 1},
        {"name": "Soft Drink (Large)",        "price": 199,  "serves": 1},
        {"name": "Fresh Juice",               "price": 249,  "serves": 1},
        {"name": "Mineral Water",             "price": 100,  "serves": 1},
    ],
}

# ─────────────────────────────────────────
#  RULE-BASED INTENT DETECTION
# ─────────────────────────────────────────
def detect_intent(message: str) -> str:
    msg = message.lower().strip()

    greeting_words   = ["hi", "hello", "hey", "salam", "assalam", "good morning",
                        "good evening", "good afternoon", "howdy"]
    menu_words       = ["menu", "food", "items", "what do you have", "what do you serve",
                        "show menu", "see menu", "view menu", "options", "dishes",
                        "what can i order", "what's available"]
    order_words      = ["order", "want", "like to have", "give me", "i'll have",
                        "can i get", "i want"]
    people_words     = ["people", "persons", "of us", "members", "how many",
                        "group", "family", "friends", "guests"]
    suggest_words    = ["suggest", "recommendation", "recommend", "what should",
                        "best for", "suitable", "good for"]
    thanks_words     = ["thank", "thanks", "thankyou", "thank you", "great", "awesome",
                        "perfect", "wonderful"]
    bye_words        = ["bye", "goodbye", "see you", "take care", "later", "quit", "exit"]
    help_words       = ["help", "assist", "support", "what can you do", "how does this work"]
    hours_words      = ["timing", "hours", "open", "close", "when", "schedule"]
    location_words   = ["location", "address", "where", "branch", "outlet"]
    price_words      = ["price", "cost", "how much", "rate", "charges", "expensive", "cheap"]

    if any(w in msg for w in bye_words):         return "bye"
    if any(w in msg for w in thanks_words):      return "thanks"
    if any(w in msg for w in greeting_words):    return "greeting"
    if any(w in msg for w in menu_words):        return "show_menu"
    if any(w in msg for w in suggest_words):     return "suggest"
    if any(w in msg for w in people_words):      return "people_count"
    if any(w in msg for w in order_words):       return "order"
    if any(w in msg for w in help_words):        return "help"
    if any(w in msg for w in hours_words):       return "hours"
    if any(w in msg for w in location_words):    return "location"
    if any(w in msg for w in price_words):       return "price_query"

    # Try to extract a standalone number (people count)
    if re.search(r'\b([1-9]|1[0-9]|20)\b', msg):
        return "people_count"

    return "unknown"


def extract_number(message: str) -> int | None:
    """Extract first integer from message."""
    match = re.search(r'\b(\d+)\b', message)
    return int(match.group(1)) if match else None


def suggest_meals(count: int) -> dict:
    """Return meal suggestions based on group size."""
    if count == 1:
        return {
            "title": "Perfect for 1 Person 🧑",
            "suggestions": [
                "Solo Deal — Rs. 799 (best value!)",
                "Zinger Burger + Loaded Fries + Soft Drink",
                "Classic Beef Burger + Onion Rings",
            ],
            "tip": "The Solo Deal is your best bet — burger, fries & drink all included! 🎯"
        }
    elif count == 2:
        return {
            "title": "Great for 2 People 👫",
            "suggestions": [
                "Duo Deal — Rs. 1,399 (best value!)",
                "Margherita Pizza (Medium) + 2 Soft Drinks",
                "2× Zinger Burgers + Loaded Fries to share",
            ],
            "tip": "The Duo Deal saves you money and comes with everything you need! 💑"
        }
    elif count <= 4:
        return {
            "title": f"Perfect for {count} People 👨‍👩‍👧‍👦",
            "suggestions": [
                "Family Deal — Rs. 2,499 (best value!)",
                "Mighty Meat Pizza (Large) + Sides + 4 Drinks",
                "Cheezious Special Pizza + Nuggets + Garlic Bread",
            ],
            "tip": "Family Deal is amazing value — feeds 4 with pizzas, sides & drinks! 🍕"
        }
    elif count <= 6:
        return {
            "title": f"Awesome for {count} People 🎉",
            "suggestions": [
                "Party Deal — Rs. 3,799 (best value!)",
                "2× Large Pizzas + Sides + 6 Drinks",
                "Mix of burgers + 2 pizzas + loaded fries",
            ],
            "tip": "Party Deal is your go-to — everything sorted for the whole crew! 🥳"
        }
    else:
        return {
            "title": f"Big Group of {count} People 🎊",
            "suggestions": [
                "Mega Party Deal — Rs. 5,999 (serves 10!)",
                "Multiple Party Deals combined",
                "Custom order: 3× Large Pizzas + Deals + Sides",
            ],
            "tip": f"For {count} people, go with Mega Party Deal + extra items. Call us for bulk orders! 📞"
        }


def format_menu() -> dict:
    """Return structured menu for frontend rendering."""
    return MENU


# ─────────────────────────────────────────
#  CONVERSATION ENGINE
# ─────────────────────────────────────────
def get_response(user_message: str, session: dict) -> tuple[str, dict]:
    """
    Core rule-based conversation engine.
    session keys: stage, name, people_count
    Returns (bot_reply_text, updated_session)
    """
    intent = detect_intent(user_message)
    name   = session.get("name", "")
    stage  = session.get("stage", "ask_name")

    # ── STAGE 1: Ask name ──────────────────────────────────────────────────
    if stage == "ask_name":
        # Accept any non-empty input as name
        raw = user_message.strip()
        if len(raw) < 1 or len(raw) > 40:
            return ("Please tell me your name so I can assist you better! 😊", session)

        name = raw.title()
        session["name"]  = name
        session["stage"] = "chat"
        reply = (
            f"Welcome to Cheezious, **{name}**! 🎉🍕\n\n"
            f"I'm Cheezi, your personal food assistant! I'm here to help you with:\n"
            f"• 📋 View our full menu\n"
            f"• 🍔 Get meal suggestions for your group\n"
            f"• 📍 Find our locations\n"
            f"• ⏰ Check our timings\n\n"
            f"What can I do for you today, **{name}**?"
        )
        return (reply, session)

    # ── STAGE 2: Main chat ─────────────────────────────────────────────────
    addr   = f", **{name}**" if name else ""

    if intent == "greeting":
        return (f"Hey{addr}! 👋 Great to hear from you again! How can I help you today?", session)

    if intent == "show_menu":
        session["stage"] = "menu_shown"
        reply = (
            f"Here's our full menu{addr}! 🍕🍔\n\n"
            f"__MENU__\n\n"
            f"How many people are you ordering for? I'll suggest the best deal for you! 👥"
        )
        return (reply, session)

    if intent == "people_count":
        count = extract_number(user_message)
        if count is None or count < 1:
            return (f"How many people are ordering{addr}? Just tell me the number! 😊", session)
        if count > 50:
            return (f"Wow, that's a big party{addr}! 🎊 For groups over 50, please call us directly for a custom catering order. Our number: **042-111-222-444**", session)

        session["people_count"] = count
        suggestion = suggest_meals(count)
        session["stage"] = "suggested"

        lines = [f"**{suggestion['title']}**\n"]
        lines.append("Here are my top picks for you:\n")
        for i, s in enumerate(suggestion["suggestions"], 1):
            lines.append(f"**{i}.** {s}")
        lines.append(f"\n💡 *{suggestion['tip']}*")
        lines.append(f"\nWould you like to see the full menu or have any other questions{addr}?")
        return ("\n".join(lines), session)

    if intent == "suggest":
        count = session.get("people_count")
        if count is None:
            return (f"Sure{addr}! First, tell me — how many people are you ordering for? 👥", session)
        suggestion = suggest_meals(count)
        lines = [f"**{suggestion['title']}**\n"]
        for i, s in enumerate(suggestion["suggestions"], 1):
            lines.append(f"**{i}.** {s}")
        lines.append(f"\n💡 *{suggestion['tip']}*")
        return ("\n".join(lines), session)

    if intent == "order":
        return (
            f"Great choice{addr}! 😍 You can place your order:\n\n"
            f"📱 **Call us:** 042-111-222-444\n"
            f"🌐 **Website:** www.cheezious.com\n"
            f"🚗 **Drive-Thru** at any branch\n\n"
            f"Is there anything else I can help you with?"
        , session)

    if intent == "hours":
        return (
            f"Here are our timings{addr}! ⏰\n\n"
            f"🕙 **Opening:** 10:00 AM\n"
            f"🕚 **Closing:** 12:00 AM (Midnight)\n"
            f"📅 **Days:** Open 7 days a week!\n\n"
            f"We're always ready to serve you! 🍕"
        , session)

    if intent == "location":
        return (
            f"We have multiple branches{addr}! 📍\n\n"
            f"🏬 **Lahore** — DHA, Gulberg, Johar Town, Model Town\n"
            f"🏬 **Islamabad** — F-7, F-10, Blue Area\n"
            f"🏬 **Karachi** — Clifton, Defence, Gulshan\n\n"
            f"Find the nearest branch at **www.cheezious.com/locations** 🗺️"
        , session)

    if intent == "price_query":
        return (
            f"Our prices are very affordable{addr}! 💰\n\n"
            f"🍔 Burgers start from **Rs. 450**\n"
            f"🍕 Pizzas start from **Rs. 999**\n"
            f"🤝 Deals start from **Rs. 799**\n\n"
            f"Type **menu** to see all items with prices! 📋"
        , session)

    if intent == "thanks":
        return (f"You're most welcome{addr}! 😊 Enjoy your meal! 🍕 Is there anything else I can help you with?", session)

    if intent == "bye":
        session["stage"] = "ask_name"
        session["name"]  = ""
        return (f"Thank you for visiting Cheezious{addr}! 👋\nHope to see you again soon! 🍕❤️\n\n*(Session ended — refresh to start over)*", session)

    if intent == "help":
        return (
            f"I can help you with{addr}:\n\n"
            f"📋 **menu** — View our full menu\n"
            f"🍽️ **suggest** — Get meal recommendations\n"
            f"📍 **location** — Find our branches\n"
            f"⏰ **timings** — Our opening hours\n"
            f"💰 **prices** — Check price range\n"
            f"📞 **order** — How to place an order\n\n"
            f"Just type what you need!"
        , session)

    # Fallback
    return (
        f"I'm not sure I understood that{addr} 🤔\n\n"
        f"Try asking about our **menu**, **deals**, **location**, or **timings**!\n"
        f"Or type **help** to see what I can do. 😊"
    , session)


# ─────────────────────────────────────────
#  FLASK ROUTES
# ─────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data    = request.get_json()
    message = data.get('message', '').strip()
    session = data.get('session', {"stage": "ask_name", "name": "", "people_count": None})

    if not message:
        return jsonify({"error": "Empty message"}), 400

    reply, updated_session = get_response(message, session)

    return jsonify({
        "reply":   reply,
        "session": updated_session,
        "menu":    format_menu() if "__MENU__" in reply else None,
        "reply":   reply.replace("__MENU__", ""),
    })

@app.route('/api/menu', methods=['GET'])
def get_menu():
    return jsonify(format_menu())

if __name__ == '__main__':
    app.run(debug=True, port=5000)

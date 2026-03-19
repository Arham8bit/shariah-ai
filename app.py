from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# ── Groq free API key — get yours at console.groq.com ──
client = Groq(api_key="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")

SYSTEM_PROMPT = """You are an expert Islamic Finance advisor with deep knowledge of Shariah law as it applies to financial matters.

You help users understand:
- Halal vs Haram financial products
- Riba (interest) and how to avoid it
- Zakat calculations and obligations
- Murabaha, Mudarabah, Ijara, and other Islamic contracts
- Shariah-compliant investing and screening
- Islamic banking products

Rules:
- Always cite relevant Islamic principles or scholarly consensus when possible
- Be clear when something is disputed among scholars (give both views)
- Do not give personal financial advice — guide based on Islamic principles only
- Keep answers clear, helpful, and respectful
- If unsure, say so honestly and recommend consulting a qualified scholar"""


# ── Page Routes ──────────────────────────────────────

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat")
def chat_page():
    return render_template("chat.html")

@app.route("/solutions")
def solutions():
    return render_template("solutions.html")

@app.route("/technology")
def technology():
    return render_template("technology.html")

@app.route("/case-studies")
def case_studies():
    return render_template("case_studies.html")

@app.route("/partners")
def partners():
    return render_template("partners.html")

@app.route("/whitepaper")
def whitepaper():
    return render_template("whitepaper.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


# ── AI Chat API ───────────────────────────────────────

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # Free, fast, high quality
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print("GROQ ERROR:", str(e))   # Shows error in terminal
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
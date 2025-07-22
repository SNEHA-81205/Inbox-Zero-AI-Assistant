# main.py
import os
import json
from flask import Flask, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct")

def analyze_email(email):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are an AI email assistant. Analyze the following email and return a JSON with these keys:
- "summary": a short summary of the email
- "urgency": High, Medium, or Low
- "action": Keep or Delete

Email content:
Subject: {email.get("subject", "")}
From: {email.get("from", "")}
Body: {email.get("body", "")}
"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        data = res.json()
        if res.status_code == 200:
            reply_text = data["choices"][0]["message"]["content"]
            return json.loads(reply_text)
        else:
            return {"summary": "Could not analyze", "urgency": "Low", "action": "Keep"}
    except Exception:
        return {"summary": "Error analyzing", "urgency": "Low", "action": "Keep"}

@app.route("/api/inbox", methods=["GET"])
def inbox():
    try:
        with open("mock_emails.json", "r") as f:
            emails = json.load(f)

        analyzed_emails = []
        for i, email in enumerate(emails):
            result = analyze_email(email)
            email.update(result)
            email["id"] = i  # Add ID for React key
            analyzed_emails.append(email)

        # Sort by urgency: High > Medium > Low
        priority = {"High": 1, "Medium": 2, "Low": 3}
        analyzed_emails.sort(key=lambda x: priority.get(x.get("urgency", "Low"), 3))

        return jsonify(analyzed_emails)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Required for Render
    app.run(host="0.0.0.0", port=port, debug=True)


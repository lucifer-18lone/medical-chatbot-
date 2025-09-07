from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()
    
    if not user_message:
        return jsonify({"reply": "Please enter a message."})
    
    try:
        # Generate response from Gemini
        response = model.generate_content(user_message)
        reply = response.text.strip() if response.text else "I couldn't generate a response."
    except Exception as e:
        reply = "Sorry, I cannot respond right now."
        print("Error:", e)
    
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

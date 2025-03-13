import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# Configure Gemini API Key
GEMINI_API_KEY = "AIzaSyDn5pMPS7uBYp5IUR4vCuF45qfbHJPvv-A"
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app)

def generate_gemini_response(user_query):
    prompt = f"""
    You are an AI assistant using Gemini 2.0 Flash. Provide a concise, clear, and helpful response to the user query. 
    Keep replies engaging, respectful, and use emojis when appropriate. 

    User Query: {user_query}

    Response:
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # Updated Model
        response = model.generate_content(prompt)

        return response.text if hasattr(response, "text") else "No response from Gemini API."

    except Exception as e:
        print(f"Error generating response: {e}")
        return "An error occurred while processing your request."

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        if not data or "query" not in data:
            return jsonify({"response": "Invalid request!"}), 400

        user_query = data["query"]
        print(f"Received query: {user_query}")

        final_response = generate_gemini_response(user_query)

        return jsonify({"response": final_response})

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"response": "Server error!"}), 500

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template
import datetime
import os
from groq import Groq
app = Flask(__name__)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
@app.route('/')
def hello():
    return render_template(r'index.html', utc_dt=datetime.datetime.utcnow())

def get_llama_response(user_message):
    
    chat_completion = client.chat.completions.create(
    messages= [{"role": "user", "content": user_message}],
    model="llama-3.3-70b-versatile")
    reposnse = chat_completion.choices[0].message.content
    print(f"message response: {reposnse}")
    return reposnse

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response = get_llama_response(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)


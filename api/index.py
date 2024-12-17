import random
from transformers import pipeline
from flask import Flask, jsonify, request

# Initialize necessary tools
advice_generator = pipeline("text-generation", model="gpt2")

# Sample predefined advice (expand this as needed)
advice_db = {
    "communication": [
        "Effective communication is key in any relationship. Make sure you're always listening actively.",
        "Don't be afraid to express your feelings. Honest communication can resolve many issues.",
        "It's important to listen with empathy and avoid interrupting your partner during discussions."
    ],
    "trust": [
        "Trust is the foundation of any strong relationship. Without it, it's hard to build a lasting bond.",
        "If trust has been broken, rebuilding it takes time and consistent actions.",
        "Trust and transparency can make a relationship much stronger."
    ],
    "love": [
        "Love is about caring for someone, respecting them, and being there through both good and bad times.",
        "True love is about growing together, supporting each other's dreams, and showing affection daily.",
        "Love is about compromise, respect, and trust."
    ]
}

# Function to check if the user's input expresses gratitude
def is_gratitude(user_input):
    gratitude_phrases = ['thanks', 'thank you', 'appreciate it', 'grateful', 'thanks a lot', 'many thanks']
    user_input = user_input.lower()
    return any(phrase in user_input for phrase in gratitude_phrases)

# Function to generate relationship advice using GPT-2
def generate_relationship_advice(user_input):
    if is_gratitude(user_input):
        return "You're welcome! I'm glad I could help. Feel free to reach out anytime if you need more advice. Take care!"

    prompt = f"Provide thoughtful, empathetic relationship advice for someone feeling: {user_input}. Offer actionable steps for improving the situation, focusing on clear communication, trust, and mutual understanding."
    generated = advice_generator(prompt, max_length=150, num_return_sequences=1, temperature=0.7)

    # Get the generated response
    advice = generated[0]['generated_text']
    
    # Strip off the initial prompt to avoid repeating it in the response
    start_index = advice.find("Provide thoughtful, empathetic relationship advice for someone feeling:")
    if start_index != -1:
        advice = advice[start_index + len("Provide thoughtful, empathetic relationship advice for someone feeling:"):].strip()

    # Trim incomplete or irrelevant responses (e.g., ending with "I'm")
    if advice.endswith("I'm") or advice.endswith("I"):
        advice = advice[:advice.rfind("I'm")].strip()

    # Return the cleaned-up advice
    return f"Here's some personalized advice: {advice}"

# Initialize Flask app
app = Flask(__name__)

# Handle the /chat endpoint for user interaction
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form['message']
    response = generate_relationship_advice(user_input)
    return jsonify({'response': response})

# Add the default endpoint to serve your HTML page
@app.route("/")
def home():
    with open("public/index.html") as f:
        return f.read()

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
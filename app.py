import random
import json
import torch
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

# Flask app initialization
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})  # Enable CORS for your API
#deploy
# Initialize the device and load model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"

# Function to get response
def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])

    return "I do not understand..."

# Route for the main page
@app.route("/")
def home():
    return render_template("base.html")

# Route for handling the chatbot response
@app.route("/api/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if user_message:
        bot_response = get_response(user_message)
        return jsonify({"response": bot_response})
    else:
        return jsonify({"response": "Please enter a valid message."})

if __name__ == "__main__":
    app.run(debug=True, port=5000)

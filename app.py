import json
import random
from flask import Flask, render_template, request, jsonify
import torch
from torch import nn

app = Flask(__name__)

# Load intents from the JSON file
with open("intents.json", "r") as file:
    intents = json.load(file)

# Example PyTorch model (Simple Feedforward Neural Network)
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc = nn.Linear(10, 1)

    def forward(self, x):
        return self.fc(x)

# Load or create your PyTorch model here
model = SimpleModel()

# Function to find a matching response
def get_custom_response(message):
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            if pattern in message.lower():
                return random.choice(intent["responses"])
    return random.choice([response for intent in intents["intents"] if intent["tag"] == "unknown" for response in intent["responses"]])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.json.get("message")
    response = get_custom_response(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

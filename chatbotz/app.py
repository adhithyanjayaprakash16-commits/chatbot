from flask import Flask, render_template, request, jsonify
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import random
from textblob import TextBlob

# PRO Feature Imports
from database import init_db, save_booking, log_query
from ticket_generator import create_pdf_ticket

app = Flask(__name__, template_folder='api/templates', static_folder='api/static')
lemmatizer = WordNetLemmatizer()
user_sessions = {}

# Initialize Database
init_db()

# Load model and data
try:
    intents = json.loads(open('intents.json').read())
    words = pickle.load(open('words.pkl', 'rb'))
    classes = pickle.load(open('classes.pkl', 'rb'))
    model = pickle.load(open('chatbot_model.pkl', 'rb'))
except Exception as e:
    print(f"Error loading model artifacts: {e}")

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence, model):
    p = bow(sentence, words)
    res = model.predict_proba([p])[0]
    ERROR_THRESHOLD = 0.30
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_response(ints, intents_json):
    tag = ints[0]['intent'] if ints else 'fallback'
    for i in intents_json['intents']:
        if i['tag'] == tag:
            return random.choice(i['responses']), tag
    return "I'm sorry, I didn't quite catch that.", 'fallback'

# Sentiment Analysis Utility
def get_sentiment_response(msg):
    analysis = TextBlob(msg)
    if analysis.sentiment.polarity < -0.4:
        return "I can see you're unhappy. I apologize for any convenience! Let me try to make this right."
    return None

# Simulation of "Live" Buses
AVAILABLE_BUSES = [
    {"name": "Adhii Express Premium", "time": "21:00", "type": "AC Sleeper", "fare": 850},
    {"name": "TN Royal Travels", "time": "22:15", "type": "Volvo Multi-Axle", "fare": 1100},
    {"name": "Green Line Budget", "time": "20:30", "type": "Non-AC Seater", "fare": 550}
]

# Robust Dialogue Management
def handle_dialogue(user_id, msg):
    # Sentiment Check
    sentiment_reply = get_sentiment_response(msg)
    
    ints = predict_class(msg, model)
    nlp_res, tag = get_response(ints, intents)
    
    # Store interaction in DB Log
    log_query(msg, nlp_res, tag)
    
    session = user_sessions.get(user_id, {"state": "NORMAL", "data": {}})
    
    # Context Switching: Allow FAQ mid-booking
    if session['state'] != "NORMAL" and tag not in ["bus_search", "fallback"]:
        return f"💡 **Info**: {nlp_res}\n\n---\nAnyway, I was asking: **{get_current_prompt(session['state'])}**"

    # State Machine
    if session['state'] == "NORMAL":
        if tag == "bus_search":
            session['state'] = "AWAIT_SOURCE"
            user_sessions[user_id] = session
            prefix = sentiment_reply + " " if sentiment_reply else ""
            return prefix + "Excited to help you travel! 🚌 Where are you starting from?"
        return (sentiment_reply + " " if sentiment_reply else "") + nlp_res

    if session['state'] == "AWAIT_SOURCE":
        session['data']['source'] = msg
        session['state'] = "AWAIT_DEST"
        user_sessions[user_id] = session
        return "Got it. And what is your destination city?"

    elif session['state'] == "AWAIT_DEST":
        session['data']['dest'] = msg
        session['state'] = "AWAIT_DATE"
        user_sessions[user_id] = session
        return f"Searching buses for {session['data']['source']} to {msg}... 🔍\nWhat is your travel date?"

    elif session['state'] == "AWAIT_DATE":
        session['data']['date'] = msg
        session['state'] = "AWAIT_BUS_SELECTION"
        user_sessions[user_id] = session
        
        bus_list = "\n".join([f"{i+1}. {b['name']} ({b['time']}) - Rs.{b['fare']}" for i, b in enumerate(AVAILABLE_BUSES)])
        return f"Here are available buses for {msg}:\n{bus_list}\n\nPlease enter 1, 2, or 3 to select."

    elif session['state'] == "AWAIT_BUS_SELECTION":
        idx = ''.join(filter(str.isdigit, msg))
        if not idx or int(idx) not in [1, 2, 3]:
            return "Please select a valid bus number (1, 2, or 3)."
        
        bus = AVAILABLE_BUSES[int(idx)-1]
        session['data']['bus'] = bus
        session['state'] = "AWAIT_PASSENGERS"
        user_sessions[user_id] = session
        return f"You selected {bus['name']}. How many passengers?"

    elif session['state'] == "AWAIT_PASSENGERS":
        count = ''.join(filter(str.isdigit, msg))
        if not count: return "How many people are going? Just type the number."
        session['data']['passengers'] = count
        total = int(count) * session['data']['bus']['fare']
        session['data']['total'] = total
        session['state'] = "AWAIT_CONFIRM"
        user_sessions[user_id] = session
        
        return f"📋 **Summary**\nBus: {session['data']['bus'] ['name']}\nDate: {session['data']['date']}\nPassengers: {count}\nTotal: Rs.{total}\n\nType 'Confirm' to finalize!"

    elif session['state'] == "AWAIT_CONFIRM":
        if "confirm" in msg.lower() or "yes" in msg.lower():
            pnr = "ADH" + str(random.randint(10000, 99999))
            
            # Save to Database
            save_booking(pnr, session['data']['source'], session['data']['dest'], session['data']['date'], session['data']['passengers'], session['data']['total'])
            
            # Generate PDF Ticket
            pdf_url = create_pdf_ticket(pnr, session['data']['source'], session['data']['dest'], session['data']['date'], session['data']['passengers'], session['data']['total'])
            
            user_sessions[user_id] = {"state": "NORMAL", "data": {}}
            return f"✅ **Confirmed!** Your PNR is {pnr}.\n\n📥 **Download your ticket here:** [Click to Download Ticket]({pdf_url})\n\nSafe and happy journey!"
        else:
            user_sessions[user_id] = {"state": "NORMAL", "data": {}}
            return "No problem, session reset. How else can I help?"

    return nlp_res

def get_current_prompt(state):
    prompts = {
        "AWAIT_SOURCE": "Where are you starting from?",
        "AWAIT_DEST": "Where do you want to go?",
        "AWAIT_DATE": "What is the travel date?",
        "AWAIT_BUS_SELECTION": "Choose a bus (1, 2, or 3).",
        "AWAIT_PASSENGERS": "How many passengers?",
        "AWAIT_CONFIRM": "Write 'Confirm' to pay."
    }
    return prompts.get(state, "How can I help?")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]
    res = handle_dialogue("demo_user", msg)
    return jsonify({"response": res})

if __name__ == "__main__":
    app.run(debug=True, port=5000)

import os
from flask import Flask, render_template, request, jsonify
import json
import pickle
import numpy as np
import nltk
import random
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer

# Vercel-specific: Download NLTK data to /tmp
import nltk
nltk.data.path.append("/tmp")
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', download_dir='/tmp')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', download_dir='/tmp')

# PRO Feature Imports
from database import init_db, save_booking, log_query
from ticket_generator import create_pdf_ticket

# Load model and data with local paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

app = Flask(__name__, 
            template_folder=os.path.join(ROOT_DIR, 'templates'), 
            static_folder=os.path.join(ROOT_DIR, 'static'))
lemmatizer = WordNetLemmatizer()
user_sessions = {}

# Initialize Database (Wrapped for Vercel)
try:
    init_db()
except Exception as e:
    print(f"Database init skipped (Read-only filesystem): {e}")


def load_file(filename, mode='rb'):
    # Try parent directory (root) first, then current directory (api/)
    paths_to_check = [
        os.path.join(ROOT_DIR, filename),
        os.path.join(BASE_DIR, filename),
        filename
    ]
    for path in paths_to_check:
        if os.path.exists(path):
            with open(path, mode) as f:
                if filename.endswith('.json'):
                    return json.load(f)
                return pickle.load(f)
    raise FileNotFoundError(f"Could not find {filename}")

try:
    intents = load_file('intents.json', 'r')
    words = load_file('words.pkl')
    classes = load_file('classes.pkl')
    model = load_file('chatbot_model.pkl')
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

def get_sentiment_response(msg):
    analysis = TextBlob(msg)
    if analysis.sentiment.polarity < -0.4:
        return "I can see you're unhappy. I apologize for any convenience! Let me try to make this right."
    return None

AVAILABLE_BUSES = [
    {"name": "Adhii Express Premium", "time": "21:00", "type": "AC Sleeper", "fare": 850},
    {"name": "TN Royal Travels", "time": "22:15", "type": "Volvo Multi-Axle", "fare": 1100},
    {"name": "Green Line Budget", "time": "20:30", "type": "Non-AC Seater", "fare": 550}
]

def handle_dialogue(user_id, msg):
    sentiment_reply = get_sentiment_response(msg)
    ints = predict_class(msg, model)
    nlp_res, tag = get_response(ints, intents)
    
    try:
        log_query(msg, nlp_res, tag)
    except:
        pass
        
    session = user_sessions.get(user_id, {"state": "NORMAL", "data": {}})
    
    if session['state'] != "NORMAL" and tag not in ["bus_search", "fallback"]:
        return f"💡 **Info**: {nlp_res}\n\n---\nAnyway, I was asking: **{get_current_prompt(session['state'])}**"

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
            pdf_url = "#"
            try:
                save_booking(pnr, session['data']['source'], session['data']['dest'], session['data']['date'], session['data']['passengers'], session['data']['total'])
                pdf_url = create_pdf_ticket(pnr, session['data']['source'], session['data']['dest'], session['data']['date'], session['data']['passengers'], session['data']['total'])
            except Exception as e:
                print(f"Booking save/PDF error: {e}")
            
            user_sessions[user_id] = {"state": "NORMAL", "data": {}}
            ticket_msg = f"✅ **Confirmed!** Your PNR is {pnr}."
            if pdf_url != "#":
                ticket_msg += f"\n\n📥 **Download your ticket here:** [Click to Download Ticket]({pdf_url})"
            ticket_msg += "\n\nSafe and happy journey!"
            return ticket_msg
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
    try:
        msg = request.form["msg"]
        res = handle_dialogue("demo_user", msg)
        return jsonify({"response": res})
    except Exception as e:
        print(f"Error in chatbot_response: {e}")
        return jsonify({"response": "I'm having a technical glitch. Please try again later!"}), 500

@app.route("/download_ticket/<pnr>")
def download_ticket(pnr):
    from flask import send_from_directory
    if os.environ.get('VERCEL'):
        return send_from_directory("/tmp", f"ticket_{pnr}.pdf", as_attachment=True)
    return send_from_directory("static/tickets", f"ticket_{pnr}.pdf", as_attachment=True)

# For local development
if __name__ == "__main__":
    app.run(debug=True)

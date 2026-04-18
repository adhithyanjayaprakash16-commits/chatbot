Act as a senior AI engineer, Python developer, and academic project mentor.

I want you to build a complete, professional, beginner-friendly college project on:
“NLP Chatbot using Python, NLTK, Keras/TensorFlow, Flask, and optional Speech Recognition”.

Project goal:
Create an intent-based chatbot that accepts user text input, preprocesses it using NLP, predicts the user intent from a trained model, and returns an automated response. Also include an optional microphone/audio input feature where speech is converted to text and then processed by the same chatbot pipeline.

I want the project to be submission-ready, easy to understand, and suitable for a BCA/BSc/BE college mini project or final-year style demo.

Requirements:

1. Use Python.
2. Use NLTK for tokenization and lemmatization.
3. Use Keras/TensorFlow for training the intent classification model.
4. Use Flask for the web interface and backend.
5. Use an intents.json dataset with tags, patterns, and responses.
6. Save trained artifacts like words.pkl, classes.pkl, and chatbot_model.h5.
7. Add fallback handling when confidence is low.
8. Make the UI clean and professional.
9. Add optional speech recognition for microphone input.
10. Keep the code simple enough for a student to explain in viva.

Now generate the full project in A-Z format with the following output structure:

A. Project overview

- Project title
- Abstract
- Problem statement
- Objective
- Scope
- Expected outcome

B. Tech stack

- Languages
- Libraries
- Frameworks
- Tools used
- Why each tool is selected

C. Architecture

- Explain the end-to-end workflow:
  user input -> preprocessing -> feature extraction -> intent prediction -> response selection -> display output
- Also explain the optional voice flow:
  microphone -> speech-to-text -> chatbot pipeline -> text response
- Provide a simple architecture diagram in text format.

D. Folder structure

- Provide a clean professional folder structure like:
  project/
  ├── app.py
  ├── train.py
  ├── intents.json
  ├── words.pkl
  ├── classes.pkl
  ├── chatbot_model.h5
  ├── templates/
  │ └── index.html
  ├── static/
  │ └── style.css
  ├── requirements.txt
  └── README.md

E. Dataset design

- Create a high-quality intents.json file.
- Include at least 12–15 intents.
- Each intent must have:
  tag
  10+ patterns
  4–6 responses
- Use a college/helpdesk/student-assistant context so the project feels practical.
- Include intents like:
  greeting, goodbye, thanks, admission, fees, courses, timings, hostel, faculty, placements, contact, location, documents_required, scholarship, fallback
- Output the full intents.json code.

F. NLP preprocessing explanation

- Explain tokenization
- Explain lemmatization
- Explain vocabulary building
- Explain bag-of-words or text vectorization
- Explain label encoding
- Explain why preprocessing is needed
- Keep explanation viva-friendly and beginner-friendly

G. Model training code

- Write full train.py code
- Include package imports
- NLTK downloads if needed
- Data loading from intents.json
- Tokenization, lemmatization
- Vocabulary creation
- Training set creation
- Keras model building
- Model compilation
- Model training
- Saving words.pkl, classes.pkl, and chatbot_model.h5
- Add comments only where useful
- Make the code production-clean but understandable

H. Prediction/inference logic

- Write code to:
  clean sentence
  build bag-of-words vector
  predict class probabilities
  filter by confidence threshold
  select the best response
- Explain the threshold logic clearly

I. Flask backend

- Write a full app.py
- Include Flask routes
- Serve index.html
- Accept user message using POST API
- Return chatbot response in JSON
- Load saved model, words.pkl, classes.pkl, and intents.json
- Include fallback response if the model is unsure
- Keep it simple and robust

J. Frontend UI

- Write full index.html
- Write full style.css
- Create a professional chat interface with:
  title/header
  chatbot message area
  user input box
  send button
  optional microphone button
  clean responsive layout
- Use vanilla HTML/CSS/JS only
- Connect frontend to Flask API
- Show both user and bot messages in chat bubbles

K. Speech input feature

- Add an optional microphone feature
- Suggest the easiest practical implementation for a college project
- If browser-based speech input is easier, mention it
- If Python speech_recognition is better for backend demo, mention it
- Provide one working implementation choice
- Explain installation requirements clearly

L. requirements.txt

- Generate the full requirements.txt file

M. README.md

- Write a professional README containing:
  project title
  features
  installation
  how to run
  project structure
  screenshots placeholder sections
  future enhancements

N. Testing

- Give 20 sample user inputs and expected bot behavior
- Mention how to test unknown inputs
- Mention how to test low-confidence fallback

O. Evaluation

- Explain what “accuracy” means in this project
- Mention limitations of intent-based chatbots
- Explain common failure cases
- Explain how to improve the model

P. Viva questions

- Give 25 likely viva questions with short strong answers
- Include questions on NLP, tokenization, lemmatization, intent classification, Flask, dataset, and limitations

Q. Report content

- Write a ready-to-use project report structure:
  Title page
  Certificate page text
  Declaration
  Acknowledgement
  Abstract
  Introduction
  Literature overview
  Existing system
  Proposed system
  Methodology
  Modules
  Algorithm
  Results
  Advantages
  Limitations
  Future scope
  Conclusion
  References

R. PPT content

- Create a 10-slide presentation outline for the project viva
- Include what to write on each slide

S. Deployment/demo

- Explain how to run locally step by step
- Explain how to record a demo video
- Explain what to show during project demonstration

T. Final polish

- Suggest how to make it look more professional
- Suggest small improvements without making it too complex

Important constraints:

- Keep everything beginner-friendly but professional.
- Do not use advanced LLM APIs or paid APIs.
- Prefer offline/local training where possible.
- Make the project realistic for a student to build and explain.
- Use clear section headings.
- Output complete code blocks for every file.
- Do not skip any file.
- Ensure the code works together consistently.
- Make the chatbot context-specific, not generic.
- Make it strong enough for academic submission.

At the end, provide:

1. Final file checklist
2. Exact run commands
3. Common errors and fixes
4. Best explanation strategy for viva

import json
import pickle
import numpy as np
import random
import os
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure NLTK packages are downloaded
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('wordnet', quiet=True)

lemmatizer = WordNetLemmatizer()

# Load the intents dataset
try:
    with open('intents.json', 'r') as file:
        intents = json.load(file)
except FileNotFoundError:
    print("Error: intents.json file not found.")
    exit()

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']

# Prepare the data
print("Preprocessing dataset...")
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_letters]
words = sorted(set(words))
classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

X = []
y = []

for doc in documents:
    bag = []
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in doc[0]]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    X.append(bag)
    y.append(classes.index(doc[1]))

X = np.array(X)
y = np.array(y)

# 80/20 split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

# Use LogisticRegression for better performance on small, high-dimensional data
print("Training model (LogisticRegression)...")
model = LogisticRegression(max_iter=500, random_state=42)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {acc * 100:.2f}%")

if not os.path.exists('output'):
    os.makedirs('output')

report = classification_report(y_test, y_pred, target_names=classes, zero_division=0)
with open('output/evaluation.txt', 'w') as f:
    f.write(f"Test Accuracy: {acc * 100:.2f}%\n\nClassification Report:\n{report}")

# Confusion Matrix
plt.figure(figsize=(12, 10))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', xticklabels=classes, yticklabels=classes, cmap='Blues')
plt.title('Bus Chatbot Confusion Matrix')
plt.tight_layout()
plt.savefig('output/confusion_matrix.png')

pickle.dump(model, open('chatbot_model.pkl', 'wb'))
print("Model and evaluation metrics saved.")

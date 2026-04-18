# Adhii - Tamil Nadu Bus Booking Chatbot

Adhii is a professional, intent-based NLP chatbot designed for bus booking and passenger support across Tamil Nadu. It uses a Neural Network (MLP) for classification and a state-based logic for guided booking flows.

## Core Features
- **40 Complex Intents**: Covers everything from COVID policies to seat selection and live tracking.
- **Guided Booking Flow**: Smooth data collection for Source, Destination, Date, and Passengers.
- **80/20 Train-Test Split**: Scientifically validated model using scikit-learn.
- **Evaluation Dashboard**: Generates classification reports and confusion matrices automatically.
- **Premium UI**: Modern split-pane design with quick action links.
- **Tamil Nadu Specific**: Contextual knowledge about major routes like Chennai, Madurai, Coimbatore, etc.

## Project Structure
```
chatbot_project/
├── app.py                # Flask Backend & Dialogue Manager
├── train.py              # Training script with 80/20 split & evaluation
├── intents.json          # Dataset with 40 tagged categories
├── words.pkl             # Vocabulary artifact
├── classes.pkl           # Label artifact
├── chatbot_model.pkl     # Trained MLPClassifier model
├── output/               # Evaluation results (Metrics, Heatmaps)
├── templates/            # HTML frontend
├── static/               # CSS & JS logic
├── requirements.txt      # Dependency list
├── README.md             # This file
└── Academic_Report.md    # Full documentation, Viva QA, and PPT outline
```

## How to Run

1. **Setup Environment**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Train & Evaluate**:
   This script will train the model, split data 80/20, and save reports to the `output/` folder.
   ```bash
   python train.py
   ```

3. **Launch Website**:
   ```bash
   python app.py
   ```
   Access at: `http://127.0.0.1:5000`

## Evaluation
After running `train.py`, check the `output/` directory for:
- `evaluation.txt`: Accuracy and detailed F1-scores.
- `confusion_matrix.png`: A visual heatmap showing model prediction accuracy.

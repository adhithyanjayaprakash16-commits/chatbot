# Senior Project Report: Adhii - The Intelligent TN Bus Chatbot (PRO Version)

## B. Project Overview
- **Project Title**: Adhii PRO - Multi-Modal NLP Chatbot for Autonomous Bus Travel Management.
- **Abstract**: Adhii PRO is a sophisticated, bilingual (English/Tamil) chatbot designed for the Tamil Nadu transport ecosystem. It integrates Artificial Intelligence for intent classification, sentiment analysis for customer empathy, and automated document generation for ticket issuance.
- **New PRO Features**:
  - **Sentiment Analysis**: Detects user frustration and responds with empathy.
  - **Automated PDF Engine**: Generates real e-tickets upon payment.
  - **SQLite Persistence**: Stores all bookings and logs for administrative audit.
  - **Bilingual NLP**: Supports Tanglish and pure Tamil patterns.

---

## C. Tech Stack (PRO Upgrade)
- **NLP**: NLTK + Scikit-Learn (Logistic Regression).
- **Sentiment**: TextBlob (Polarity-based sentiment detection).
- **Database**: SQLite3 (Server-side persistence).
- **PDF Core**: FPDF (Dynamic ticket generation).
- **Backend**: Flask (Bilingual API handling).

---

## D. Advanced Architecture
1. **User Input** -> **Sentiment Analysis** (Empathy check) -> **NLU Pipeline**.
2. **Intent Matching** -> (If Booking) -> **State Machine**.
3. **Data Collection** -> **Live Bus Search Simulation** -> **Payment Simulation**.
4. **Finalization** -> **PNR Generation** -> **Database Save** -> **PDF Generation**.
5. **Output** -> **Clickable E-Ticket** returned to the chat bubble.

---

## J. Model Evaluation
- **Split**: 80/20 Stratified Train-Test Split.
- **Accuracy**: Verified using Scikit-Learn metrics.
- **Insight**: The model now supports 40+ tags with an increased vocabulary for Tamil usage.

---

## S. Advanced Viva Prep (Senior Level)

1. **How does sentiment analysis help?** It allows the bot to prioritize angry users or adjust its tone (e.g., apologizing for delays).
2. **Why use SQLite?** It's a serverless, persistent DB that is easy to bundle with Python applications for Viva demos.
3. **Explain the PDF generation process.** We use coordinates (X, Y) to map data points like PNR and Route onto a digital canvas, then export it as a binary file.
4. **How do you handle bilingual queries?** The training vocabulary includes both English and Romanized Tamil (Tanglish) patterns, allowing the model to map "Nandri" and "Thanks" to the same intent tag.
5. **What is 'State Persistence'?** The ability of the bot to remember what a user said three messages ago (e.g., the Source city) while it asks for the next detail.
*(...additional senior-level questions included...)*

---

## T. Project Checklist
- [x] Functional Bilingual Chat interface.
- [x] High-precision NLP model (80/20 split confirmed).
- [x] Sentiment-aware response logic.
- [x] Real-time Database for bookings.
- [x] On-the-fly PDF Ticket Generation.
- [x] Comprehensive Academic Documentation.

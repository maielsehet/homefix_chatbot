# 🏠 HomeFix AI

An AI-powered home maintenance assistant that helps users diagnose household problems through **text**, **voice**, and (future) **image analysis**. The assistant communicates with the user, asks follow-up questions, provides simple troubleshooting steps when possible, or recommends the appropriate technician when professional assistance is required.

---

# 📌 Project Overview

HomeFix AI is designed to simplify the process of identifying and solving household maintenance problems.

Instead of immediately contacting a technician, users can describe their issue using text or voice. The AI assistant analyzes the problem, asks intelligent follow-up questions, and determines whether:

- The issue can be solved by the user.
- A professional technician is required.

If a technician is needed, the system generates a complete diagnostic report to help the technician understand the issue before arriving.

---

# 🎯 Objectives

- Reduce unnecessary technician visits.
- Help users solve simple problems themselves.
- Improve communication between customers and technicians.
- Save both time and cost.
- Provide an intelligent troubleshooting experience.

---

# ✨ Features

## ✅ Text Chat

Users can describe their problem naturally.

Example:

> "My air conditioner is leaking water."

The chatbot understands the issue and starts the diagnosis.

---

## 🎤 Voice Input

Users can speak instead of typing.

Workflow:

Voice

↓

Speech-to-Text

↓

AI Diagnosis

↓

Response

---

## 🖼️ Image Analysis (Future Release)

Users will be able to upload images of damaged devices or error screens.

The AI will analyze the image and use it as additional information during diagnosis.

---

## 🤖 Intelligent Diagnosis

Instead of immediately answering, the AI asks follow-up questions.

Example:

User:
"My washing machine is not spinning."

AI:

- Is there any error code?
- Does the machine make noise?
- Does water drain correctly?

The chatbot narrows down the possible causes before providing a recommendation.

---

## 🛠️ DIY Solutions

If the issue is simple, the AI provides step-by-step instructions.

Example:

- Clean the air filter.
- Reset the circuit breaker.
- Check the water valve.

---

## 👷 Technician Recommendation

If the issue cannot be solved safely, the AI recommends the correct technician.

Examples:

- HVAC Technician
- Electrician
- Plumber
- Carpenter

---

## 📄 Technician Report

The AI generates a structured report containing:

- Device
- Problem
- Symptoms
- Possible causes
- User answers
- Suggested diagnosis
- Urgency level

This report is sent to the technician before the visit.

---

# 🧠 AI Workflow

User Input
(Text / Voice)

↓

Speech-to-Text (if voice)

↓

Conversation

↓

Follow-up Questions

↓

RAG Retrieval

↓

LLM

↓

Decision Engine

↓

Simple Solution
OR

Technician Recommendation

↓

Report Generation

---

# 🏗️ System Architecture

Frontend / Mobile

↓

FastAPI

↓

AI Service

↓

RAG Pipeline

↓

Vector Database (ChromaDB)

↓

Large Language Model

↓

JSON Response

---

# 🧩 AI Components

## Retrieval-Augmented Generation (RAG)

Retrieves only the most relevant maintenance information from the knowledge base before generating a response.

---

## Natural Language Processing (NLP)

Processes user requests written in natural language.

---

## Speech-to-Text

Converts voice messages into text before sending them to the chatbot.

---

## Large Language Model (LLM)

Generates human-like responses based on retrieved information.

---

## Decision Engine

Determines whether:

- DIY Solution
- Follow-up Questions
- Technician Recommendation

---

# 📚 Knowledge Base

The AI knowledge base contains structured maintenance information such as:

- Air Conditioners
- Washing Machines
- Refrigerators
- Water Heaters
- Plumbing
- Electrical Problems

Each record includes:

- Device
- Problem
- Symptoms
- Causes
- Solutions
- Technician Required
- Urgency

---

# 📂 Project Structure

```
homefix-ai/

│

├── app/

│ ├── api/

│ ├── rag/

│ ├── services/

│ ├── models/

│ └── utils/

│

├── data/

│

├── vector_db/

│

├── tests/

│

├── requirements.txt

├── README.md

└── main.py
```

---

# ⚙️ Technology Stack

Backend

- Python
- FastAPI

AI

- LangChain
- Hugging Face
- Sentence Transformers

Vector Database

- ChromaDB

Machine Learning

- Embedding Models

Version Control

- Git
- GitHub

---

# 📡 API Endpoints

## POST /chat

Accepts text messages.

---

## POST /voice

Accepts voice recordings.

---

## POST /image (Future)

Accepts image uploads.

---

## POST /feedback

Stores user feedback.

---

# 👥 Team Responsibilities

## AI Lead

- System Design
- Architecture
- Code Review
- Integration
- Task Distribution

---

## Data Engineer

- Collect maintenance data
- Validate information
- Organize knowledge base

---

## AI Engineer

- RAG
- Embeddings
- Vector Database
- Retrieval

---

## Backend AI Engineer

- FastAPI
- API Development
- Integration
- Deployment

---

# 🚀 Future Improvements

- Image Analysis
- OCR for Error Codes
- Predictive Maintenance
- Arabic Dialect Support
- Technician Rating System
- Multi-language Support
- Mobile Notifications

---

# 📖 Future Roadmap

Version 1

- Text Chat
- Voice Support
- RAG
- Technician Recommendation

Version 2

- Image Analysis
- OCR
- Smart Device Detection

Version 3

- Predictive Maintenance
- IoT Integration
- Smart Home Support

---

# 📜 License

This project is developed for educational and startup purposes.

---

# ❤️ Team

Developed with passion by the HomeFix AI Team.

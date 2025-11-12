🧠 MindMirror: Your AI Journal Companion
MindMirror is a full-stack, AI-powered journaling application designed to be a personal companion for self-reflection. It goes beyond a simple notebook by analyzing your emotions, remembering past entries, and providing insightful, empathetic feedback to help you understand your emotional patterns over time.

Core Features
AI-Powered Reflection: Uses a Large Language Model (Llama 3) to generate thoughtful, non-judgmental reflections on your journal entries.

Long-Term Memory (RAG): Implements a Retrieval-Augmented Generation (RAG) system. MindMirror retrieves relevant past entries from a vector database to provide context-aware and deeply personal feedback.

Emotional Analysis: Automatically detects and tags each entry with its primary emotion (e.g., joy, sadness, anger) using a Hugging Face model.

Data Visualization: (Work in progress) A built-in dashboard to visualize your emotional trends, sentiment over time, and most frequent topics.

⚙️ How It Works: The Architecture
MindMirror is built on a modern AI stack that combines data processing with advanced language generation.

Input: The user writes a journal entry in the Streamlit frontend.

Analysis: The text is immediately analyzed by a Hugging Face model to determine the emotion.

Storage: The entry, timestamp, and emotion are saved to a CSV. The text is also embedded and stored as a vector in a ChromaDB vector store.

Retrieval (RAG): The user's new entry is used to query ChromaDB, which retrieves the most emotionally or semantically similar past entries.

Generation: The new entry, the retrieved past entries, and a carefully crafted system prompt are sent to the Llama 3 LLM (via Groq). The LLM generates the final, context-aware reflection, which is displayed to the user.

🧰 Tech Stack
Frontend: Streamlit

Backend: Python

LLM: Llama 3 (via Groq API)

Vector Database (RAG): ChromaDB

AI & ML: Hugging Face Transformers, SentenceTransformers

Data Handling: Pandas

Data Visualization: Matplotlib, Seaborn

🚀 Getting Started
Follow these instructions to get a local copy up and running.

Prerequisites
Anaconda or Miniconda

A free Groq API key (get one at groq.com)

Installation
Clone the repository:

Bash

git clone https://github.com/your-username/mindmirror_app.git
cd mindmirror_app
Create and activate the Conda environment:

Bash

conda create --name mindmirror python=3.9
conda activate mindmirror
Install the required libraries:

Bash

pip install -r requirements.txt
Set up your environment variables:

Create a file in the root directory named .env

Add your Groq API key to this file:

GROQ_API_KEY="your-secret-api-key-here"
Run the application:

Bash

streamlit run app.py
Your default web browser will open, and you can start using MindMirror!

🗺️ Future Roadmap
User Authentication: Add a login system so multiple users can have their own private journals.

Speech-to-Text: Integrate a "voice memo" feature to allow users to speak their entries.

Advanced Dashboard: Build out the interactive visualization page within Streamlit.

Custom Fine-Tuning: Fine-tune a smaller, open-source model on therapeutic conversation datasets to create a unique MindMirror "personality."

License
Distributed under the MIT License. See LICENSE for more information.

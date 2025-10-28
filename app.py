import os
import pandas as pd
from datetime import datetime
from transformers import pipeline
import chromadb
from groq import Groq
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

project_path = 'C:/Users/User/Desktop/mindmirror/MyMindMirrorProject'
journal_file_path = os.path.join(project_path, 'journal.csv')

emotion_classifier = pipeline(
    'text-classification',
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=1
)

db_path = os.path.join(project_path, 'mindmirror_memory')

client = chromadb.PersistentClient(path=db_path)

collection = client.get_or_create_collection(name="journal_entries")

def store_in_vectordb(entry, entry_id, metadata):

  collection.add(
      documents=[entry],
      ids=[entry_id],
      metadatas=[metadata]
  )


def retrieve_similar_query(query, k=2):
    results = collection.query(
        query_texts=[query],
        n_results=k
    )
    return results
    

def process_and_store_entry(entry):
    analysedResult = emotion_classifier(entry)
    emotionLabel = analysedResult[0][0]['label']
    emotionScore = round(analysedResult[0][0]['score'], 4)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    newEntry = {
        'timestamp': [timestamp],
        'entry': [entry],
        'emotion_label' : [emotionLabel],
        'emotion_score' : [emotionScore]
        }
    df = pd.DataFrame(newEntry)

    if os.path.exists(journal_file_path):
        df.to_csv(journal_file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(journal_file_path, mode='w', header=True, index=False)

    store_in_vectordb(
        entry = entry,
        entry_id = timestamp,
        metadata = {
            'emotion': emotionLabel
        }
    )


clientGroq = Groq(api_key=GROQ_API_KEY)

def get_LLM_response(entry, retrieved_memory):
  memories_context = "\n".join(retrieved_memory['documents'][0]) if retrieved_memory['documents'] else "No relevant memories found."
  system_prompt = f"""
    You are MindMirror, a deeply empathetic and insightful AI journal companion. Your purpose is to help the user reflect on their thoughts and emotions, not to give advice.

    You are reviewing a user's journal entry. You also have access to some of their past entries that might be related.

    Here are the user's relevant past memories:
    ---
    {memories_context}
    ---

    Now, here is the user's new journal entry:
    ---
    {entry}
    ---

    Your task is to:
    1. Acknowledge and validate the user's current feelings.
    2. Gently and subtly connect their current feelings to the patterns or themes from their past memories, if there's a clear link.
    3. End with a single, gentle, open-ended, and reflective question to encourage deeper thought. Do not give advice or solutions.
    """

  chat_completion = clientGroq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt}
        ]
    )
  
  return chat_completion.choices[0].message.content



st.title("🧠 MindMirror: Your AI Journal")
st.write("Welcome to your personal space for reflection. Write down your thoughts, and let's explore them together.")

user_entry = st.text_area("How are you feeling today?", height=150)

if st.button("Reflect on This Entry"):
    if user_entry:
        
        with st.spinner("Processing your thoughts..."):
            
            process_and_store_entry(user_entry)

            
            similar_memories = retrieve_similar_query(user_entry)

            
            ai_reflection = get_LLM_response(user_entry, similar_memories)

            
            st.subheader("MindMirror's Reflection:")
            st.write(ai_reflection)

            st.subheader("Similar Memories Retrieved:")
            if similar_memories and similar_memories['documents']:
                for doc in similar_memories['documents'][0]:
                    st.info(f"- {doc}")
            else:
                st.write("No specific memories came to mind for this entry.")
    else:
        st.warning("Please write something before reflecting.")
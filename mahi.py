import streamlit as st
import openai
import json
import os

# ✅ DEBUG LINE: Check if OpenAI key is loaded
st.write("Secrets loaded?", "openai" in st.secrets)

# Set your OpenAI API key
openai.api_key = st.secrets["openai"]["api_key"]

# Load memory from file
def load_memory():
    if os.path.exists("memory.json"):
        with open("memory.json", "r") as f:
            return json.load(f)
    return {"name": "", "mood": "", "skincare": "", "body_goals": ""}

# Save memory to file
def save_memory(memory):
    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=2)

# Start Streamlit app
st.set_page_config(page_title="Mahi - Your Sweet AI Buddy 💗")
st.title("🌸 Chat with Mahi – Your Soft, Sweet Buddy")

memory = load_memory()

# Collect user profile only once
if memory["name"] == "":
    memory["name"] = st.text_input("What's your name?")
    memory["mood"] = st.text_input("How are you feeling today?")
    memory["skincare"] = st.text_input("Any skincare concerns?")
    memory["body_goals"] = st.text_input("Do you have any body goals?")
    if st.button("Save & Start Chat"):
        save_memory(memory)
        st.success("Mahi is ready to talk to you 💕")
        st.experimental_rerun()
else:
    st.markdown(f"👋 Hello **{memory['name']}**, I'm Mahi! Let's chat.")
    st.markdown(f"🌸 Mood: *{memory['mood']}*  |  ✨ Body Goal: *{memory['body_goals']}*")

    user_input = st.text_input("Type your message to Mahi")

    if user_input:
       if user_input:
    prompt = f"""
You are Mahi, a sweet, comforting best friend for {memory['name']}.
She is feeling {memory['mood']} today. Her skincare concern is: {memory['skincare']}.
Her body goal is: {memory['body_goals']}.
Reply like a loving friend — gentle, soft, and emotionally warm.

User: {user_input}
Mahi:
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        reply = response['choices'][0]['message']['content']
        st.text_area("Mahi says:", value=reply, height=150)

    except openai.error.OpenAIError as e:
        st.error(f"OpenAI API error: {e}")

    except Exception as e:
        st.error(f"Unexpected error: {e}")


import streamlit as st
import os
import datetime
from openai import OpenAI

# Get your API key from Streamlit Secrets
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="BDR Assistant", layout="centered")
st.image("https://uploads-ssl.webflow.com/63b4b77234c56e3301c2d31a/63b4c0ebed7bda69d179d276_tixr_logo.svg", width=180)

st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .block-container {
        padding-top: 1.5rem;
    }
    .stTextArea textarea, .stSelectbox, .stTextInput input {
        border-radius: 0.5rem;
        border: 1px solid #ccc;
        padding: 10px;
        font-size: 15px;
    }
    .stButton > button {
        background-color: #0056b3;
        color: white;
        border-radius: 0.4rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #004099;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎧 Tixr BDR Call Assistant")
st.caption("Qualify faster. Sound smarter. Learn quicker.")

# Input section
with st.expander("📝 Fill out call details"):
    tone = st.selectbox("🗣️ Choose Tone", ["Friendly", "Professional", "Direct", "Playful"])
    transcript = st.text_area("📄 Paste Transcript", value='Based on my research, this organiser will be asking questions about:', height=200)
    vertical = st.selectbox("🎯 Choose Event Vertical", ["Music", "Comedy", "Sports", "Festivals", "Venues", "Other"])
    ticketing_company = st.selectbox("🎟️ What ticketing company does the prospect currently use?", [
        "AXS", "Dice", "Easol", "Eventbrite", "Eventim", "Fatsoma", "Gigantic", "SeeTickets",
        "Secutix", "Skiddle", "Ticketmaster", "Universe", "Vivenu"
    ])
    prospect_website = st.text_input("🌐 Prospect Website URL (optional)")

log_data = []

if st.button("💡 Get Tailored Question Funnel"):
    if not transcript.strip():
        st.warning("Please paste a transcript to proceed.")
    else:
        with st.spinner("Building tailored question funnel..."):
            try:
                funnel_prompt = f"""
You are a sales assistant helping a BDR at Tixr prepare for their first conversation with a new event organiser.
The organizer currently uses {ticketing_company} and operates in the {vertical} vertical.

Your job is to create a concise but effective question funnel — a sequence of thoughtful, tailored questions the BDR can ask to understand the prospect’s needs, uncover friction with their current platform, and naturally lead toward booking a deeper discovery call with a BDM.

Avoid diving into product details. Use Tixr's name where helpful to establish relevance or contrast. For example, if you're referring to the BDR's knowledge or product fit, say "Tixr offers..." or "Tixr is known for..."

Make the tone {tone.lower()}, conversational, and natural — as if a UK-based BDR were chatting over coffee with the organiser. Keep it practical and human, not robotic or scripted. Mention Tixr where it's genuinely helpful, not pushy.

Structure the output as:

1. **Intro Question** (Warm, open-ended)
2. **Context Question** (Current setup)
3. **Pain Exploration** (Highlight potential friction)
4. **Vision Question** (What would great look like?)
5. **Close Question** (Segues to booking a follow-up)

Transcript Insight:
{transcript}
                """

                funnel_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You help BDRs guide smart, structured first conversations."},
                        {"role": "user", "content": funnel_prompt}
                    ]
                )

                funnel_output = funnel_response.choices[0].message.content
                st.subheader("🧭 Tailored Question Funnel")
                with st.container():
                    for line in funnel_output.split(""):

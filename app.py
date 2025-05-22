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
You are a sales assistant helping a BDR at Tixr prepare for their first conversation with a new event organizer.
The organizer currently uses {ticketing_company} and operates in the {vertical} vertical.

Your job is to create a concise but effective question funnel — a sequence of thoughtful, tailored questions the BDR can ask to understand the prospect’s needs, uncover friction with their current platform, and naturally lead toward booking a deeper discovery call with a BDM.

Avoid diving into product details. Use Tixr's name where helpful to establish relevance or contrast. For example, if you're referring to the BDR's knowledge or product fit, say "Tixr offers..." or "Tixr is known for..."

Make the tone {tone.lower()}, conversational, and natural — as if a BDR were chatting casually with the organizer. Keep it practical and human, not robotic or scripted. Mention Tixr where it's genuinely helpful, not pushy.

Structure the output as:

1. **Intro Questions** (2–3 short, warm questions to start the conversation)
   - *Tip:* Use these to show you've done your homework and break the ice.
   - *Example Answer:* "We’ve been looking to expand our pre-sale reach lately."

2. **Context Questions** (2–3 short questions about their current setup)
   - *Tip:* Focus on what they’re using today and how it works for them.
   - *Example Answer:* "We mostly rely on manual check-ins through [platform]."

3. **Pain Exploration Questions** (2–3 concise questions to uncover friction)
   - *Tip:* Use these to surface known weaknesses in their current platform.
   - *Example Answer:* "Reporting’s been a bit patchy — hard to get clear insights quickly."

4. **Vision Questions** (2–3 impactful prompts to understand what they want)
   - *Tip:* Prompt them to picture a better experience — that’s where Tixr fits in.
   - *Example Answer:* "I’d love something that can automate more of our comp tracking."

5. **Close Questions** (2–3 natural segues to book a follow-up with a BDM)
   - *Tip:* These should feel casual but confident — open the door for the next step.
   - *Example Answer:* "Yeah, happy to book in a time next week to explore further."(2–3 natural segues to book a follow-up with a BDM)

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
                st.markdown(funnel_output)
                try:
                    st.download_button("📋 Copy All Questions", funnel_output, file_name="tixr_question_funnel.txt")
                except Exception as e:
                    st.error(f"Download button failed: {e}")

            except Exception as e:
                st.error(f"Something went wrong: {e}")

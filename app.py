import streamlit as st
import os
import datetime
from openai import OpenAI

# Get your API key from Streamlit Secrets
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="BDR Assistant", layout="centered")
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

Avoid diving into Tixr product details. Instead, help the BDR guide a conversation that builds trust and curiosity. Structure the output as:

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
                st.markdown(funnel_output)

                log_data.append({
                    "timestamp": datetime.datetime.now().isoformat(),
                    "type": "question_funnel",
                    "ticketing_company": ticketing_company,
                    "vertical": vertical,
                    "prospect_website": prospect_website,
                    "transcript": transcript,
                    "funnel": funnel_output
                })

            except Exception as e:
                st.error(f"Something went wrong: {e}")

if st.button("🧠 Research This Ticketing Company"):
    with st.spinner("Gathering quick insights..."):
        try:
            company_prompt = f"""
Give a short overview of {ticketing_company}. List its typical clients, main features, and common criticisms or challenges event organizers face when using it.
Keep it brief and helpful for a BDR preparing for a competitive sales call.
            """
            company_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You help BDRs research ticketing companies quickly."},
                    {"role": "user", "content": company_prompt}
                ]
            )
            st.subheader(f"📌 Research on {ticketing_company}:")
            st.markdown(company_response.choices[0].message.content)

            log_data.append({
                "timestamp": datetime.datetime.now().isoformat(),
                "type": "ticketing_research",
                "ticketing_company": ticketing_company,
                "content": company_response.choices[0].message.content
            })

        except Exception as e:
            st.error(f"Something went wrong: {e}")

if prospect_website and st.button("🔍 Research This Prospect"):
    with st.spinner("Researching the prospect (mock data only)..."):
        try:
            prospect_prompt = f"""
You're helping a BDR prepare to speak with an event organizer. Here's their website: {prospect_website}

Analyze the type of organizer based on the website. Suggest what types of events they likely run, any unique value propositions they seem to offer, and what a BDR should know before a first conversation. Assume the BDR wants to be informed but not overwhelm the prospect.
If you cannot access the website, provide a generic briefing format they can follow.
            """
            prospect_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You help BDRs quickly research prospects or organizers."},
                    {"role": "user", "content": prospect_prompt}
                ]
            )
            st.subheader(f"🔍 Prospect Briefing: {prospect_website}")
            st.markdown(prospect_response.choices[0].message.content)

            log_data.append({
                "timestamp": datetime.datetime.now().isoformat(),
                "type": "prospect_research",
                "prospect_name": prospect_name,
                "content": prospect_response.choices[0].message.content
            })

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# Display session log summary (in debug/testing mode only)
with st.expander("🗂️ View Session Log"):
    if log_data:
        for log in log_data:
            st.write(log)
    else:
        st.caption("No logs recorded yet in this session.")

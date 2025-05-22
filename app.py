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
        background-color: #f9f9f9;
    }
    .block-container {
        padding-top: 2rem;
    }
    .stTextArea textarea {
        background-color: #ffffff;
        border: 1px solid #cccccc;
    }
    .stSelectbox, .stTextInput {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎧 Tixr BDR Call Assistant")
st.caption("Qualify faster. Sound smarter. Learn quicker.")

# Input section
with st.expander("📝 Fill out call details"):
    transcript = st.text_area("📄 Paste Transcript", height=200)
    vertical = st.selectbox("🎯 Choose Event Vertical", ["Music", "Comedy", "Sports", "Festivals", "Venues", "Other"])
    ticketing_company = st.selectbox("🎟️ What ticketing company does the prospect currently use?", [
        "AXS", "Dice", "Easol", "Eventbrite", "Eventim", "Fatsoma", "Gigantic", "SeeTickets",
        "Secutix", "Skiddle", "Ticketmaster", "Universe", "Vivenu"
    ])
    prospect_name = st.text_input("👤 Prospect or Event Organizer Name (optional)")

log_data = []

if st.button("💡 Get Suggested Questions"):
    if not transcript.strip():
        st.warning("Please paste a transcript to proceed.")
    else:
        with st.spinner("Thinking..."):
            try:
                prompt = f"""
You are a helpful assistant for a BDR in the ticketing industry.
The prospect currently uses {ticketing_company} for ticketing, and operates in the {vertical} vertical.
Based on the following sales call transcript, suggest 3 short, high-quality open-ended discovery questions (1 sentence each) that the BDR can ask next.

Transcript:
{transcript}
                """

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You help BDRs ask smart, concise discovery questions."},
                        {"role": "user", "content": prompt}
                    ]
                )

                suggestions = response.choices[0].message.content
                st.subheader("🤖 Suggested Questions:")
                st.markdown(suggestions)

                log_data.append({
                    "timestamp": datetime.datetime.now().isoformat(),
                    "type": "question_suggestions",
                    "ticketing_company": ticketing_company,
                    "vertical": vertical,
                    "prospect_name": prospect_name,
                    "transcript": transcript,
                    "suggestions": suggestions
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

if prospect_name and st.button("🔍 Research This Prospect"):
    with st.spinner("Researching the prospect (mock data only)..."):
        try:
            prospect_prompt = f"""
Give a quick briefing for a BDR going into a meeting with an event organizer or prospect named '{prospect_name}'.
Summarize what they might be known for, the type of events they organize, and any notable past partnerships or challenges.
If no real data is available, provide a generic template or useful guidance.
            """
            prospect_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You help BDRs quickly research prospects or organizers."},
                    {"role": "user", "content": prospect_prompt}
                ]
            )
            st.subheader(f"🔍 Prospect Briefing: {prospect_name}")
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

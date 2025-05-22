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
st.header("📈 Deal Size Calculator")
tickets_sold = st.number_input("🎟️ Tickets sold in last 12 months", min_value=0, step=10)
avg_ticket_price = st.number_input("💷 Average ticket price (£)", min_value=0.0, step=0.5)

if tickets_sold and avg_ticket_price:
    gross_revenue = tickets_sold * avg_ticket_price
    estimated_tixr_share = gross_revenue * 0.05
    qualification_status = "✅ Qualified" if estimated_tixr_share >= 20000 else "❌ Disqualified"

    st.markdown(f"**Estimated Gross Revenue:** £{gross_revenue:,.2f}")
    st.markdown(f"**5% Estimate (Tixr Potential):** £{estimated_tixr_share:,.2f}")
    st.markdown(f"**Qualification Status:** {qualification_status}")

st.header("📝 Fill Out Call Details")
tone = st.selectbox("🗣️ Choose Tone", ["Friendly", "Professional", "Direct", "Playful"])
transcript = st.text_area("📄 What would you like to talk about in this call with the client?", placeholder='Marketing, handling large on-sales, membership ticketing, reserved seating, ticketing page design, etc.', height=200)
ticketing_company = st.selectbox("🎟️ What ticketing company does the prospect currently use?", [
    "AXS", "Dice", "Easol", "Eventbrite", "Eventim", "Fatsoma", "Gigantic", "SeeTickets",
    "Secutix", "Skiddle", "Ticketmaster", "Universe", "Vivenu"
])
prospect_website = st.text_input("🌐 Prospect Website URL (optional)")

log_data = []

if st.button("💡 Get Tailored Question Funnel"):
    if not transcript.strip():
        st.warning("Please fill in what you'd like to talk about.")
    else:
        with st.spinner("Building tailored question funnel..."):
            try:
                funnel_prompt = f"""
You are a sales assistant helping a BDR at Tixr prepare for their first conversation with a new event organizer.
The organizer currently uses {ticketing_company}. Use your knowledge of where {ticketing_company} typically falls short or gets criticized in the industry to craft strategic discovery questions that uncover potential gaps.

Your job is to create a concise but effective question funnel — a sequence of thoughtful, tailored questions the BDR can ask to understand the prospect’s needs, uncover friction with their current platform, and naturally lead toward booking a deeper discovery call with a BDM.

Avoid diving into product details. Use Tixr's name where helpful to establish relevance or contrast. For example, if you're referring to the BDR's knowledge or product fit, say "Tixr offers..." or "Tixr is known for..."

Make the tone {tone.lower()}, conversational, and natural — as if a BDR were chatting casually with the organizer. Keep it practical and human, not robotic or scripted. Mention Tixr where it's genuinely helpful, not pushy.

Structure the out

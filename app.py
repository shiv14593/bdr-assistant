import streamlit as st
import os
from openai import OpenAI

# Get your API key from Streamlit Secrets
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="BDR Assistant", layout="centered")
st.title("🎧 Tixr BDR Call Assistant")
st.write("Paste a snippet from your sales call and get smart, open-ended questions to keep the conversation flowing.")

# Input section
transcript = st.text_area("📄 Paste Transcript", height=200)
vertical = st.selectbox("🎯 Choose Event Vertical", ["Music", "Comedy", "Sports", "Festivals", "Venues", "Other"])

if st.button("💡 Get Suggested Questions"):
    if not transcript.strip():
        st.warning("Please paste a transcript to proceed.")
    else:
        with st.spinner("Thinking..."):
            try:
                prompt = f"""
You are a helpful assistant for a BDR in the UK ticketing industry.
Based on the following sales call transcript and the vertical ({vertical}), suggest 3 high-quality but short and clear open-ended discovery questions the BDR can ask next. The goal here is to help BDRs train but also in a live enviornment ask questions on the fly

Transcript:
{transcript}
                """

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You help BDRs ask smart discovery questions."},
                        {"role": "user", "content": prompt}
                    ]
                )

                suggestions = response.choices[0].message.content
                st.subheader("🤖 Suggested Questions:")
                st.markdown(suggestions)

            except Exception as e:
                st.error(f"Something went wrong: {e}")

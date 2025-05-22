import streamlit as st
import openai
import os

# Use secret from Streamlit settings (safer)
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="BDR Assistant", layout="centered")

st.title("🎧 Tixr BDR Call Assistant")
st.write("Paste a snippet from your sales call and get smart, open-ended questions to keep the conversation flowing.")

# Input fields
transcript = st.text_area("📄 Paste Transcript", height=200)
vertical = st.selectbox("🎯 Choose Event Vertical", ["Music", "Comedy", "Sports", "Festivals", "Venues", "Other"])

if st.button("💡 Get Suggested Questions"):
    if transcript.strip() == "":
        st.warning("Please paste a transcript to proceed.")
    else:
        with st.spinner("Thinking..."):
            prompt = f"""
You are a helpful assistant for a BDR in the ticketing industry.
Based on the following sales call transcript and the vertical ({vertical}), suggest 3 high-quality open-ended discovery questions the BDR can ask next.

Transcript:
{transcript}
            """

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You help BDRs ask smart discovery questions."},
                        {"role": "user", "content": prompt}
                    ]
                )

                suggestions = response['choices'][0]['message']['content']
                st.subheader("🤖 Suggested Questions:")
                st.markdown(suggestions)

            except Exception as e:
                st.error(f"Something went wrong: {e}")

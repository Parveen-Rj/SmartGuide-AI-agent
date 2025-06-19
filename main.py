import streamlit as st
st.set_page_config(page_title="SmartGuide AI", page_icon="🤖", layout="centered")
#import google.generativeai as geminiai
from dotenv import load_dotenv
import os
from agents import Agent,Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
# Load API Key
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)


agent = Agent(
    name = "Agent",
    instructions = "You are SmartGuide AI — a highly knowledgeable assistant trained to answer questions accurately and responsibly in the fields of Health, Education, Islam, and Technology. You must always provide factual, ethical, and clear answers."

)
# Custom CSS for styling
st.markdown("""
    <style>
            /* REMOVE default top spacing */
    .block-container {
        padding-top: 2rem !important;
    }

    /* Optional: also remove margin from body */
    body {
        margin: 2px;
        padding: 2px;
    }
    /* Page background */
.stApp {
        background-color: #0f172a;
        font-family: 'Segoe UI', sans-serif;
        padding: 20px;
    }

    .title-style {
         font-weight: 700;
         font-size: 42px;
        
        color: #38bdf8;
        text-align: center;
        margin-bottom: 12px;
    }


    /* Label for input */
    label {
        color: #f8fafc !important;
        font-size: 18px !important;
        font-weight: 600;
    }

    /* Input box */
    input[type="text"] {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
        border: 2px solid #38bdf8 !important;
        padding: 10px;
        font-size: 16px;
        border-radius: 8px;
        width: 100%;
    }

    /* Placeholder text */
    input::placeholder {
        color: #94a3b8 !important;
        font-style: italic;
    }

    button[kind="primary"] {
        background-color: #38bdf8;
        color: #0f172a;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        margin-top: 15px;
        transition: 0.3s ease;
    }

    button[kind="primary"]:hover {
        background-color: #0ea5e9;
        color: white;
    }

    .stSpinner > div > div {
        color: #facc15;
    }

    .stMarkdown {
        background-color: #1e293b;
        color: #e2e8f0;
        border-left: 5px solid #38bdf8;
        padding: 15px;
        border-radius: 10px;
        font-size: 17px;
    }
    </style>
""", unsafe_allow_html=True)





st.markdown('<div class="title-style">🤖 SmartGuide AI</div>', unsafe_allow_html=True)
st.markdown('<div class="caption-style">Ask questions about Health, General Knowledge, Education, Islam, or Technology.</div>', unsafe_allow_html=True)

# st.title("🤖 SmartGuideAI")
# st.caption("Ask questions about Health, General Knowledge , Education, Islam, or Technology.")

# Input
user_input = st.text_input("💬 Ask SmartGuideAI:", placeholder="ask anything?")

if st.button("Ask"):
    if user_input.strip() == "":


        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = Runner.run_sync(
                    agent,
                    input=user_input,
                    run_config=config
                )
                st.success("Answer:")
                st.write(response)
            except Exception as e:
                st.error(f"❌ Error: {e}")


# response = Runner.run_sync(
#     agent,
#     input = "input text",
#     run_config = config

    
# )
# print(response)
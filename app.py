from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

import streamlit as st
import os
from dotenv import load_dotenv   

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
## langsmith tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY") 

prompt = ChatPromptTemplate.from_messages(
    [
        ("system" , "You are a helpful assistant. Please response to the user queries"),
        ("user" , "Question:{question}")
    ]
)

from langchain_core.messages import HumanMessage
import base64

st.title("Langchain Gemini – Text + Image Support")

input_text = st.text_input("Ask something...")
uploaded_image = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY
)

output_parser = StrOutputParser()
chain = prompt | model | output_parser


def encode_image(file):
    return base64.b64encode(file.read()).decode("utf-8")


if st.button("Submit"):
    if uploaded_image and input_text:
        img_b64 = encode_image(uploaded_image)

        message = HumanMessage(content=[
            {"type": "text",
             "text": f"Use the image + question to answer.\nQuestion: {input_text}"},
            {"type": "image_url",
             "image_url": f"data:image/jpeg;base64,{img_b64}"}
        ])

        response = model.invoke([message])
        st.write(response.content)

    # ---- Case 2: Only Image ----
    elif uploaded_image:
        img_b64 = encode_image(uploaded_image)

        message = HumanMessage(content=[
            {"type": "text", "text": "Describe this image in detail"},
            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{img_b64}"}
        ])

        response = model.invoke([message])
        st.write(response.content)

    # ---- Case 3: Only Text ----
    elif input_text:
        st.write(chain.invoke({"question": input_text}))

    else:
        st.warning("Please enter a question or upload an image.")

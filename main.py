import streamlit as st
import openai
from openai import OpenAI
import base64
from PIL import Image
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# Function to convert image to base64
def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Function to send image data and additional info to OpenAI
def analyze_image_with_openai(image_data, location, date):
    prompt = f"Analyze this image taken at {location} on {date}. Describe what you see and provide insights."
    
    # Ensure your API key is loaded from environment variables
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Sending a base64 encoded image isn't directly supported; this is a placeholder
    # You would need to use an image processing API to describe the image or use the image data
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=300
    )

    return response.choices[0].text

# Function to create a PDF from the analysis result
def create_pdf(text, location, date):
    pdf_file_path = f"Disaster_Report_{location.replace(' ', '_')}_{date}.pdf"
    c = canvas.Canvas(pdf_file_path, pagesize=letter)
    c.drawString(72, 750, f"Disaster Report for {location}")
    c.drawString(72, 730, f"Date: {date}")
    text_object = c.beginText(72, 710)
    text_object.textLines(text)
    c.drawText(text_object)
    c.save()
    return pdf_file_path

# Streamlit UI setup
st.title("Disaster Image Analysis with GPT-4")

# Image uploader
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Location and date input
location = st.text_input("Enter the location of the image")
date = st.date_input("Select the date of the image", datetime.today())

# Analyze button
if st.button("Analyze Image"):
    if uploaded_file is not None and location:
        # Convert the uploaded file to an image and then to base64
        image = Image.open(uploaded_file)
        image_base64 = image_to_base64(image)

        # Call the function to send the image data to OpenAI and display the response
        try:
            description = analyze_image_with_openai(image_base64, location, date.strftime("%Y-%m-%d"))
            st.write("Analysis Result:")
            st.write(description)

            # Create a PDF with the report content
            pdf_file_path = create_pdf(description, location, date.strftime("%Y-%m-%d"))
            
            # Display a link to download the PDF
            with open(pdf_file_path, "rb") as file:
                st.download_button(
                    label="Download PDF Report",
                    data=file,
                    file_name=pdf_file_path,
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"Failed to analyze the image: {e}")
    else:
        st.warning("Please upload an image and specify the location and date.")

import streamlit as st
from transformers import pipeline, AutoImageProcessor
from PIL import Image

# 1. Setup Page Config
st.set_page_config(page_title="Plant Health AI", page_icon="🌱")
st.title("🌱 Plant Disease Detector")
st.write("Upload a photo of a plant leaf to identify potential diseases.")

# 2. Load the AI Model from Hugging Face
@st.cache_resource
def load_model():
    # This downloads the model on first run and caches it locally
    processor = AutoImageProcessor.from_pretrained(
        "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification",
        use_fast=True
    )
    # Load the pipeline with the processor
    return pipeline(
        "image-classification", 
        model="linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification",
        image_processor=processor
    )

classifier = load_model()

# 3. Disease Management Database (Sample)
# You can expand this dictionary with more specific tips
management_tips = {
    "Potato___Early_blight": "Apply copper-based fungicides. Ensure proper spacing for airflow.",
    "Tomato___Bacterial_spot": "Avoid overhead watering. Remove infected plant debris immediately.",
    "Corn_(maize)___Common_rust": "Use resistant varieties and apply fungicides if infection is severe.",
    "Apple___Black_rot": "Prune out dead wood and remove mummified fruit from the tree.",
    "healthy": "Your plant looks healthy! Keep up the good work with regular watering and sunlight."
}

# 4. Image Upload Logic
uploaded_file = st.file_uploader("Choose a leaf image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)
    
    with st.spinner('Analyzing plant health...'):
        # Get predictions
        results = classifier(image)
        
        # Display Results
        top_prediction = results[0]
        label = top_prediction['label']
        confidence = top_prediction['score']
        
        st.subheader(f"Result: {label}")
        st.info(f"Confidence Level: {confidence:.2%}")

        # Provide Management Tips
        st.markdown("### 🛠️ Management Strategy")
        # Check if the label (or part of it) exists in our tips database
        tips = management_tips.get(label, "Consult an agricultural expert for specific treatment for this variety.")
        st.write(tips)
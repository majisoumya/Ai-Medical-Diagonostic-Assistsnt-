import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import traceback
from PIL import Image
import io
import requests
from streamlit_lottie import st_lottie # Import lottie for animations

# --- Custom CSS for the final, polished look ---
def load_css():
    st.markdown("""
        <style>
        /* Define keyframe animations */
        @keyframes gradient-animation {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Use a pseudo-element for the animated gradient background */
        .stApp::before {
            content: '';
            position: fixed; /* Fixed position to cover the entire viewport */
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: -2; /* Place it behind all content */
            background: linear-gradient(-45deg, #0d1b2a, #1b263b, #415a77, #778da9);
            background-size: 400% 400%;
            animation: gradient-animation 20s ease infinite;
        }

        /* Main page styling with medical icon pattern */
        .stApp {
            /* Layer the repeating medical icon pattern on top */
            background-image: url('—Pngtree—pharmacist 3d icon isolated on_20173428.png');
            background-color: transparent; /* Make the element's own background transparent */
            z-index: 4;
        }

        /* Title styling */
        h1 {
            text-align: center;
            color: #FFFFFF;
            text-shadow: 0px 2px 8px rgba(0, 0, 0, 0.3);
            animation: fadeIn 1s ease-out;
            font-weight: 700;
        }
        
        /* LEFT column/container - "Frosted Glass" Light */
        .st-emotion-cache-1r6slb0 {
             background-color: rgba(255, 255, 255, 0.8);
             border: 1px solid rgba(255, 255, 255, 0.2);
             border-radius: 15px;
             padding: 25px !important;
             box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
             backdrop-filter: blur(10px);
             -webkit-backdrop-filter: blur(10px);
             transition: all 0.3s ease-in-out;
             color: #2c3e50; /* Dark text for the light panel */
        }
        .st-emotion-cache-1r6slb0:hover {
            transform: translateY(-5px);
        }
        
        /* RIGHT column/container - "Frosted Glass" Dark for WHITE text */
        .st-emotion-cache-1bp22im {
             background-color: rgba(27, 38, 59, 0.85); /* Dark blue frosted glass */
             border: 1px solid rgba(255, 255, 255, 0.1);
             border-radius: 15px;
             padding: 25px !important;
             box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
             backdrop-filter: blur(10px);
             -webkit-backdrop-filter: blur(10px);
             transition: all 0.3s ease-in-out;
             color: #FFFFFF !important; /* White text for the dark panel */
        }
        .st-emotion-cache-1bp22im:hover {
            transform: translateY(-5px);
        }
        
        /* Ensure all text within the right dark panel is white */
        .st-emotion-cache-1bp22im .stMarkdown, .st-emotion-cache-1bp22im .stInfo {
            color: #FFFFFF !important;
        }
        /* Style links to be visible on the dark panel */
        .st-emotion-cache-1bp22im a {
            color: #87CEEB !important; /* Sky blue for links */
        }

        /* Button styling */
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            border: none;
            background: linear-gradient(45deg, #00B4DB, #0083B0);
            color: white;
            font-weight: 600;
            padding: 12px 0;
            transition: all 0.3s ease-in-out;
            box-shadow: 0 4px 15px 0 rgba(0, 172, 219, 0.3);
        }
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 20px 0 rgba(0, 172, 219, 0.5);
        }
        
        </style>
    """, unsafe_allow_html=True)

# --- Function to load Lottie animation from URL (Unchanged) ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="AI Diagnostic Assistant", 
    page_icon="🩺", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS
load_css()

st.title("🩺 AI-Powered Medical Image Diagnostic Assistant")

# --- API Key Configuration ---
# IMPORTANT: Replace "YOUR_API_KEY_HERE" with your actual Google Gemini API key.
api_key = "AIzaSyCiZ946lLDnstnByuKCyMbGVle2Y1fHyCk" # Replace with your key

# Stop the app if the API key hasn't been replaced.
if not api_key or api_key == "YOUR_API_KEY_HERE":
    st.error("Please replace 'YOUR_API_KEY_HERE' with your actual Google API Key in the code.")
    st.info("You can get your API key from Google AI Studio.")
    st.stop()

# --- Configure the Generative AI model ---
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Failed to configure the API with the provided key. Please check your key. Error: {e}")
    st.stop()

# --- System Prompt (Unchanged) ---
system_prompt = """
You are a highly specialized AI medical assistant trained to analyze a wide variety of medical images and assist in disease prediction. Your primary function is to assess the uploaded image and provide an accurate, responsible, and ethical analysis based on known medical imaging patterns.

Follow these strict guidelines:

1. **Image Analysis**:
   - Identify the type of image provided (e.g., X-ray, MRI, CT scan, histopathology slide, skin lesion photo, etc.).
   - Detect any abnormal patterns such as tumors, lesions, asymmetries, discolorations, or structural anomalies.

2. **Disease Prediction**:
   - Based on the visual evidence, suggest potential medical conditions. Examples include, but are not limited to:
     - Cancers (e.g., breast cancer, lung cancer, skin cancer)
     - Neurological diseases (e.g., stroke, brain tumor)
     - Dermatological issues (e.g., melanoma, eczema, psoriasis)
     - Pulmonary conditions (e.g., pneumonia, tuberculosis, COVID-19)
     - Bone fractures or musculoskeletal disorders
     - Inflammatory or infectious diseases

3. **Output Structure (Use Markdown for formatting)**:
   - **Predicted Condition**: Name the most likely disease or state "Healthy/No abnormality detected".
   - **Confidence Level**: High / Medium / Low (based on visual clarity and confidence in features).
   - **Detailed Findings**: Describe what you see in the image that supports your prediction.
   - **Recommended Action**: Suggest next steps like specific lab tests, clinical examination, or imaging follow-up.
   - **Disclaimer**: Always include the mandatory disclaimer.

4. **Ethical Considerations**:
   - Do NOT provide a definitive diagnosis. Your role is to assist, not replace, a professional.
   - If the image is unclear or not a medical image, state that you cannot perform an analysis.
   - Always include this mandatory warning at the end of your analysis:

---
⚠️ *Disclaimer: This analysis is generated by an AI model and is for informational purposes only. It does not constitute a medical diagnosis. Please consult a certified healthcare professional for an accurate diagnosis and treatment plan.*
"""

# --- Model Configuration (Unchanged) ---
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": HarmCategory.HARM_CATEGORY_HATE_SPEECH, "threshold": HarmBlockThreshold.BLOCK_NONE},
    {"category": HarmCategory.HARM_CATEGORY_HARASSMENT, "threshold": HarmBlockThreshold.BLOCK_NONE},
    {"category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, "threshold": HarmBlockThreshold.BLOCK_NONE},
    {"category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, "threshold": HarmBlockThreshold.BLOCK_NONE},
]

# --- Load Gemini Model (Unchanged) ---
try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
except Exception as e:
    st.error(f"Model initialization error: {e}")
    st.stop()

# --- Streamlit Layout ---
st.markdown(
    "<p style='text-align: center; color: white; text-shadow: 0 1px 2px black;'>Upload a medical image (X-ray, MRI, skin lesion, etc.) to receive an AI-generated preliminary analysis.</p>", 
    unsafe_allow_html=True
)

col1, col2 = st.columns([0.8, 1.2], gap="large")

with col1:
    # --- Lottie Animation ---
    lottie_url = "https://lottie.host/80b5993b-8e5f-4e69-923c-a99f2a7f516d/0cWiaLcYwS.json"
    lottie_json = load_lottieurl(lottie_url)
    
    # Placeholder for uploaded image or Lottie animation
    image_placeholder = st.empty()
    image_placeholder.image("AI Medical Assistant.png", caption="Your Image", use_column_width=True)
    
    if lottie_json:
        with image_placeholder:
            st_lottie(lottie_json, speed=1, height=300, key="initial")

    uploaded_file = st.file_uploader("Choose a medical image...", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        # Display the uploaded image, replacing the animation
        image_placeholder.image(uploaded_file, caption="Your Uploaded Image", use_column_width=True)

    submit = st.button("🔍 Analyze Image")

with col2:
    result_placeholder = st.empty()
    result_placeholder.info("The analysis result will appear here after you upload an image and click 'Analyze'.")

# --- Image Handling & Prediction Logic ---
if submit:
    if uploaded_file:
        with st.spinner("🤖 The AI assistant is analyzing the image... Please wait."):
            try:
                # Read the uploaded file as bytes and convert to a PIL Image
                image_bytes = uploaded_file.read()
                image = Image.open(io.BytesIO(image_bytes))

                # Construct the prompt for the model
                prompt_parts = [
                    system_prompt,
                    image,
                ]

                # Generate content using the model
                response = model.generate_content(prompt_parts)
                
                # Display the result in the right column
                result_placeholder.markdown(response.text, unsafe_allow_html=True)

            except Exception as e:
                st.error("❌ An error occurred during the analysis.")
                # For debugging, show the full traceback in a more readable way
                st.code(traceback.format_exc(), language='python')
    else:
        # Using st.toast for a less intrusive warning
        st.toast("⚠️ Please upload an image first!", icon="📸")


# --- Disclaimer Footer (Unchanged) ---
st.markdown("---")
st.warning("⚠️ *This tool is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.*")
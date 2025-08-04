🩺 AI-Powered Medical Image Diagnostic Assistant
An intelligent web-based diagnostic tool that uses Google Gemini AI to analyze uploaded medical images (X-rays, MRIs, skin lesions, etc.) and provide preliminary AI-assisted insights.


🔍 Features
🧠 Gemini API Integration for advanced medical image understanding.

🖼️ Upload medical images like X-ray, MRI, CT scan, or dermatology photos.

📊 AI-generated condition prediction with confidence level and recommended actions.

🎨 Animated, responsive Streamlit UI with Lottie animations and frosted glass design.

⚠️ Built-in ethical safeguards and medical disclaimers.

🌐 Fully hosted on Render and accessible online.

🚀 Live Demo
🌍 https://ai-medical-soumyadip.onrender.com

📸 Screenshots
Upload Panel	Analysis Panel

🛠️ Technologies Used
streamlit – UI framework

google-generativeai – Gemini API integration

Pillow – Image processing

requests – Lottie animation loading

streamlit-lottie – Lottie animations

🧑‍⚕️ Ethical Disclaimer
⚠️ This application is intended for informational purposes only and does not constitute a medical diagnosis. Please consult a certified healthcare professional for an accurate assessment.

🧰 Setup Instructions
🔗 Clone the repository
bash
Copy
Edit
git clone https://github.com/majisoumya/Ai-Medical-Diagonostic-Assistsnt-.git
cd Ai-Medical-Diagonostic-Assistsnt-
📦 Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
🔑 Add your API Key
Replace this line in main.py with your actual Gemini API Key:

python
Copy
Edit
api_key = "YOUR_API_KEY_HERE"
🔐 You can get a free API key from Google AI Studio.

▶️ Run the app
bash
Copy
Edit
streamlit run main.py
📁 Project Structure
css
Copy
Edit
├── main.py
├── requirements.txt
├── AI Medical Assistant.png
└── README.md


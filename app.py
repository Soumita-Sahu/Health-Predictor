import streamlit as st
import numpy as np
import joblib

# Load models
model_lung = joblib.load('final_random_forest_model.pkl')
model_heart = joblib.load('final_logistic_regression_model.pkl')

# Page config
st.set_page_config(
    page_title="🩺 Health Risk Predictor",
    layout="wide",      # <-- changed from 'centered' to 'wide' to avoid center layout
    page_icon="🩺"
)

st.sidebar.markdown("""
---
📅 **Last updated:** June 2025  
🛠️ **Version:** 1.0.3
""")


# --- Custom CSS ---
# --- Custom CSS with Professional Fonts ---
st.markdown("""
<style>
/* Target the tab labels */
    .stTabs [data-baseweb="tab"] {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #ffffff !important; /* Or any professional color */
        padding: 10px 20px !important;
    }

    /* Highlight selected tab */
    .stTabs [aria-selected="true"] {
        border-bottom: 3px solid #e74c3c !important; /* Active tab underline */
        color: #e74c3c !important; /* Active tab text color */
    }
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Open+Sans:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Open Sans', sans-serif;
    font-size: 18px;
    color: #2E2E2E;
    background-color: #f4f6f8;
}

h1, h2, h3 {
    font-family: 'Inter', sans-serif;
    color: #004080;
    font-weight: 600;
    letter-spacing: 0.02em;
}

.section-heading {
    font-size: 2rem;
    color: #004080;
    margin-top: 50px;
    margin-bottom: 25px;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    border-bottom: 2px solid #e0e0e0;
    padding-bottom: 5px;
}

.header-title {
    font-size: 3.5rem;
    font-weight: 700;
    color: #D72638;
    text-align: center;
    margin-top: 10px;
    margin-bottom: 12px;
    font-family: 'Inter', sans-serif;
}

.header-subtitle {
    font-size: 1.5rem;
    text-align: center;
    color: #555;
    margin-bottom: 35px;
    font-family: 'Open Sans', sans-serif;
}

.stButton>button {
    background-color: #004080;
    color: #fff;
    font-weight: 600;
    padding: 0.6em 1.4em;
    border-radius: 8px;
    border: none;
    transition: 0.3s ease;
}

.stButton>button:hover {
    background-color: #002855;
}

.stTextInput>div>input, .stTextArea>div>textarea {
    background-color: #ffffff;
    border: 1px solid #ccc;
    padding: 0.6em;
    font-size: 1.05rem;
    border-radius: 6px;
}

.chat-box {
    border: 1px solid #D72638;
    border-radius: 10px;
    padding: 15px;
    max-height: 280px;
    overflow-y: auto;
    background-color: #fff8f9;
}

.chat-message-user {
    color: #D72638;
    font-weight: 600;
    margin-bottom: 5px;
}

.chat-message-bot {
    color: #2E2E2E;
    font-style: italic;
    margin-bottom: 10px;
}

.footer-section {
    text-align: center;
    padding: 25px 10px;
    color: #888;
    font-size: 1rem;
    background-color: #f0f0f0;
    margin-top: 40px;
}

.footer-links a {
    color: #888;
    text-decoration: none;
    margin: 0 20px;
    font-weight: 500;
}

.footer-links a:hover {
    color: #D72638;
}
</style>
""", unsafe_allow_html=True)


# --- Sidebar: About Us ---


st.sidebar.header("ℹ️ About Us")

st.sidebar.markdown("""
Final-year students from the **CSE Department** at **Techno Main Salt Lake**, building easy-to-use health prediction tools.
""")

st.sidebar.markdown("### 👥 Team")
st.sidebar.markdown("""

- **Arghyadeep Mondal** (13000121130)  
- **Souvik Mondal** (13000121132)  
- **Soumyadeep Das** (13000121136)
- **Soumita Sahu** (13000121060)  
""")

st.sidebar.markdown("""
### 🎯 Mission  
Provide reliable, simple tools for early health risk detection to encourage proactive care.
""")

st.sidebar.markdown("""
⚠️ *Predictions are statistical and not medical advice. Please consult healthcare professionals.*
""")

st.sidebar.markdown("""
### 📬 Contact  
[healthpredictor@techno.edu](mailto:healthpredictor@techno.edu)
""")



# --- HEADER ---
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');

        .header {
            font-family: 'Montserrat', sans-serif;
            font-size: 2.8rem;
            font-weight: 700;
            color: #2c3e50;  /* dark slate blue */
            text-align: center;
            margin-top: 10px;
            margin-bottom: 5px;
        }

        .subheader {
            font-family: 'Montserrat', sans-serif;
            font-size: 1.4rem;
            font-weight: 500;
            color: #6c7a89;  /* slate gray */
            text-align: center;
            margin-top: 0;
            margin-bottom: 20px;
            letter-spacing: 0.05em;
        }
    </style>

    <h1 class="header">🩺 Health Risk Predictor</h1>
    <p class="subheader">Empowering Your Heart and Lung Health with Smart Insights</p>
    """,
    unsafe_allow_html=True,
)


# Initialize chat history session state if not present (once outside tabs)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Tabs ---

tab_names = [
    "💉 Lung Cancer Prediction",
    "💔 Heart Disease Prediction",
    "🩺 Health Tips",
    "❓ FAQ",
    "📬 Contact & Feedback",
    "🤖 Health Assistant Chat Bot"
]

# Inject CSS to style the tabs font size, padding, and spacing
st.markdown(
    """
    <style>
    /* Target the tabs container */
    div[data-testid="stTabs"] > div {
        font-size: 18px !important;
        font-weight: 600 !important;
        letter-spacing: 0.03em;
        padding: 12px 16px !important;
        min-width: 170px;
    }

    /* Remove hover effect */
    div[data-testid="stTabs"] button:hover {
        background-color: transparent !important;
        color: inherit !important;
    }

    /* Active tab style */
    div[data-testid="stTabs"] button[aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.3);  /* semi-transparent white */
        color: inherit !important;  /* keep text color same */
        font-weight: 700;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



tabs = st.tabs(tab_names)

for i, tab in enumerate(tabs):
    with tab:
        
        if tab_names[i] == "💉 Lung Cancer Prediction":
            st.write("Input your data here to predict lung cancer risk.")
            # Add your lung cancer prediction UI here

        elif tab_names[i] == "💔 Heart Disease Prediction":
            st.write("Input your data here to predict heart disease risk.")
            # Add your heart disease prediction UI here

        elif tab_names[i] == "🩺 Health Tips":
            st.write("Here are some tips to keep your heart and lungs healthy.")
            # Add health tips content here

        elif tab_names[i] == "❓ FAQ":
            st.write("Common questions and answers about heart and lung health.")
            # Add FAQ content here

        elif tab_names[i] == "📬 Contact & Feedback":
            st.write("Contact us or leave your feedback.")
            # Add contact/feedback form here

        elif tab_names[i] == "🤖 Health Assistant Chat Bot":
            st.write("Chat with our assistant for health advice.")
            # Add chatbot UI here


# -------- Tab 1: Lung Cancer Prediction --------
with tabs[0]:
    st.markdown('<h2 style="font-size: 24px; color: #34495e;">🌍 Lung Cancer Prediction</h2>', unsafe_allow_html=True)

    
    age = st.slider("Age", 18, 100, value=30, help="Select your age")
    
    smoking = st.selectbox("Do you smoke?", options=["Select", "Yes", "No"], help="Do you currently smoke?")
    yellow_fingers = st.selectbox("Do you have yellow fingers?", options=["Select", "Yes", "No"], help="Are your fingers yellow-stained?")
    anxiety = st.selectbox("Do you suffer from anxiety?", options=["Select", "Yes", "No"], help="Do you often feel anxious?")
    peer_pressure = st.selectbox("Are you under peer pressure?", options=["Select", "Yes", "No"], help="Do others influence your habits?")
    chronic_disease = st.selectbox("Do you have any chronic disease?", options=["Select", "Yes", "No"], help="Any long-term illnesses?")
    fatigue = st.selectbox("Do you feel fatigued?", options=["Select", "Yes", "No"], help="Do you often feel tired?")
    allergy = st.selectbox("Do you have allergies?", options=["Select", "Yes", "No"], help="Do you have any allergies?")
    wheezing = st.selectbox("Do you experience wheezing?", options=["Select", "Yes", "No"], help="Do you hear wheezing when breathing?")
    alcohol = st.selectbox("Do you consume alcohol?", options=["Select", "Yes", "No"], help="Do you drink alcohol?")
    coughing = st.selectbox("Do you have a persistent cough?", options=["Select", "Yes", "No"], help="Is your cough long-lasting?")
    shortness = st.selectbox("Do you feel shortness of breath?", options=["Select", "Yes", "No"], help="Do you get breathless easily?")
    swallowing = st.selectbox("Do you face difficulty swallowing?", options=["Select", "Yes", "No"], help="Do you have trouble swallowing?")
    chest_pain = st.selectbox("Do you experience chest pain?", options=["Select", "Yes", "No"], help="Do you have any chest pains?")
    weight_loss = st.selectbox("Have you experienced unexplained weight loss?", options=["Select", "Yes", "No"], help="Have you lost weight without trying?")
    
    all_answers = [smoking, yellow_fingers, anxiety, peer_pressure, chronic_disease, fatigue, allergy,
                   wheezing, alcohol, coughing, shortness, swallowing, chest_pain, weight_loss]
    
    if "Select" in all_answers:
        st.info("Please answer all questions above to enable prediction.")
    else:
        if st.button("Predict Lung Cancer Risk"):
            features = np.array([
                age,
                1 if smoking == "Yes" else 0,
                1 if yellow_fingers == "Yes" else 0,
                1 if anxiety == "Yes" else 0,
                1 if peer_pressure == "Yes" else 0,
                1 if chronic_disease == "Yes" else 0,
                1 if fatigue == "Yes" else 0,
                1 if allergy == "Yes" else 0,
                1 if wheezing == "Yes" else 0,
                1 if alcohol == "Yes" else 0,
                1 if coughing == "Yes" else 0,
                1 if shortness == "Yes" else 0,
                1 if swallowing == "Yes" else 0,
                1 if chest_pain == "Yes" else 0,
                1 if weight_loss == "Yes" else 0
            ]).reshape(1, -1)
            
            result = model_lung.predict(features)
            
            if result[0] == 1:
                st.error("⚠️ High risk of Lung Cancer. Please consult a doctor immediately.")
            else:
                st.success("✅ Low risk of Lung Cancer. Keep monitoring your health.")

with tabs[1]:
    st.markdown('<h2 style="font-size: 24px; color: #34495e;">💔 Heart Disease Prediction</h2>', unsafe_allow_html=True)

    age = st.slider("Age", 20, 100, value=20, help="Select your age (20 to 100).")
    
    sex = st.selectbox(
        "Gender",
        options=["Select Gender", "Male", "Female"],
        help="Choose your gender."
    )
    
    cp = st.selectbox(
        "Chest Pain Type",
        options=["Select chest pain type", "Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"],
        help="Select the type of chest pain you experience."
    )
    
    trestbps = st.number_input(
        "Resting Blood Pressure (mm Hg)",
        min_value=90,
        max_value=200,
        value=90,
        help="Enter your resting blood pressure (in mm Hg)."
    )
    
    chol = st.number_input(
        "Serum Cholesterol (mg/dl)",
        min_value=100,
        max_value=400,
        value=100,
        help="Enter your serum cholesterol level (in mg/dl)."
    )
    
    fbs = st.selectbox(
        "Fasting Blood Sugar > 120 mg/dl",
        options=["Select", "Yes", "No"],
        help="Is your fasting blood sugar > 120 mg/dl?"
    )
    
    restecg = st.selectbox(
        "Resting ECG Result",
        options=["Select ECG result", "Normal", "Having ST-T wave abnormality", "Showing probable/definite LV hypertrophy"],
        help="Select the result of your resting ECG."
    )
    
    thalach = st.number_input(
        "Maximum Heart Rate Achieved",
        min_value=60,
        max_value=220,
        value=60,
        help="Enter your maximum heart rate achieved."
    )
    
    exang = st.selectbox(
        "Exercise Induced Angina",
        options=["Select", "Yes", "No"],
        help="Do you experience angina induced by exercise?"
    )
    
    oldpeak = st.slider(
        "Oldpeak",
        0.0, 6.0, 0.0,
        help="ST depression induced by exercise relative to rest."
    )
    
    slope = st.selectbox(
        "Slope of Peak Exercise ST Segment",
        options=["Select slope", "Upsloping", "Flat", "Downsloping"],
        help="Select the slope type of peak exercise ST segment."
    )
    
    ca = st.slider(
        "Number of Major Vessels Colored by Fluoroscopy",
        0, 4, 0,
        help="Number of major vessels colored by fluoroscopy (0–4)."
    )
    
    thal = st.selectbox(
        "Thalassemia",
        options=["Select thalassemia type", "Normal", "Fixed Defect", "Reversible Defect"],
        help="Select your thalassemia status."
    )

    # Check if user has selected valid options in all selectboxes
    required_selects = [sex, cp, fbs, restecg, exang, slope, thal]
    if "Select" in required_selects or "Select Gender" in required_selects or "Select chest pain type" in required_selects or "Select ECG result" in required_selects or "Select slope" in required_selects or "Select thalassemia type" in required_selects:
        st.info("Please fill in all fields correctly to enable prediction.")
    else:
        if st.button("Predict Heart Disease Risk"):
            sex_val = 1 if sex == "Male" else 0
            cp_val = ["Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"].index(cp)
            fbs_val = 1 if fbs == "Yes" else 0
            restecg_val = ["Normal", "Having ST-T wave abnormality", "Showing probable/definite LV hypertrophy"].index(restecg)
            exang_val = 1 if exang == "Yes" else 0
            slope_val = ["Upsloping", "Flat", "Downsloping"].index(slope)
            thal_val = ["Normal", "Fixed Defect", "Reversible Defect"].index(thal)

            input_data = np.array([
                age, sex_val, cp_val, trestbps, chol, fbs_val, restecg_val,
                thalach, exang_val, oldpeak, slope_val, ca, thal_val
            ]).reshape(1, -1)

            result = model_heart.predict(input_data)
            if result[0] == 1:
                st.error("⚠️ High risk of Heart Disease. Please consult a doctor immediately.")
            else:
                st.success("✅ Low risk of Heart Disease. Maintain a healthy lifestyle.")


# -------- Tab 3: Health Tips --------
with tabs[2]:
    st.markdown('<h2 style="font-size: 24px; color: #34495e;">🩺 Health Tips</h2>', unsafe_allow_html=True)

    st.markdown("""
    - 🚭 **Avoid Smoking**: Major risk factor for lung and heart diseases.
    - 🥗 **Eat Balanced Diet**: Rich in fiber, low in saturated fats.
    - 🏃‍♀️ **Exercise Regularly**: At least 30 minutes most days.
    - 🛌 **Sleep Well**: Aim for 7–8 hours of restful sleep.
    - 😌 **Manage Stress**: Try meditation or yoga.
    """)

# -------- Tab 4: FAQ --------
with tabs[3]:
    st.markdown('<h2 style="font-size: 24px; color: #34495e;">❓ Frequently Asked Questions</h2>', unsafe_allow_html=True)

    st.markdown("""
    **Q1:** Is this tool accurate?  
    > This tool uses trained ML models, but it's not a replacement for professional medical advice.

    **Q2:** Can I use this report for medical treatment?  
    > No. It is for awareness and should be shown to a doctor for further advice.

    **Q3:** How often should I check?  
    > Once every 6–12 months or as recommended by a doctor.
    """)

# -------- Tab 5: Contact & Feedback --------
with tabs[4]:
    st.markdown('<h2 style="font-size: 24px; color: #34495e;">📬 Contact & Feedback</h2>', unsafe_allow_html=True)

    contact_name = st.text_input("Your Name")
    contact_email = st.text_input("Your Email")
    contact_msg = st.text_area("Your Feedback or Message")
    if st.button("📨 Submit Feedback"):
        if contact_name and contact_email and contact_msg:
            st.success("Thank you for your feedback! We'll get back to you soon.")
        else:
            st.error("Please fill out all fields before submitting.")

# -------- Tab 6: Health Assistant Chat Bot --------
with tabs[5]:
    st.markdown('<h2 style="font-size: 24px; color: #34495e;">🤖 Health Assistant Chat Bot</h2>', unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # --- PROCESS CHAT BEFORE DISPLAY ---
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message here and press Enter to submit:", key="chat_input")
        submitted = st.form_submit_button("Send")

    if submitted and user_input:
        st.session_state.chat_history.append(("user", user_input))
        msg_lower = user_input.lower()

        if "lung" in msg_lower:
            bot_reply = (
                "For lung health, avoid smoking, reduce pollution exposure, "
                "and practice breathing exercises like pranayama."
            )
        elif "heart" in msg_lower:
            bot_reply = (
                "For a healthy heart, eat a balanced diet low in saturated fats, "
                "exercise regularly, and manage stress."
            )
        elif "diet" in msg_lower or "nutrition" in msg_lower:
            bot_reply = (
                "A heart- and lung-friendly diet includes fruits, vegetables, "
                "whole grains, lean proteins, and limits processed foods and salt."
            )
        elif "meditate" in msg_lower or "meditation" in msg_lower:
            bot_reply = (
                "Meditation reduces stress and benefits heart and lung health. "
                "Try 10-20 minutes daily."
            )
        elif "exercise" in msg_lower or "workout" in msg_lower:
            bot_reply = (
                "Regular exercise strengthens your heart and lungs. Aim for 150 minutes weekly."
            )
        elif "restriction" in msg_lower or "health restriction" in msg_lower:
            bot_reply = (
                "Follow your doctor's advice for any activity or diet restrictions."
            )
        elif "hello" in msg_lower or "hi" in msg_lower:
            bot_reply = "Hello! How can I assist you with your lung or heart health?"
        elif "thank" in msg_lower:
            bot_reply = "You're welcome! Ask me anything about lung or heart health."
        else:
            bot_reply = (
                "I'm here to help with lung and heart health questions — "
                "like diet, exercise, meditation, and restrictions."
            )

        st.session_state.chat_history.append(("bot", bot_reply))

    # --- CHAT DISPLAY STYLES ---
    st.markdown("""
    <style>
        .chat-container {
            max-height: 350px;
            overflow-y: auto;
            padding-right: 10px;
            border: 1px solid #ccc;
            border-radius: 10px;
            background-color: #f9f9f9;
            margin-bottom: 15px;
        }
        .chat-message-user {
            background-color: #e3f2fd;
            padding: 10px;
            border-radius: 10px;
            margin: 5px;
            color: #0d47a1;
        }
        .chat-message-bot {
            background-color: #fce4ec;
            padding: 10px;
            border-radius: 10px;
            margin: 5px;
            color: #880e4f;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- DISPLAY CHAT HISTORY ABOVE INPUT ---
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for sender, message in st.session_state.chat_history:
        if sender == "user":
            st.markdown(f'<div class="chat-message-user">🧑‍💬 You: {message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message-bot">🤖 Bot: {message}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)



# --- Footer ---
st.markdown("---", unsafe_allow_html=True)
st.markdown("""
    <style>
        .footer-container {
            background-color: #0e1117;
            padding: 20px 0;
            text-align: center;
            font-size: 15px;
            color: #bbb;
        }
        .footer-links span {
            margin: 0 10px;
            color: #bbb;
            transition: color 0.3s ease;
            cursor: default;
        }
        .footer-links span:hover {
            color: #1E90FF;
        }
    </style>

    <div class="footer-container">
        <div style="margin-bottom: 10px;">
            <b style="color: #ffffff;">Health Risk Predictor</b> — A Final Year Project by Students of 
            <span style="color: #ffffff;">Techno Main Salt Lake, CSE Dept.</span>
        </div>
        <div>
            © 2025 Soumyadeep Das, Arghyadeep Mondal, Souvik Mondol, Soumita Sahu · All rights reserved.
        </div>
        <div class="footer-links" style="margin-top: 10px;">
            <span>📩 Contact Us</span> | <span>💬 Live Chat</span> | <span>📄 FAQ</span>
        </div>
    </div>
""", unsafe_allow_html=True)



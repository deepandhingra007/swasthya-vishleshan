import streamlit as st
import google.generativeai as genai
import pathlib
import requests


genai.configure(api_key="AIzaSyBjLgNEzTt219-kVgsAnAQmvLpWaxMPEzY")
model = genai.GenerativeModel('gemini-2.0-flash')
st.set_page_config(layout = "wide")
st.markdown("""
        <style>
               .block-container {
                    padding-top: 3rem;
                    padding-bottom: 0rem;
                    padding-left: 2rem;
                    padding-right: 2rem;
                }
        </style>
        """, unsafe_allow_html=True)

languages = {
    'English': 'English',
    'हिन्दी': 'Hindi',
    'Español': 'Spanish',
    'Français': 'French',
    'Deutsch': 'German',
    'ਪੰਜਾਬੀ': 'Punjabi',
    'ગુજરાતી': 'Gujarati',
    'मराठी': 'Marathi',
    'தமிழ்': 'Tamil',
    'తెలుగు': 'Telugu',
    'বাংলা': 'Bengali',
    'ಕನ್ನಡ': 'Kannada',
    'മലയാളം': 'Malayalam',
    'اردو': 'Urdu',
    'ଓଡ଼ିଆ': 'Odia',
    'العربية': 'Arabic',
    '中文': 'Chinese',
    '日本語': 'Japanese',
    '한국어': 'Korean',
    'Русский': 'Russian',
    'Italiano': 'Italian',
    'Nederlands': 'Dutch',
    'Português': 'Portuguese',
    'Türkçe': 'Turkish'
}

col1, col2 = st.columns([1, 3])

with col2:
    selected_language = st.selectbox("Select Language", options=list(languages.keys()), key="language_select", label_visibility="collapsed")
    st.markdown(
        """
        <style>
        div[data-testid="stSelectbox"] {
            width: 150px;
            float: right;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

if 'selected_language' not in locals():
    selected_language = "English"

with col1:
    if "about_creator_clicked" not in st.session_state:
        st.session_state.about_creator_clicked = False

    if st.button("About Creator", key="about_creator"):
        st.session_state.about_creator_clicked = not st.session_state.about_creator_clicked

    if st.session_state.about_creator_clicked:
        t_intro="Introducing Swasthya Vishleshan Created by Deepan Kumar, a visionary data enthusiast,Swasthya Vishleshan is an innovative AI-powered application designed to revolutionize health report analysis.With a mission to simplify complex health data & to breaks language barriers by offering insights in regional languages.This ensures that everyone, regardless of their linguistic background,can better understand their health reports and make informed decisions.Built with care and creativity, this app is for the people. https://www.linkedin.com/in/deepandhingra007"
        if selected_language != "English":
            prompt= "Translate this text into "+selected_language+" Language & provide result in minimal words:"+t_intro
            response = model.generate_content(prompt)
            t_intro=response.text
        st.sidebar.write("🌟"+ t_intro)
        #st.sidebar.write("Fuel my creativity with a cup of coffee 🍵")
        st.sidebar.image("https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png", width=150,)
        # URL
        # iamge ID
        file_id = "16cdOT6JrMa7-90wHl6gR2LNRc9uuUC9t"

        # URL
        QR_url = f"https://drive.google.com/uc?export=view&id={file_id}"
        response = requests.get(QR_url)
        st.sidebar.write("UPI:")
        st.sidebar.image(response.content, width=250)
        st.sidebar.write("Paypal: deepandhingra007@gmail.com")
    else:
        st.session_state.about_creator_clicked = False


t0="Welcome to Swasthya Vishleshan Application👋"
if selected_language != "English":
    prompt= "Translate this text into "+selected_language+" Language & provide result in minimal words but do not change this word 'Swasthya Vishleshan' but chage the script in converted language:"+t0
    response = model.generate_content(prompt)
    t0=response.text
st.title(t0)


t1="- A Healthcare Analytics App"

if selected_language != "English":
    prompt= "Translate this text into "+selected_language+" Language & provide result in minimal words :"+t1
    response = model.generate_content(prompt)
    t1=response.text

st.markdown(f"<h1 style='font-size:20px; text-align:left; margin-left:0;padding-top: 0;'>{t1}</h1>", unsafe_allow_html=True)

t2=""" 
Welcome to Swasthya Vishleshan Your health insights, simplified!

Swasthya Vishleshan is your go-to platform for analyzing health reports with ease and accuracy. Upload your health documents, and let our app process and present vital information in a simple and clear format. Whether you're tracking progress, understanding medical terms, or seeking actionable insights, Swasthya Vishleshan has you covered.

Stay informed, stay healthy.
    """

if selected_language != "English":
    prompt= "Translate this text into "+selected_language+" Language & provide result in minimal words :"+t2
    response = model.generate_content(prompt)
    t2=response.text

st.markdown(f"<h1 style='font-size:14px; text-align:left; margin-left:0;padding-top: 0;'>{t2}</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your report here: (Only PDF file Acceptable)", type=["pdf"])

if uploaded_file is not None:
    try:
        filepath = pathlib.Path(uploaded_file.name)
        st.success("File uploaded successfully!")
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        report_check_prompt = "Check if this document is a medical report then return True otherwise False and give me a one word answer please"
        response = model.generate_content(
            contents=[
                {
                    "data": filepath.read_bytes(),
                    "mime_type": "application/pdf"
                },
                report_check_prompt
            ]
        )
        
        if "True" in response.text:
            report_format_prompt = """Analyze the report to identify the owner, date, medical tests performed, their results, precautions for unsatisfactory tests,Anticipated symptoms or Foreseeable signs that person can have,Home Remedies, suggest if the person needs to contact a doctor, and present the summarise results in Non-technical terms for easy & Better understanding.

        Output should be like this & do not add content like (Okay, here is an analysis of the provided medical report, structured for clarity and understanding)   :

        1. Report Ownership and Date
            - Owner: CAN WINN FOUNDATION, patient name Divya Arora.
            - Report Date:** February 11, 2025

        2. Medical Tests Performed
        This report covers a comprehensive range of tests:
            - Liver Function Test (LFT): Evaluates the health and function of the liver.
            -   Urine Routine & Microscopy Extended: Analyzes the physical, chemical, and microscopic components of urine.
            - Erythrocyte Sedimentation Rate (ESR): Measures inflammation in the body.
            - Malaria Parasite (MP): Detects the presence of malaria parasites in the blood.
            - Complete Blood Count (CBC): Provides a detailed count and analysis of blood cells.
            - WIDAL Test (Slide Method): Detects antibodies related to typhoid fever.
            - Typhoid IgM antibody:** Detects IgM antibodies to S. typhi (typhoid fever).

        3. Test Results and Interpretation
        Here's a summary of the key findings, separated by test category:
            - Liver Function Test (LFT):
                - Aspartate Aminotransferase (AST/SGOT): Elevated at 60.60 U/L (Reference Range: 3-35 U/L)
                - Alanine Aminotransferase (ALT/SGPT): Elevated at 70.4 U/L (Reference Range: 3-35 U/L)
                - Gamma Glutamyl Transferase (GGT): Elevated at 109.1 U/L (Reference Range: 5-38 U/L)
            - Urine Routine & Microscopy Extended: All test results are within normal limits.
            - Erythrocyte Sedimentation Rate (ESR): ESR is within normal limits.
            - Malaria Parasite (MP): No malaria parasites were detected.
            - Complete Blood Count (CBC): All test results are within normal limits.
            - WIDAL Test (Slide Method): No agglutination was detected for Salmonella Typhi-O Antigen, Salmonella Typhi-H Antigen, Salmonella Paratyphi – AH Antigen, and Salmonella Paratyphi - BH Antigen.
            - Typhoid IgM antibody: Result is negative.

        4. Probable Symptoms
            Elevated liver enzymes can indicate liver inflammation or damage. Some potential symptoms associated with this include:
                - Fatigue
                - Weakness
                - Loss of appetite
                - Nausea
                - Abdominal pain (especially in the upper right quadrant)
                - Jaundice (yellowing of the skin and eyes)
                - Dark urine
                - Pale stools

        5. Home Remedies
            - Liver Health: Reduce or eliminate alcohol consumption and processed foods. Increase intake of fruits, vegetables, and lean proteins.
            - General Wellness: Maintain a healthy diet, stay hydrated, and get enough rest.

        6. Need to Contact a Doctor?
           Yes, given the elevated levels of some liver enzymes, it's important to contact a doctor to investigate the cause. If symptoms persist over time, it's highly advisable to consult a doctor.

        7. Report's Results in Simple Language """

            response = model.generate_content(
                contents=[
                    {
                        "data": filepath.read_bytes(),
                        "mime_type": "application/pdf"
                    },
                    report_format_prompt
                ]
            )
            t3=response.text

            if selected_language != "English":
                prompt= "Translate this text into "+selected_language+" Language:"+t3
                response = model.generate_content(prompt)
            t3=response.text

            st.markdown(f"<h1 style='font-size:11px; text-align:left; margin-left:0;padding-top: 0;'>{t3}</h1>", unsafe_allow_html=True)
        
        else:
            st.error("The uploaded document is not a medical report.")
        
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.warning("Please upload a PDF file to proceed.")


Important_NOTE="**Important Note:** This analysis is for informational purposes only and should not substitute professional medical advice. A healthcare provider should always be consulted for diagnosis and treatment."
st.markdown(f"<h1 style='font-size:15px; text-align:left; margin-left:0;padding-top: 0; color:red;'>{Important_NOTE}</h1>", unsafe_allow_html=True)


# Adding a footer
footer = """
<div style='text-align: center; padding: 10px; color: gray;'>
    © 2025 Swasthya Vishleshan. All rights reserved.
</div>
"""

st.markdown(footer, unsafe_allow_html=True)




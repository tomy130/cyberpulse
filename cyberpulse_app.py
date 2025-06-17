# CyberPulse: AI-Powered Cybersecurity Risk Assessment Tool
# Built by Thomas W. – CyberPulse, 2025

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from fpdf import FPDF

# Sample scoring logic (replace with ML model later)
def calculate_risk_score(inputs):
    score = 100
    risk_factors = []

    if inputs['MFA'] == 'No':
        score -= 15
        risk_factors.append(('No MFA', 'Enable MFA on all key accounts.'))
    if inputs['Backups'] in ['Never', 'Rarely']:
        score -= 20
        risk_factors.append(('No Regular Backups', 'Schedule automatic weekly backups using Google Drive or OneDrive.'))
    if inputs['Incident Response Plan'] == 'No':
        score -= 20
        risk_factors.append(('No Incident Response Plan', 'Use this basic IR plan:\n1. Identify\n2. Contain\n3. Eradicate\n4. Recover\n5. Notify\n6. Improve'))
    if inputs['Software Updates'] in ['Rarely', 'Never']:
        score -= 15
        risk_factors.append(('Unpatched Software', 'Enable auto-updates or check monthly.'))
    if inputs['WiFi Security'] == 'Weak':
        score -= 10
        risk_factors.append(('Weak Wi-Fi Security', 'Use WPA3 encryption and a strong password.'))

    score = max(0, min(100, score))
    return score, risk_factors

# Streamlit UI
st.set_page_config(page_title="CyberPulse", layout="centered")
st.title("CyberPulse: Small Business Cyber Risk Report")
st.markdown("Built by Thomas W. – CyberPulse, 2025")

st.header("🔒 Cybersecurity Self-Check")
st.write("Answer the following questions to get your CyberPulse Score and personalized security recommendations.")

# Input form
with st.form("cyber_form"):
    business_size = st.selectbox("Business size:", ['1–10', '11–50', '51–100'])
    mfa = st.selectbox("Do you use Multi-Factor Authentication (MFA)?", ['Yes', 'No'])
    backups = st.selectbox("How often do you back up data?", ['Daily', 'Weekly', 'Monthly', 'Rarely', 'Never'])
    ir_plan = st.selectbox("Do you have an Incident Response Plan?", ['Yes', 'No'])
    software = st.selectbox("How often do you update software?", ['Weekly', 'Monthly', 'Rarely', 'Never'])
    wifi = st.selectbox("How secure is your Wi-Fi password?", ['Strong', 'Medium', 'Weak'])
    submitted = st.form_submit_button("Generate Report")

if submitted:
    user_inputs = {
        'Business Size': business_size,
        'MFA': mfa,
        'Backups': backups,
        'Incident Response Plan': ir_plan,
        'Software Updates': software,
        'WiFi Security': wifi
    }

    score, issues = calculate_risk_score(user_inputs)

    st.subheader("🧠 CyberPulse Score: ")
    if score >= 80:
        st.success(f"Your score is {score}/100 – Low Risk")
    elif score >= 50:
        st.warning(f"Your score is {score}/100 – Moderate Risk")
    else:
        st.error(f"Your score is {score}/100 – High Risk")

    st.subheader("📋 Personalized Recommendations:")
    for issue, fix in issues:
        st.markdown(f"**{issue}**: {fix}")

    # Generate PDF report
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="CyberPulse Risk Report", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Score: {score}/100", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, txt="Issues Found & Suggestions:", ln=True)
    for issue, fix in issues:
        pdf.multi_cell(0, 10, txt=f"- {issue}: {fix}")
    pdf.output("CyberPulse_Report.pdf")

    with open("CyberPulse_Report.pdf", "rb") as f:
        st.download_button("📄 Download PDF Report", f, file_name="CyberPulse_Report.pdf")

import streamlit as st
import fitz

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("📄 AI Resume Analyzer")
st.write("Upload your Resume and Job Description to calculate ATS score.")

def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.lower()

skills_list = [
    "python","java","c","sql","html","css","javascript","machine learning",
    "deep learning","nlp","tensorflow","keras","pandas","numpy","power bi",
    "flask","opencv","streamlit"
]

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])

if resume_file and jd_file:
    resume_text = extract_text(resume_file)
    jd_text = extract_text(jd_file)

    resume_skills = set([s for s in skills_list if s in resume_text])
    jd_skills = set([s for s in skills_list if s in jd_text])

    match = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    score = int((len(match) / len(jd_skills)) * 100) if jd_skills else 0

    st.subheader("🧠 Resume Skills Detected")
    st.write(list(resume_skills))

    st.subheader("💼 Job Skills Detected")
    st.write(list(jd_skills))

    st.subheader("✅ ATS Score & Analysis")
    st.write("Matching Skills:", match)
    st.write("Missing Skills:", list(missing))
    st.metric("ATS Score", f"{score} / 100")

    st.subheader("💡 Suggested Skills to Learn")
    st.write(list(missing))

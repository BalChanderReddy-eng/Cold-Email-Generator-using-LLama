import streamlit as st

# -------------------- DEBUG WRAPPER --------------------
try:
    from langchain_community.document_loaders import WebBaseLoader
    from chains import Chain
    from utils import clean_text, extract_text_from_pdf

    st.write("✅ Imports OK!")

except Exception as e:
    st.error(f"❌ Error loading app: {e}")
    st.stop()  # Stop further execution if imports fail
# -------------------------------------------------------

# -------------------- Optional USER_AGENT --------------------
import os
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
# ------------------------------------------------------------

# Your original Streamlit code starts here
def create_streamlit_app(chain):
    st.title("📧 Cold Mail Generator")

    url_input = st.text_input("Enter a Job URL:", value="")
    uploaded_file = st.file_uploader("Upload your Resume (PDF):", type="pdf")

    if st.button("Analyze & Generate Email"):
        if not url_input:
            st.error("⚠️ Please enter a job URL.")
            return

        if not uploaded_file:
            st.error("⚠️ Please upload a resume.")
            return

        try:
            loader = WebBaseLoader([url_input])
            job_text = clean_text(loader.load().pop().page_content)

            jobs = chain.extract_jobs(job_text)
            if not jobs:
                st.error("⚠️ No job postings found in the given URL.")
                return

            job = jobs[0]

            st.subheader("📝 Extracted Job Details")
            st.write(f"**Role:** {job.get('role', 'N/A')}")
            st.write(f"**Experience:** {job.get('experience', 'N/A')}")
            st.write(f"**Skills Required:** {', '.join(job.get('skills', []))}")
            st.write(f"**Job Description:** {job.get('description', 'N/A')}")

            resume_text = extract_text_from_pdf(uploaded_file)
            resume_skills = chain.extract_skills(resume_text)

            job_skills = job.get("skills", [])
            match_score = chain.calculate_match_score(resume_skills, job_skills)

            st.subheader("📊 Resume Match Score")
            st.write(f"**{match_score:.1f}%**")

            if match_score < 40:
                st.error("❌ Not fit for the job. Consider updating your resume.")
            elif 50 <= match_score < 60:
                st.warning("⚠️ Resume needs improvements. Modify your skills.")
            else:
                st.success("✅ Good fit! Generating cold email...")
                email = chain.write_mail(job, links=[])
                st.subheader("📧 Generated Cold Email")
                st.code(email, language="markdown")

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain)

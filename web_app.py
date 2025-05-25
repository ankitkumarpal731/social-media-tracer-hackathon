import streamlit as st
from app.main import run_trace
from app.utils.graph_generator import generate_graph
from app.utils.pdf_report import create_pdf
import streamlit.components.v1 as components
import subprocess

# Page settings
st.set_page_config(page_title="Social Media Tracer", page_icon="🔍", layout="centered")
st.title("🔍 Social Media Tracer Tool")
st.caption("Built for CyberHackathon 2025 by Ankit Kumar Pal")

# Scan mode selector
st.markdown("### 🔍 Choose Scan Mode:")
scan_mode = st.radio("Select mode:", ["Quick Scan (Fast)", "Deep Scan (Sherlock)", "Deep Scan (Maigret)"])

# Input field
user_input = st.text_input("Enter Email or Phone:")

if user_input:
    input_type = "email" if "@" in user_input else "phone"
    result = run_trace(input_type, user_input)

    st.subheader("📋 Basic Trace Result")
    st.write(f"**Input Type:** {input_type.capitalize()}")
    st.write(f"**Input Value:** `{result['input']}`")
    st.write(f"**Valid:** {'✅ Yes' if result['valid'] else '❌ No'}")

    if result["valid"]:
        # Platform matches
        if result["platform_matches"]:
            st.markdown("### ✅ Platform Matches:")
            for match in result["platform_matches"]:
                st.markdown(f"""
                - 🌐 **Platform**: {match['platform'].capitalize()}
                - 🔗 [Profile URL]({match['profile_url']})
                - 🧠 **Confidence**: `{match['confidence']}%`
                """)

            # Graph
            graph_path = generate_graph(result['input'], result['platform_matches'], "graph.html")
            st.subheader("📌 Visual Graph")
            with open(graph_path, 'r', encoding='utf-8') as f:
                graph_html = f.read()
            components.html(graph_html, height=550)

            # PDF Export
            if st.button("📄 Download PDF Report"):
                pdf_path = create_pdf(result)
                with open(pdf_path, "rb") as f:
                    st.download_button("📥 Download PDF", f, file_name="trace_report.pdf")
        else:
            st.info("ℹ️ No platform matches found.")

        # Deep Scan - Sherlock
        if scan_mode == "Deep Scan (Sherlock)":
            st.subheader("🕵️ Deep Scan (Sherlock Results)")
            username = user_input.split("@")[0] if "@" in user_input else user_input[-10:]
            sherlock_cmd = f"python -m sherlock_project {username} --print-found"

            with st.spinner("Running Sherlock..."):
                try:
                    output = subprocess.check_output(sherlock_cmd, shell=True, text=True, stderr=subprocess.STDOUT)
                    st.code(output, language="bash")
                except subprocess.CalledProcessError as e:
                    st.error("❌ Sherlock failed.")
                    st.text(e.output)

        # Deep Scan - Maigret
        elif scan_mode == "Deep Scan (Maigret)":
            st.subheader("🕵️ Deep Scan (Maigret Results)")
            maigret_cmd = f"maigret {user_input.split('@')[0]} --no-color --no-progressbar --top-sites 10"

            with st.spinner("Running Maigret..."):
                try:
                    output = subprocess.check_output(maigret_cmd, shell=True, stderr=subprocess.STDOUT)
                    output = output.decode('utf-8', errors='replace')
                    st.code(output, language="bash")
                except subprocess.CalledProcessError as e:
                    st.error("❌ Maigret failed.")
                    st.text(e.output.decode('utf-8', errors='replace'))

    elif user_input.strip() != "":
        st.warning("⚠️ Invalid input. Please enter a valid email or phone number.")

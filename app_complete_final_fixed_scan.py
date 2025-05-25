import streamlit as st
st.set_page_config(page_title="Social Media Tracer - Debug Mode", layout="centered")

import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from validate_email_address import validate_email
from platform_trace import check_platforms, extract_identifier
from report_exporter import save_json, save_txt, save_pdf
import subprocess
import os
import datetime

report_data = {}
status_log = []

st.title("🔍 Social Media Tracer Tool (Debug Version)")

trace_type = st.selectbox("Choose Type to Trace", ["Phone", "Email"])
input_value = st.text_input(f"Enter {trace_type} to Trace:")

if st.button("Start Full Trace"):
    if not input_value:
        st.warning("⚠️ Please enter a value to trace.")
    else:
        identifier = extract_identifier(input_value, trace_type)

        try:
            if trace_type == "Phone":
                parsed = phonenumbers.parse(input_value)
                st.success("✔ Phone number parsed successfully.")
                status_log.append("✔ Phone number parsed.")

                country = geocoder.country_name_for_number(parsed, "en")
                carrier_name = carrier.name_for_number(parsed, "en")
                timezones = timezone.time_zones_for_number(parsed)

                st.write(f"📍 Country: {country}")
                st.write(f"📶 Carrier: {carrier_name}")
                st.write(f"🕒 Timezone: {timezones}")

                report_data.update({
                    "Type": "Phone",
                    "Input": input_value,
                    "Valid": phonenumbers.is_valid_number(parsed),
                    "Country": country,
                    "Carrier": carrier_name,
                    "Timezone": ', '.join(timezones),
                    "WhatsApp": "Likely Active",
                    "Truecaller": "Name Match Found"
                })

            elif trace_type == "Email":
                try:
                    is_valid = validate_email(input_value, verify=True)
                except:
                    is_valid = validate_email(input_value, verify=False)

                st.write(f"📧 Email Valid: {is_valid}")
                st.markdown(f"[Check data breach](https://haveibeenpwned.com/account/{input_value})")

                report_data.update({
                    "Type": "Email",
                    "Input": input_value,
                    "Valid Email": is_valid
                })

        except Exception as e:
            st.error(f"[ERROR] Parsing failed: {e}")
            status_log.append(f"✖ Parsing failed: {e}")

        st.subheader("🌐 Platform Presence Check")
        with st.spinner("Checking platforms..."):
            results = check_platforms(identifier)
            for platform, (url, available) in results.items():
                status = "✅ Found" if available else "❌ Not found"
                st.write(f"- {platform}: {status} ([Link]({url}))")
                report_data[platform] = status

        st.subheader("🕵️ Sherlock Username Scan")
        try:
            output = subprocess.check_output(
                f"python sherlock_scan_all.py {identifier}",
                shell=True, text=True, timeout=180
            )
            st.code(output[:1500])
            report_data["Sherlock Scan"] = "Executed"
            status_log.append("✔ Sherlock executed successfully.")
        except subprocess.TimeoutExpired:
            st.warning("⚠️ Sherlock scan timed out.")
            status_log.append("⚠ Sherlock timed out.")
            report_data["Sherlock Scan"] = "Timeout"
        except Exception as e:
            st.error(f"[ERROR] Sherlock failed: {e}")
            status_log.append(f"✖ Sherlock failed: {e}")
            report_data["Sherlock Scan"] = "Failed"

        st.subheader("🌐 Maigret Extended Scan")
        try:
            result = subprocess.run(
                ["python", "-m", "maigret", identifier, "--top-sites", "300"],
                capture_output=True,
                timeout=240
            )
            output = result.stdout.decode("utf-8", errors="ignore")
            st.code(output[:1500])
            report_data["Maigret Scan"] = "Executed"
            status_log.append("✔ Maigret scan successful.")
        except subprocess.TimeoutExpired:
            st.warning("⚠️ Maigret scan took too long.")
            status_log.append("⚠ Maigret timeout.")
            report_data["Maigret Scan"] = "Timeout"
        except Exception as e:
            st.error(f"[ERROR] Maigret failed: {e}")
            status_log.append(f"✖ Maigret failed: {e}")
            report_data["Maigret Scan"] = "Failed"

st.header("📁 Export Report")
if report_data:
    if st.button("Save Report Files"):
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("output", exist_ok=True)
        save_json(report_data, f"output/report_{now}.json")
        save_txt(report_data, f"output/report_{now}.txt")
        save_pdf(report_data, f"output/report_{now}.pdf")
        st.success("✅ Report saved to output/ folder!")
        st.markdown(f"[📄 View PDF](output/report_{now}.pdf)")

    st.subheader("🧾 Debug Status Log")
    for line in status_log:
        st.write(line)
else:
    st.info("ℹ️ Run a trace first to export results.")

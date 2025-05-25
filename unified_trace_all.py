import subprocess
import sys
import os

def run_sherlock(username):
    sherlock_path = os.path.join(os.getcwd(), "sherlock", "sherlock.py")
    if not os.path.exists(sherlock_path):
        print("Sherlock not found.")
        return
    try:
        print(f"🔎 Sherlock full scan for: {username}")
        subprocess.run(["python", sherlock_path, username], check=True)
    except Exception as e:
        print(f"❌ Sherlock error: {e}")

def run_maigret(username):
    try:
        print(f"🌐 Maigret full scan for: {username}")
        result = subprocess.run(["maigret", username, "--print-found"], capture_output=True, text=True, timeout=240)
        print(result.stdout[:3000])
    except Exception as e:
        print(f"❌ Maigret error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python unified_trace.py <username_or_email>")
    else:
        user_input = sys.argv[1]
        run_sherlock(user_input)
        run_maigret(user_input)

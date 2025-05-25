from app.trace.email_trace import trace_email
from app.trace.phone_trace import trace_phone

def run_trace(input_type, value):
    if input_type == "email":
        return trace_email(value)
    elif input_type == "phone":
        return trace_phone(value)
    else:
        return {"error": "Invalid input type"}

# app/trace/email_trace.py

from validate_email_address import validate_email
from app.utils.logger import logger




def trace_email(email):
    logger.info(f"Tracing email: {email}")

    result = {
        "input": email,
        "type": "email",
        "valid": False,
        "platform_matches": []
    }

    # Step 1: Validate email
    is_valid = validate_email(email, verify=False)
    result["valid"] = is_valid

    if not is_valid:
        logger.warning(f"Invalid email: {email}")
        return result

    # Step 2: Check dummy platforms (replace with Sherlock/Maigret logic later)
    dummy_platforms = ["facebook", "instagram", "twitter"]
    for platform in dummy_platforms:
        profile_url = f"https://{platform}.com/{email.split('@')[0]}"
        match = {
            "platform": platform,
            "matched": True,
            "profile_url": profile_url,
            "confidence": 75
        }
        result["platform_matches"].append(match)

    return result

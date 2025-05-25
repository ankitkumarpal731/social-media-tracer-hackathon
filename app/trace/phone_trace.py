# app/trace/phone_trace.py

import phonenumbers
from app.utils.logger import logger




def trace_phone(phone):
    logger.info(f"Tracing phone number: {phone}")

    result = {
        "input": phone,
        "type": "phone",
        "valid": False,
        "platform_matches": []
    }

    # Step 1: Validate and parse number
    try:
        parsed = phonenumbers.parse(phone, None)
        if phonenumbers.is_valid_number(parsed):
            result["valid"] = True
        else:
            logger.warning("Invalid phone number")
            return result
    except Exception as e:
        logger.error(f"Phone parsing error: {e}")
        return result

    # Step 2: Dummy matches (later replace with Truecaller/Telegram etc.)
    dummy_platforms = ["whatsapp", "telegram", "truecaller"]
    for platform in dummy_platforms:
        match = {
            "platform": platform,
            "matched": True,
            "profile_url": f"https://{platform}.com/{phone[-6:]}",
            "confidence": 70
        }
        result["platform_matches"].append(match)

    return result

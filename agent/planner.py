def plan(user_text, memory):
    if "అర్హత" in user_text or "రైతు" in user_text:
        return "CHECK_ELIGIBILITY"

    return "ANSWER_QUESTION"

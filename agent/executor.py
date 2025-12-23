def execute(action, user_text, tools, memory):
    if action == "CHECK_ELIGIBILITY":
        return tools["eligibility"](memory)

    if action == "ANSWER_QUESTION":
        return tools["qa"](user_text)

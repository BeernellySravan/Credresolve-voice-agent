from difflib import SequenceMatcher
from data.qa_dataset import QA_DATASET


def qa_tool(user_text):
    best_score = 0
    best_answer = None

    for item in QA_DATASET:
        score = SequenceMatcher(None, user_text, item["question"]).ratio()
        if score > best_score:
            best_score = score
            best_answer = item["answer"]

    if best_score > 0.5:
        return best_answer

    return "క్షమించండి, ఈ ప్రశ్నకు సమాధానం కనుగొనలేకపోయాను."


def eligibility_tool(memory):
    if memory.get("occupation") == "farmer":
        return "మీరు రైతు భరోసా మరియు PM-Kisan పథకాలకు అర్హులు."
    return "అర్హత నిర్ధారించడానికి మరిన్ని వివరాలు అవసరం."

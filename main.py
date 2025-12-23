from speech.tts import speak
from speech.stt import speech_to_text_push_to_talk

from agent.memory import Memory
from agent.planner import plan
from agent.executor import execute
from agent.evaluator import evaluate

from tools.tools import qa_tool, eligibility_tool


memory = Memory()

tools = {
    "qa": qa_tool,
    "eligibility": eligibility_tool
}

welcome = "“నమస్తే! ప్రభుత్వ సంక్షేమ పథకాలపై మార్గదర్శక సమాచారం అందించే ఈ సేవకు స్వాగతం. దయచేసి మీరు మాట్లాడవచ్చు.”"
print(" AI:", welcome)
speak(welcome)

while True:
    user_text = speech_to_text_push_to_talk()
    if user_text == "":
        continue

    print(" User:", user_text)

    if "చాలు" in user_text:
        speak("ధన్యవాదాలు. మళ్ళీ కలుద్దాం.")
        break

    # memory update example
    if "రైతు" in user_text:
        memory.update("occupation", "farmer")

    action = plan(user_text, memory)
    result = execute(action, user_text, tools, memory)
    final_answer = evaluate(result)

    print(" AI:", final_answer)
    speak(final_answer)

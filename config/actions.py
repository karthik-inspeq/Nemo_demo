from typing import Optional
import os
from dotenv import load_dotenv
from nemoguardrails.actions import action
from inspeq.client import InspeqEval
load_dotenv()

@action(is_system_action=True)
async def check_blocked_terms(context: Optional[dict] = None):
    bot_response = context.get("bot_message")

    # A quick hard-coded list of proprietary terms. You can also read this from a file.
    proprietary_terms = ["proprietary", "proprietary1", "proprietary2"]

    for term in proprietary_terms:
        if term in bot_response.lower():
            return True

    return False
# mesures toxicity based on inspeq metrics
@action(is_system_action=True)
async def toxicity_inspeq(context: Optional[dict] = None):
    bot_response = context.get("bot_message")
    final_result = inspeq_result(bot_response)
    if final_result == "FAILED":
        return True

    return False
# Define toxicity using inspeq metric
def inspeq_result(response):
    metrics_list = [
        "TOXICITY"
        ]
    # prompt = prompt.encode('utf-8').decode('unicode_escape')
    input_data= [
                {
                    "prompt": "string",
                    "context": "string",
                    "response":response
                }
                ]

    inspeq_eval = InspeqEval(inspeq_api_key=os.environ["INSPEQ_API_KEY"], inspeq_project_id= os.environ["INSPEQ_PROJECT_ID"])
    results = inspeq_eval.evaluate_llm_task(
            metrics_list=metrics_list,
            input_data=input_data,
            task_name="nemo"
        )
    final_result = float(results["results"][0]["evaluation_details"]["actual_value"])
    return final_result
from typing import Optional
import os
from dotenv import load_dotenv
from nemoguardrails.actions import action
from inspeq.client import InspeqEval
load_dotenv()

# mesures toxicity based on inspeq metrics
@action(is_system_action=True)
async def toxicity_inspeq(context: Optional[dict] = None):
    bot_response = context.get("bot_message")
    bot_context = context.get("relevant_chunks")
    eval_result= inspeq_result(bot_context, bot_response)
    verdict = False
    for i in range(len(eval_result["results"])):
        final_result = eval_result["results"][i]["metric_evaluation_status"]
        name = eval_result["results"][i]["evaluation_details"]["metric_name"]
        new_name = name.replace("_EVALUATION", "")
        if final_result == 'FAILED' and final_result != 'EVAL_FAIL':
            if new_name == "TOXICITY":
                verdict = True
                break
            elif new_name == "RESPONSE_TONE":
                verdict = True
                break
            elif new_name == "PROMPT_INJECTION":
                verdict = True
                break
            elif new_name == "INSECURE_OUTPUT":
                verdict = True
                break
            elif new_name == "INVISIBLE_TEXT":
                verdict = True
                break
        else:
            continue
    return verdict
# Define toxicity using inspeq metric
def inspeq_result(context, response):
    metrics_list = [
        "TOXICITY",
        "PROMPT_INJECTION",
        "INVISIBLE_TEXT",
        "INSECURE_OUTPUT"
        ]
    prompt = os.environ["prompt"]
    prompt = prompt.encode('utf-8').decode('unicode_escape')
    input_data= [
                {
                    "prompt": prompt,
                    "context": context,
                    "response":response
                }
                ]

    inspeq_eval = InspeqEval(inspeq_api_key=os.environ["INSPEQ_API_KEY"], inspeq_project_id= os.environ["INSPEQ_PROJECT_ID"])
    results = inspeq_eval.evaluate_llm_task(
            metrics_list=metrics_list,
            input_data=input_data,
            task_name="nemo"
        )
    return results
from typing import Optional
import os
from dotenv import load_dotenv
from nemoguardrails.actions import action
from inspeq.client import InspeqEval
load_dotenv()

# @action(is_system_action=True)
# async def check_blocked_terms(context: Optional[dict] = None):
#     bot_response = context.get("bot_message")

#     # A quick hard-coded list of proprietary terms. You can also read this from a file.
#     proprietary_terms = ["proprietary", "proprietary1", "proprietary2"]

#     for term in proprietary_terms:
#         if term in bot_response.lower():
#             return True

#     return False
# mesures toxicity based on inspeq metrics
@action(is_system_action=True)
async def toxicity_inspeq(context: Optional[dict] = None):
    bot_response = context.get("bot_message")
    bot_context = context.get("relevant_chunks")
    results = inspeq_result(bot_context ,bot_response)
    verdict = False
    for i in range(len(results["results"])):
      name = results["results"][i]["evaluation_details"]["metric_name"]
      new_name = name.replace("_EVALUATION", "")
      final_result = results["results"][i]["metric_evaluation_status"]
      if final_result == 'FAILED' and final_result != "EVAL_FAIL":
        if new_name == "TOXICITY":
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
    print(f"the final verdict is {verdict}")
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
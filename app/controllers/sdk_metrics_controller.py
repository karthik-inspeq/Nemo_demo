from dotenv import load_dotenv
from fastapi import HTTPException, status
from app.services import similarity_score
from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
# import redis
from app.services.schemas import ActualValueDtype, MetricReturnModel, EvaluationType
from app.services.utils import return_labels_summarization, return_labels
from ..services.metric_names import METRICNAMES
load_dotenv()

# REDIS_HOST = os.getenv("REDIS_HOST")
# REDIS_PORT = int(os.getenv("REDIS_PORT"))

# redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def create_success_response(data, custom_action=""):
    return {
        "data": data,
        "status": {
            "code": "200",
            "message": "Success",
            "custom_code": "",
            "custom_action": custom_action
        }
    }

class SdkEvaluationInput(BaseModel):
    llm_input_query: str
    llm_input_context: str
    llm_output: str
          
class MetricConfigInput(BaseModel):
    threshold: Optional[float] = 0.5
    custom_labels: List[str] = None
    label_thresholds: Optional[List[float]] = None     

    class Config:
        extra = "forbid"


def process_compression_score(
    input_data: SdkEvaluationInput,config_input: MetricConfigInput
):
    try:
       
        if config_input is None:
            config_input = MetricConfigInput()  
        
        calculated = similarity_score.SimilarityScore() \
            .compression_score(ground_truths=[input_data.llm_input_context], predictions=[input_data.llm_output])
        calculated = calculated["avg"]
        verdict = ""
        if calculated < config_input.threshold:
            verdict = "Pass"
        else:
            verdict = "Fail"
        
        result = MetricReturnModel(
            metric_name=EvaluationType.COMPRESSION_SCORE_EVALUATION,
            actual_value=calculated, ## TODO: the confidence score needed here
            actual_value_type=ActualValueDtype.FLOAT,
            metric_labels=return_labels(METRICNAMES.COMPRESSION_SCORE, calculated, config_input.threshold, config_input.custom_labels),
            threshold=[verdict], # input threshold
            threshold_score=None,
            personal_attributes=fairness_input.personal_attributes,
            attribute_labels=fairness_input.attribute_labels,
            metric_label=fairness_input.metric_label,
            
            others={"explanation": f'Compression score is {calculated}'}
        )

        return create_success_response(result, custom_action="")

    except HTTPException as http_exception:
        raise http_exception
    
    except Exception as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error_message
        )

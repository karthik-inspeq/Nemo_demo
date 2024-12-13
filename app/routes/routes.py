from fastapi import APIRouter, HTTPException
from app.controllers.sdk_metrics_controller import process_compression_score

from typing import Optional, List
import traceback
from fastapi import FastAPI, HTTPException, Depends, status
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.openapi.docs import get_swagger_ui_html


router = APIRouter()


class SdkEvaluationInput(BaseModel):
    llm_input_query: str
    llm_input_context: str
    llm_output: str
          
class MetricConfigInput(BaseModel):
    threshold: Optional[float]=0.5
    custom_labels: List[str]=["PASS", "FAIL"]
    label_thresholds: Optional[List[float]]=[0,0.5, 1]     

    class Config:
        extra = "forbid"
class FairnessConfigInput(BaseModel):
    personal_attributes: Optional[List[str]]=["Gender", "Race"] 
    attribute_labels: Optional[List[str]]=["Male", "White"]
    metric_label: Optional[float]=0.7


@router.get("/compression_score/health")
def root():
    return {"message": "I am Healthy!"}


@router.post("/compression_score")
# @reduce_credits_on_success_decorator
def compression_score(
    input_data: SdkEvaluationInput,
    config_input: Optional[MetricConfigInput]=None,
    fairness_input: Optional[FairnessConfigInput]=None
    
):
    return process_compression_score(input_data, config_input, fairness_input)

@router.get("/compression_score/docs", include_in_schema=False)
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

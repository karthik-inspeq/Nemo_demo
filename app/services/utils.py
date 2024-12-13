from .metric_names import METRICNAMES
# from evaluate import load
import numpy as np
from enum import Enum
from typing import Any, Union

def return_labels_binary(score):
    labels = []
    if score > 0.5:
        labels.append("Detected")
        return labels
    else:
        labels.append("Not Detected")
        return labels

def return_labels_summarization(score):
    labels = []
    if score == 0:
        labels.append("Fail")
        return labels
    else:
        labels.append("Pass")
        return labels


def return_labels(metric_name, score, threshold, label):
    labels = []
    if metric_name == METRICNAMES.TONALITY:
        if score > 0.5:
            labels.append("Positive")
            return labels
        elif score < 0.5:
            labels.append("Negative")
            return labels
        else:
            labels.append("Neutral")
            return labels
    elif metric_name == METRICNAMES.GRAMMATICAL_CORRECTNESS:
        if score > 0.5 and score < 0.71:
            labels.append("Partially Correct")
            return labels
        elif score < 0.5:
            labels.append("Incorrect")
            return labels
        else:
            labels.append("Correct")
            return labels
    elif metric_name == METRICNAMES.FLUENCY:
        if score > 0.5 and score < 0.71:
            labels.append("Moderately Fluent")
            return labels
        elif score <= 0.5:
            labels.append("Not Fluent")
            return labels
        else:
            labels.append("Fluent")
            return labels
    elif metric_name == METRICNAMES.FACTUAL_CONSISTENCY:
        if score > 0.5 and score < 0.71:
            labels.append("Inconsistent")
            return labels
        elif score <= 0.5:
            labels.append("Hallucinated")
            return labels
        else:
            labels.append("Consistent")
            return labels
    elif metric_name == METRICNAMES.CONCEPTUAL_SIMILARITY:
        if score > 0.5 and score < 0.71:
            labels.append("Somewhat similar")
            return labels
        elif score <= 0.5:
            labels.append("Dissimilar")
            return labels
        else:
            labels.append("Similar")
            return labels
    elif metric_name == METRICNAMES.COHERENCE:
        if score > 0.5 and score < 0.71:
            labels.append("Slightly Coherent")
            return labels
        elif score <= 0.5:
            labels.append("Incoherent")
            return labels
        else:
            labels.append("Coherent")
            return labels
    elif metric_name == METRICNAMES.READABILITY:
        if score > 0.3 and score < 0.6:
            labels.append("Moderate")
            return labels
        elif score <= 0.3:
            labels.append("Sophisticated")
            return labels
        else:
            labels.append("Easy")
            return labels
    elif metric_name == METRICNAMES.CLARITY:
        if score > 0.5 and score < 0.75:
            labels.append("Partially Clear")
            return labels
        elif score <= 0.5:
            labels.append("Not Clear")
            return labels
        else:
            labels.append("Clear")
            return labels
    elif metric_name == METRICNAMES.DIVERSITY:    
        if score <= 0.41:
            labels.append("Redundant")
            return labels
        else:
            labels.append("Not Redundant")  
            return labels 
    elif metric_name == METRICNAMES.CREATIVITY:    
        if score <= 0.5:
            labels.append("Not Creative")
            return labels
        else:
            labels.append("Creative")  
            return labels 
    elif metric_name == METRICNAMES.PROMPT_INJECTION:    
        if score > 0.5 and score < 0.7:
            labels.append("Medium_Confidence")
            return labels
        elif score <= 0.5:
            labels.append("Low_Confidence")
            return labels
        else:
            labels.append("High_Confidence")
            return labels      
    elif metric_name == METRICNAMES.TOXICITY:    
        if score > 0.4 and score < 0.6:
            labels.append("Toxic")
            return labels
        elif score <= 0.4:
            labels.append("Not Toxic")
            return labels
        else:
            labels.append("Severely Toxic")
            return labels      
    elif metric_name == METRICNAMES.BIAS:    
        if score > 0.4 and score < 0.6:
            labels.append("Slightly Bias")
            return labels
        elif score <= 0.4:
            labels.append("Unbias")
            return labels
        else:
            labels.append("Extreme Bias")
            return labels
    elif metric_name == METRICNAMES.COMPRESSION_SCORE:    
        if score < threshold:
            labels.append(label[0])
            return labels
        else:
            labels.append(label[1])
            return labels

def return_labels_binary(score):
    labels = []
    if score > 0.5:
        labels.append("Detected")
        return labels
    else:
        labels.append("Not Detected")
        return labels

def pass_labels():
    return ['Positive', 'Neutral', 'Marginally Relevant Answer', 'Relevant Answer', 'Partially Correct', 'Correct', 'Moderately Fluent', 'Fluent', 'Inconsistent', 'Consistent', 'Somewhat similar', 'Similar', 'Slightly Coherent', 'Coherent', 'Moderate', 'Easy', 'clear','NA-Not evaluated','Passed', 'Creative', 'Not Redundant', 'Detected']


def custom_labels(score, labels, label_thresholds):
    if label_thresholds[0] != 0 or label_thresholds[-1] != 1:
        raise ValueError("The first value of label_thresholds should be 0 and the last value should be 1")

    if len(labels) != len(label_thresholds) - 1:
        raise ValueError("The length of label_thresholds should be one greater than the length of labels")
    for i in range(0, len(label_thresholds)):
        if i == len(label_thresholds)-1:
            return labels[-1]
        if score >= label_thresholds[i] and score < label_thresholds[i+1]:
            return labels[i]

    raise ValueError("Invalid score or label_thresholds")
    

def binary_custom_labels(score, labels, label_thresholds):
    if len(labels) != len(label_thresholds):
        raise ValueError("label_thresholds should have the same length as labels")
    
    if label_thresholds[0] != 0 or label_thresholds[-1] != 1:
        raise ValueError("The first value of label_thresholds should be 0 and the last value should be 1")
    
    for threshold in label_thresholds:
        if threshold not in [0, 1]:
            raise ValueError("Invalid label_thresholds: The thresholds should be limited to the values 0 and 1.")
    
    for i in range(len(label_thresholds)):
        if score == label_thresholds[i]:
            return labels[i]
    
    raise ValueError("Invalid score or label_thresholds")

# def evaluate_bertscore(predictions, references):
#         bertscore = load("bertscore")
#         results= bertscore.compute(predictions=predictions, references=references, model_type="distilbert-base-uncased")
#         return results

def normalize_values(input, minVal, maxVal):
    normalized = (input - minVal) / (maxVal - minVal)
    return normalized        
          

def jsonable_encoder(obj: Any) -> Any:
    if isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, list):
        return [jsonable_encoder(item) for item in obj]
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.float32):
        return float(obj)
    # ... (other cases)
    else:
        return obj

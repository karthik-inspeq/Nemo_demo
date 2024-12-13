from openai import OpenAI, OpenAIError
from fastapi import HTTPException
import openai

class BaseMetric():
    def __init__(self, api_key):
        self.api_key = api_key
        
    def chat_run(self, prompt_template, user_txt):
        client = OpenAI(api_key=self.api_key)
        try:
            chat_completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt_template},
                    {"role": "user", "content": user_txt},
                ],
            )
            return chat_completion.choices[0].message.content
        
# https://platform.openai.com/docs/guides/error-codes/python-library-error-types
        except openai.AuthenticationError as e:
            raise HTTPException(
                status_code=401, 
                detail=f"Authentication credentials of openai key are invalid",
            ) from None
            pass
        except openai.NotFoundError as e:
            raise HTTPException(
                status_code=404, 
                detail=f"Not Found error, regarding your open_api key",
            ) from None
            pass
        
        except openai.PermissionDeniedError as e:
            raise HTTPException(
                status_code=403, 
                detail=f"Permission denied, regarding your open_api key",
            ) from None
            pass
        
        except openai.RateLimitError as e:
              #Handle rate limit error (we recommend using exponential backoff)
            raise HTTPException(
                status_code=429, 
                detail=f"OpenAI API rate limit exceeded. Increase your rate limit by adding a payment method to your account",
            ) from None
            pass
        
        except openai.APIError as e:
              #Handle API error here, e.g. retry or log
            raise HTTPException(
                status_code=500, 
                detail=f"{e}",
            ) from None
            pass
        

    def latency(self):
        pass

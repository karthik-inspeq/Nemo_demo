import uuid
import uvicorn

from fastapi import FastAPI, HTTPException
from mangum import Mangum

from app.routes import routes
from app.monitoring import logging_config
from app.middlewares.correlation_id_middleware import CorrelationIdMiddleware
from app.middlewares.logging_middleware import LoggingMiddleware
from app.handlers.exception_handler import exception_handler
from app.handlers.http_exception_handler import http_exception_handler
from fastapi.openapi.utils import get_openapi
###############################################################################
#   Application object                                                        #
###############################################################################

# app = FastAPI()
from fastapi.openapi.models import Contact, Info

app = FastAPI(
    title="Inspeq AI APIS",
    description="Inspeq AI APIS",
    version="0.1",
    contact={"name": "Inspeq AI", "email": "support@inspeq.ai"},
    openapi_url="/openapi.json",
    docs_url=None,
    redoc_url="/redoc",
    info=Info(
        title="Inspeq AI",
        description="Insepeq AI APIS",
        version="1.0.0",
        contact=Contact(
            name="Inspeq AI",
            email="support@inspeq.ai",
        ),
    ),
)

###############################################################################
#   Logging configuration                                                     #
###############################################################################

logging_config.configure_logging(level='DEBUG', service='compression_score', instance=str(uuid.uuid4()))

###############################################################################
#   Error handlers configuration                                              #
###############################################################################

app.add_exception_handler(Exception, exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

###############################################################################
#   Middlewares configuration                                                 #
###############################################################################

# Tip : middleware order : CorrelationIdMiddleware > LoggingMiddleware -> reverse order
app.add_middleware(LoggingMiddleware)
app.add_middleware(CorrelationIdMiddleware)

###############################################################################
#   Routers configuration                                                     #
###############################################################################

app.include_router(routes.router, prefix='/v1/metrics', tags=['compression_score'])

@app.get("/compression_score/openapi.json")
def openapi():
    return get_openapi(title="FastAPI", version="0.1.0", routes=routes)


###############################################################################
#   Handler for AWS Lambda                                                    #
###############################################################################


handler = Mangum(app)

###############################################################################
#   Run the self contained application                                        #
###############################################################################

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

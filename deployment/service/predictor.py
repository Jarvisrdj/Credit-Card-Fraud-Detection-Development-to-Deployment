# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.
import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.logger import logger
from .service import ScoringService



# The flask app for serving predictions
app = FastAPI()


@app.get("/ping")
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    health = ScoringService.get_model() is not None  # You can insert a health check here
    if health:
        return JSONResponse("\n")
    else:
        return JSONResponse("\n", status_code=404)


@app.post("/invocations")
def transformation(request: Request):
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    data = None
    # Convert from CSV to pandas
    try:
        specs = json.loads(request.headers['X-Amzn-SageMaker-Custom-Attributes'])
    except Exception as e:
        return PlainTextResponse(content=e, status_code=415)

    print("="*20)
    print("specs: ", specs)
    print("type :", type(specs))

    try:
        logger.info("Predicting for motor: {motorid} at time: {timeid}".format(**specs))
    except:
        pass

    # Do the prediction
    print("*"*10,"ENTERING fetch class","*"*10)
    data = ScoringService.fetch(**specs)

    if data.empty:
        return PlainTextResponse(
            content="Insuffucient data for this timeid", 
            status_code=400)

    print("*"*10,"ENTERING predict class","*"*10)
    result = ScoringService.predict(data) 

    if not result:
        return PlainTextResponse(
            content="Failed to compute", 
            status_code=500)

    features = {'features': specs}
    return {**features, **result}

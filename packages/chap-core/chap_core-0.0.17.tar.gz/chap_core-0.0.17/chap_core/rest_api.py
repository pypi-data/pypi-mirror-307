import json
import logging
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from chap_core.api_types import PredictionRequest, EvaluationResponse
from chap_core.internal_state import Control, InternalState
from chap_core.model_spec import ModelSpec
from chap_core.predictor.feature_spec import Feature, all_features
from chap_core.rest_api_src.data_models import FullPredictionResponse
import chap_core.rest_api_src.worker_functions as wf
from chap_core.predictor.model_registry import registry
from chap_core.worker.interface import SeededJob
from chap_core.worker.rq_worker import RedisQueue

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_app():
    app = FastAPI(root_path="/v1")
    origins = [
        "*",  # Allow all origins
        "http://localhost:3000",
        "localhost:3000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = get_app()


class State(BaseModel):
    ready: bool
    status: str
    progress: float = 0


internal_state = InternalState(Control({}), {})

state = State(ready=True, status="idle")


class NaiveWorker:
    def queue(self, func, *args, **kwargs):
        return NaiveJob(func(*args, **kwargs))


class NaiveJob:
    def __init__(self, result):
        self._result = result

    @property
    def status(self):
        return "finished"

    @property
    def exception_info(self):
        return ""

    @property
    def progress(self):
        return 1

    @property
    def result(self):
        return self._result

    def cancel(self):
        pass

    @property
    def is_finished(self):
        return True


# worker = NaiveWorker()
# worker = BGTaskWorker(BackgroundTasks(), internal_state, state)
worker = RedisQueue()


def set_cur_response(response):
    state["response"] = response


@app.get("favicon.ico")
async def favicon() -> FileResponse:
    return FileResponse("chap_icon.jpeg")


@app.post("/predict")
async def predict(data: PredictionRequest) -> dict:
    """
    Start a prediction task using the given data as training data.
    Results can be retrieved using the get-results endpoint.
    """
    json_data = data.model_dump()
    str_data = json.dumps(json_data)
    job = worker.queue(wf.predict, str_data)
    internal_state.current_job = job
    return {"status": "success"}


@app.post("/evaluate")
async def evaluate(data: PredictionRequest, n_splits: Optional[int]=2, stride: int = 1) -> dict:
    """
    Start a prediction task using the given data as training data.
    Results can be retrieved using the get-results endpoint.
    """
    json_data = data.model_dump()
    str_data = json.dumps(json_data)
    job = worker.queue(wf.evaluate, str_data, n_splits, stride)
    internal_state.current_job = job
    return {"status": "success"}


@app.get("/list-models")
async def list_models() -> list[ModelSpec]:
    """
    List all available models. These are not validated. Should set up test suite to validate them
    """
    return registry.list_specifications()


@app.get("/list-features")
async def list_features() -> list[Feature]:
    """
    List all available features
    """
    return all_features


@app.get("/get-results")
async def get_results() -> FullPredictionResponse:
    """
    Retrieve results made by the model
    """
    cur_job = internal_state.current_job
    if not (cur_job and cur_job.is_finished):
        raise HTTPException(status_code=400, detail="No response available")
    result = cur_job.result
    return result


@app.get("/get-evaluation-results")
async def get_evaluation_results() -> EvaluationResponse:
    """
    Retrieve evaluation results made by the model
    """
    cur_job = internal_state.current_job
    if not (cur_job and cur_job.is_finished):
        raise HTTPException(status_code=400, detail="No response available")
    return cur_job.result

@app.get("/get-exception")
async def get_exception() -> str:
    """
    Retrieve exception information if the job failed
    """
    cur_job = internal_state.current_job
    return cur_job.exception_info or ''

@app.post("/cancel")
async def cancel() -> dict:
    """
    Cancel the current training
    """
    if internal_state.control is not None:
        internal_state.control.cancel()
    return {"status": "success"}


@app.get("/status")
async def get_status() -> State:
    """
    Retrieve the current status of the model
    """
    if internal_state.is_ready():
        return State(ready=True, status="idle")

    return State(
        ready=False,
        status=internal_state.current_job.status,
        progress=internal_state.current_job.progress,
    )


def seed(data):
    internal_state.current_job = SeededJob(result=data)

def get_openapi_schema():
    return app.openapi()

def main_backend(seed_data=None):
    import uvicorn
    if seed_data is not None:
        seed(seed_data)
    uvicorn.run(app, host="0.0.0.0", port=8000)

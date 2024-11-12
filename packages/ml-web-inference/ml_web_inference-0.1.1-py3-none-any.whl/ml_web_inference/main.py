import asyncio
from typing import Callable, Awaitable
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import Response
import uvicorn
from datetime import datetime


def expose(
    api_name: str,
    inference_function: Callable[[Request], Awaitable[Response]],
    port: int = 10000,
    init_function: Callable[[], None] = None,
    hangup_function: Callable[[], None] = None,
    hangup_timeout_sec: int = 1800,
    hangup_interval_sec: int = 60,
):
    host = "localhost"
    app = FastAPI()
    initialized = False
    last_inference_time = datetime.now()

    async def check_hangup():
        nonlocal initialized
        while True:
            await asyncio.sleep(hangup_interval_sec)
            if initialized:
                time_since_last_call = datetime.now() - last_inference_time
                if time_since_last_call.total_seconds() > hangup_timeout_sec:
                    if hangup_function is not None:
                        hangup_function()
                    initialized = False

    @app.post(f"/{api_name}")
    async def inference(request: Request, background_tasks: BackgroundTasks):
        nonlocal initialized, last_inference_time
        if not initialized:
            if init_function is not None:
                init_function()
            initialized = True
        last_inference_time = datetime.now()
        background_tasks.add_task(check_hangup)

        return await inference_function(request)

    uvicorn.run(app, host=host, port=port, log_level="info")

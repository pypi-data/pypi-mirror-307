# ml-web-inference

Template for exposing a machine learning model as a web service.

## Example Usage

```python
from ml_web_inference import expose, Request, Response, JSONResponse


async def test_inference(request: Request) -> Response:
    data = await request.json()
    return JSONResponse(content={"data": data})


def test_init():
    print("Initializing model...")


def test_hangup():
    # After the hangup timeout, the server will call this function to hang up the model
    print("Hanging up model...")


expose(
    "test",
    test_inference,
    port=9234,
    hangup_timeout_sec=10,
    hangup_interval_sec=5,
    init_function=test_init,
    hangup_function=test_hangup,
)

# test with
# $response = Invoke-RestMethod -Uri "http://localhost:9234/test" -Method Post -Body (@{"key1"="value1";"key2"="value2"} | ConvertTo-Json) -ContentType "application/json"
# in PowerShell
```
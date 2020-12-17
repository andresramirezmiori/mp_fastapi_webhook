import os
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from constants import EXAMPLE_BODY, VERIFICATION_TOKEN


app = FastAPI()
DEBUG = os.getenv('DEBUG', False)


def process_message(message: dict):
    # expense logic
    return True


@app.get("/")
async def root():    
    return "Hello World!"


@app.post("/webhook/")
async def webhook_handler(req: Request):
    # verify signature if needed
    # add logic to handle the request
    # headers = req.headers
    # password = headers['Authorization']
    if DEBUG:
        body = EXAMPLE_BODY
    else:
        body = await req.json()
    
    # body = example_body
    response = {}
    if 'challenge' in body and 'verification_token' in body:
        if (body['verification_token'] != VERIFICATION_TOKEN):
            raise HTTPException(status_code=403, detail='bad verification code')
        response = {"challenge": body['challenge']}
    else:
        process_message(body)
        response = {
            'received': 'OK'
        }
    return response

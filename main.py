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
async def webhook_handler(background_tasks: BackgroundTasks, req: Request):
    # add logic to handle the request
    # headers = req.headers
    # password = headers['Authorization']
    if DEBUG:
        body = EXAMPLE_BODY
    else:
        body = await req.json()
    response = {}
    # Check if MessengerPeople sent you a challenge, check the verification code.
    # If both is correct, fine - if not - send a 403.
    if 'challenge' in body and 'verification_token' in body:
        if (body['verification_token'] != VERIFICATION_TOKEN):
            raise HTTPException(status_code=403, detail='bad verification code')
        response = {"challenge": body['challenge']}
    else:
        # keep webhook simple and fast, 
        # make task on backgroung to upload in a queue or something like.
        background_tasks.add_task(
            process_message,
            body
        )
        response = {
            'received': 'OK'
        }
    return response

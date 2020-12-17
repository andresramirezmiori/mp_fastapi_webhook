# mp_fastapi_webhook
Simple FastApi webhook based on the [official php version](https://github.com/messengerpeople/simple-php-webhook) of MessengerPeople.

MessengerPeople recomendation:
> We strongly suggest to keep webhooks simple and fast and handle processing logic async. This webhook contains an example message for testing. You can navigate to https://app.messengerpeople.dev/monitoring/ to see all your incoming and outgoing messages. The field "webhook_request" contains the payload that would be sent to your webhook."

## Code
In the [main.py](/main.py) you can find the complete code that implements the webhook.To calm the anxiety, below is the portion corresponding to the webhook endpoint.

```python
@app.post("/webhook/")
async def webhook_handler(background_tasks: BackgroundTasks, req: Request):
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
        # Add challenge to the response
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
```

## Serve on Deta
It's very simple serve the webhook with a [Deta](https://web.deta.sh/) account(check the offical [deta FastApi guide](https://docs.deta.sh/docs/tutorials/fast-api-guide)).

On the base repo folder:

* Install deta CLI, then restart console
```bash
$ curl -fsSL https://get.deta.dev/cli.sh | sh
```
* Login into deta, and deploy your application with deta new
```bash
$ deta login
$ deta new
Successfully created a new micro
{
	"name": "mp_fastapi_webhook",
	"runtime": "python3.7",
	"endpoint": "https://yourendpoint.deta.dev",
	"visor": "enabled",
	"http_auth": "enabled"
}
```
visit https://<your_deta_endpoint>/docs to see the FastApi auto documentation
* Disable deta auth: In these case of use we don`t want **http_auth** enabled
```bash
$ deta auth disable
```
* Open Deta visor: If you want to see the request maked to your Deta server
```bash
$ deta visor open
```

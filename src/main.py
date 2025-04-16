from fastapi import FastAPI, Request
import httpx
import json
import os

app = FastAPI()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    if "pusher" in payload and "repository" in payload:
        repo = payload["repository"]["full_name"]
        pusher = payload["pusher"]["name"]
        url = payload["repository"]["html_url"]

        message = f"*{repo}* に *{pusher}* が push しました！\n<{url}|リポジトリを開く>"

        async with httpx.AsyncClient() as client:
            res = await client.post(SLACK_WEBHOOK_URL, json={"text": message})
            print("Slack response:", res.status_code, res.text)

    return {"status": "ok"}


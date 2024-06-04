import logging
from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
import os
import uvicorn
import telebot
import requests

# Set up logging 
logging.basicConfig(level=logging.INFO)

# Initialize logger
logger = logging.getLogger(__name__)

app = FastAPI(session_timeout=60*60) # 1 hour timeout

# server_api_uri = 'http://localhost:8081/bot{0}/{1}'
# # if server_api_uri != '':
# telebot.apihelper.API_URL = server_api_uri
# logger.info(f'Setting API_URL: {server_api_uri}')

# # server_file_url = 'http://localhost:8081'
# server_file_url = 'http://0.0.0.0:8081'
# # if server_file_url != '':
# telebot.apihelper.FILE_URL = server_file_url
# logger.info(f'Setting FILE_URL: {server_file_url}')

# token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
# # Initialize the bot
# bot = telebot.TeleBot(token)

@app.post("/message")
async def call_message(request: Request, authorization: str = Header(None)):
    # This function only retirns the chat id
    logger.info('post: message')    
    message = await request.json()
    # logger.info(f'message: {message}')

    # If message starts from "/chat"
    if message['text'].startswith('/group'):
        message_text = message['chat']['id']
        logger.info(f'Starts with /group: {message_text}')
        
    elif message['text'].startswith('/user'):        
        message_text = message['from']['id']
        logger.info(f'Starts with /user: {message_text}')
    else:
        # Return ok, 200
        return JSONResponse(content={"status": "ok"}, status_code=200)    

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    # Send reply to sender ablut the chat_id
    update_message = send_reply(token, message['chat']['id'], message['message_id'], message_text)

    # Return ok, 200
    return JSONResponse(content={"status": "ok"}, status_code=200)


def send_reply(bot_token, chat_id, message_id, text):
    url = f"http://localhost:8081/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'reply_to_message_id': message_id
    }
    response = requests.post(url, data=payload)
    return response.json()


def main():
    uvicorn.run(app, host="0.0.0.0", port=8706)


if __name__ == "__main__":
    main()

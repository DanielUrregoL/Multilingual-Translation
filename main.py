from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from functions import response_ai, response_my_memory
from dotenv import load_dotenv
import os

app = FastAPI()

# static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# environment variables
load_dotenv("/home/don_putas/Documents/nao_medical/api/.env")

api_key_ds = os.getenv("API_KEY_DS")
api_key_gpt = os.getenv("API_KEY_GPT")
url = os.getenv("BASE_URL")
my_memory_url = os.getenv("MYMEMORY_URL")


# Keep track of active connections
active_connections = set()

@app.websocket("/ws/gpt/")
async def websocket_endpoint(websocket: WebSocket):
    """
    Websocket endpoint for the GPT model
        Args:
            websocket: WebSocket: websocket connection
        Returns:
            The translated text from the GPT model to the client or the error message
    """
    await websocket.accept()
    active_connections.add(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            input_lang = data["input_lang"]
            output_lang = data["output_lang"]
            text = data["text"].strip()

            if not text:
                continue  

            response = response_ai(url, api_key_gpt, input_lang, output_lang, text, "openai/o3-mini")
            await websocket.send_json({"translated_text": response})

    except WebSocketDisconnect:
        active_connections.remove(websocket)

@app.websocket("/ws/my_memory/")
async def websocket_endpoint(websocket: WebSocket):
    """
    Websocket endpoint for the my_memory translation service
        Args:
            websocket: WebSocket: websocket connection
        Returns:
            The translated text from the my_memory service to the client or the error message
    """
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            data = await websocket.receive_json() 
            input_lang = data["input_lang"]
            output_lang = data["output_lang"]
            text = data["text"].strip()

            if not text:
                continue  

            response = response_my_memory(my_memory_url, input_lang, output_lang, text)
            await websocket.send_json({"translated_text": response})

    except WebSocketDisconnect:
        active_connections.remove(websocket)

@app.websocket("/ws/ds/")
async def websocket_endpoint(websocket: WebSocket):
    """
    Websocket endpoint for the deepseek model
        Args:
            websocket: WebSocket: websocket connection
        Returns:
            The translated text from the deepseek model to the client or the error message  
    """
    await websocket.accept()
    active_connections.add(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            input_lang = data["input_lang"]
            output_lang = data["output_lang"]
            text = data["text"].strip()

            if not text:
                continue 

            response = response_ai(url, api_key_ds, input_lang, output_lang, text, "deepseek/deepseek-chat:free")
            await websocket.send_json({"translated_text": response})

    except WebSocketDisconnect:
        active_connections.remove(websocket)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Function to read the root endpoint
        Returns:
            The index.html file
    """
    with open("static/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

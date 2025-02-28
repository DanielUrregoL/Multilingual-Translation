from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from functions import response_ai, response_my_memory
from dotenv import load_dotenv
import os

app = FastAPI()

# Serve static files (Frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load environment variables
load_dotenv()

api_key_ds = os.getenv("API_KEY_DS")
api_key_gpt = os.getenv("API_KEY_GPT")
url = os.getenv("BASE_URL")
my_memory_url = os.getenv("MYMEMORY_URL")

@app.post("/translate/gpt/")
async def translate_gpt(data: dict):
    """
    REST API endpoint for GPT model translation.
    """
    input_lang = data.get("input_lang")
    output_lang = data.get("output_lang")
    text = data.get("text", "").strip()

    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    response = response_ai(url, api_key_gpt, input_lang, output_lang, text, "openai/o3-mini")

    return JSONResponse(content={"translated_text": response})

@app.post("/translate/my_memory/")
async def translate_my_memory(data: dict):
    """
    REST API endpoint for MyMemory translation service.
    """
    input_lang = data.get("input_lang")
    output_lang = data.get("output_lang")
    text = data.get("text", "").strip()

    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    response = response_my_memory(my_memory_url, input_lang, output_lang, text)

    return JSONResponse(content={"translated_text": response})

@app.post("/translate/ds/")
async def translate_ds(data: dict):
    """
    REST API endpoint for DeepSeek model translation.
    """
    input_lang = data.get("input_lang")
    output_lang = data.get("output_lang")
    text = data.get("text", "").strip()

    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    response = response_ai(url, api_key_ds, input_lang, output_lang, text, "deepseek/deepseek-chat:free")

    return JSONResponse(content={"translated_text": response})

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Serves the index.html file.
    """
    return open("static/index.html").read()

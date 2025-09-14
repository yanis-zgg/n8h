from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
import uuid
import os

# Import Kokoro
try:
    from kokoro import Kokoro
except ImportError:
    raise ImportError("Kokoro package not found. Make sure it's in requirements.txt or installed manually.")

app = FastAPI()
model = Kokoro()

@app.post("/tts")
async def tts(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "")
        if not text:
            return JSONResponse({"error": "No text provided"}, status_code=400)

        # Generate a unique file name
        file_id = str(uuid.uuid4())
        output_file = f"/tmp/{file_id}.wav"

        # Run Kokoro TTS
        model.tts_to_file(text, output_file)

        return FileResponse(output_file, media_type="audio/wav")
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

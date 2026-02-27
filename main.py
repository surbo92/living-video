from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os, uuid, shutil, subprocess
from weather import get_weather
from scheduler import start_scheduler

app = FastAPI()
UPLOAD_DIR = "videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def run(cmd):
    subprocess.run(cmd, shell=True)

def process_video(video_id):
    weather = get_weather()
    input_path = f"{UPLOAD_DIR}/{video_id}.mp4"
    output_path = f"{UPLOAD_DIR}/{video_id}_processed.mp4"

    vf = ""

    if weather["is_day"] == 0:
        vf += "eq=brightness=-0.3:contrast=1.2:saturation=0.7"

    if weather["rain"] > 0:
        if vf:
            vf += ","
        vf += "drawbox=color=white@0.2:t=fill"

    if not vf:
        vf = "null"

    cmd = f'ffmpeg -y -i {input_path} -vf "{vf}" -c:a copy {output_path}'
    run(cmd)

start_scheduler(process_video)

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    video_id = str(uuid.uuid4())
    path = f"{UPLOAD_DIR}/{video_id}.mp4"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    process_video(video_id)

    return {"video_id": video_id}

@app.get("/video/{video_id}")
def get_video(video_id: str):
    return FileResponse(f"{UPLOAD_DIR}/{video_id}_processed.mp4")

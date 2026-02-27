from apscheduler.schedulers.background import BackgroundScheduler
import os

def update_all_videos(process_video):
    for file in os.listdir("videos"):
        if file.endswith(".mp4") and "_processed" not in file:
            video_id = file.replace(".mp4", "")
            process_video(video_id)

def start_scheduler(process_video):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: update_all_videos(process_video),
                      "interval",
                      hours=24)
    scheduler.start()

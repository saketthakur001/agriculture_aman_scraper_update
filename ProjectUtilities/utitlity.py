import requests
from PIL import Image
from io import BytesIO
import re, os, traceback
from pytube import YouTube
from bs4 import BeautifulSoup
from datetime import datetime
from django.conf import settings
from django.core.files import File
from moviepy.editor import clips_array
from moviepy.editor import VideoFileClip 
from django.core.files.base import ContentFile
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def getThumbnail(url, uploaded_file, my_model):
    try:
        if url:
            # Check if the input is a URL
            try:
                video_id = ''
                if "youtube.com" in url:
                    yt = YouTube(url)
                    video_thumbnail_url = yt.thumbnail_url
                    video_id = yt.video_id

                elif "vimeo.com" in url:
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    thumbnail_tag = soup.find('meta', attrs={'property': 'og:image'})
                    video_thumbnail_url = thumbnail_tag['content'] if thumbnail_tag else None

                if video_thumbnail_url:
                    response = requests.get(video_thumbnail_url)
                    if response.status_code == 200:
                        filename = f"thumbnail_{datetime.now().strftime('%d_%m_%y_%H_%M_%S')}.jpg"
                        my_model.thumbnail.save(filename, ContentFile(response.content))
                        my_model.save()

                        return True
            except Exception as e:
                print(f"Error: {str(e)}")

        elif uploaded_file:
            if uploaded_file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image = Image.open(uploaded_file)
                image.thumbnail((500, 500))
                my_model.thumbnail.save('thumbnail_' + uploaded_file.name, File(BytesIO(image.tobytes())))
                my_model.save()
                return True

            elif uploaded_file.name.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.webm')):
                video = VideoFileClip(uploaded_file.temporary_file_path())
                thumbnail = video.get_frame(0)  # Capture the first frame as a thumbnail
                thumbnail_image = Image.fromarray(thumbnail)
                thumbnail_image.thumbnail((500, 500))
                thumbnail_io = BytesIO()
                thumbnail_image.save(thumbnail_io, format='JPEG')
                my_model.thumbnail.save('thumbnail_' + uploaded_file.name + '.jpg', File(thumbnail_io))
                my_model.save()
                return True
    except Exception as e:
        print(f"Error: {str(e)}")
    return False

## convert url
def convert_to_embed_url(url):
    try:
        # Check if the URL is from YouTube
        if re.match(r'^https?://(?:www\.)?(youtube\.com|youtu\.be)', url):
            youtube_regex = r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^&]+)|youtu\.be/([^&]+)'
            match = re.search(youtube_regex, url)
            if match:
                video_id = match.group(1) or match.group(2)
                if video_id:
                    embed_url = f'https://www.youtube.com/embed/{video_id}'
                    return embed_url

        # Check if the URL is from Vimeo
        elif re.match(r'^https?://(www\.)?vimeo\.com', url):
            vimeo_regex = r'^https?://(www\.)?vimeo\.com/(\d+)'
            match = re.search(vimeo_regex, url)
            if match:
                video_id = match.group(2)
                if video_id:
                    embed_url = f'https://player.vimeo.com/video/{video_id}'
                    return embed_url
                
    except Exception as e:
        print(f"Error: {str(e)}")
    
    return None


### genearte preview gif
def generate_video_preview(file, model_object):
    try:
        start_time = 1

        # file_name, file_extension = os.path.splitext(file.name)

        preview_file_name = f"test_preview.gif"

        video = VideoFileClip(file.temporary_file_path())
        video_duration = video.duration

        video = video.resize(newsize=(550, 300))

        end_time = 3 if video_duration > 3 else video_duration
        video_segment = video.subclip(start_time, end_time)
        video_preview_path = os.path.join(settings.MEDIA_ROOT, preview_file_name)  # Replace with your media directory path
        video_segment.write_gif(video_preview_path, program="imageio")
        video_segment.close()
        with open(video_preview_path, 'rb') as preview_file:
            model_object.preview.save(preview_file_name, File(preview_file), save=True)
        os.remove(video_preview_path)

        return True
    except:
        traceback.print_exc()
        return False
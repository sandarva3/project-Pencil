from django.shortcuts import render
import yt_dlp
import os
from django.conf import settings
from django.http import StreamingHttpResponse, HttpResponse

def audio_view(request):
    if request.method == "POST":
        try:
            link = request.POST['link']
            dictionary = {
                'format': 'bestaudio[ext=webm]/bestaudio/best',
                'outtmpl': os.path.join(settings.BASE_DIR, 'downloads', '%(title)s.%(ext)s'),
                'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],

            }
            with yt_dlp.YoutubeDL(dictionary) as ydl:
                info = ydl.extract_info(link, download=True)
                audio_title = info.get('title', 'No title')
                thumbnail = info.get('thumbnail', 'No thumbnail')

            context = {
                'status': 'success',
                'filename': f'{audio_title}.mp3',
                'title': audio_title,
                'thumbnail': thumbnail
            }
            return render(request, 'audio/audio.html', context)

        except Exception as e:
            print(f"The error is: {e}")
            context = {
                'status': 'Failed', 'msg1': 'Audio not downloaded'
            }
            return render(request, 'audio/audio.html', context)

    else:
        return render(request, 'audio/audio.html')

def downloadAudio_view(request):
    if request.method == "GET" and 'filename' in request.GET:
        filename = request.GET['filename']
        
        try:
            file_path = os.path.join(settings.BASE_DIR, 'downloads', filename)
            
            def file_stream():
                file_obj = None  # Initialize the file object
                try:
                    file_obj = open(file_path, 'rb')
                    while True:
                        data = file_obj.read(8192)
                        if not data:
                            break
                        yield data
                finally:
                    if file_obj is not None:
                        file_obj.close()
                    if os.path.exists(file_path):
                        os.remove(file_path)


            response = StreamingHttpResponse(file_stream(), content_type='audio/mp3')
            response['Content-Disposition'] = f'attachment; filename={filename}'
            return response

        except Exception as e:
            print(f"Something went Wrong. Exception: {e}")
            return HttpResponse("Something Went Wrong. EXCEPTION !")

    return HttpResponse('Something went wrong!')

from django.shortcuts import render
import yt_dlp
import os
from django.conf import settings
import json
from django.http import JsonResponse, FileResponse, HttpResponse, StreamingHttpResponse

def home_view(request):
    return render(request, 'home.html')

def youtube_view(request):
    if request.method == "POST":
        try:
            link = request.POST['link']
            dictionary = {}
            with yt_dlp.YoutubeDL(dictionary) as ydl:
                info = ydl.extract_info(link, download=False)
                resolutions = []
                for f in info['formats']:
                    if f.get('height') is not None:
                        resolutions.append(f['height'])

                title = info.get('title', 'No title')
                thumbnail = info.get('thumbnail', 'No thumbnail')

                resolutions = list(set(resolutions))
                resolutions.sort(reverse=True)

            context = {
                'resolutions': resolutions,
                'link': link,
                'title': title,
                'thumbnail': thumbnail,
            }   
            return render(request, 'pencilapp/youtube.html', context)

        except Exception as e:
            print(f"The error is: {e}")
            return render(request, 'pencilapp/youtube.html', {'msg1': 'Error proceeding further! Make sure URL is valid.'})


    elif request.method == "GET" and 'link' in request.GET and 'resolution' in request.GET:
        try:
            print("Yeah")
            link = request.GET['link']
            selected_resolution = request.GET['resolution']
            dictionary = {
                'format': f'bestvideo[height={selected_resolution}]+bestaudio/best',
                'outtmpl': os.path.join(settings.BASE_DIR, 'downloads', '%(title)s.%(ext)s'),
            }   
            with yt_dlp.YoutubeDL(dictionary) as ydl:
                info = ydl.extract_info(link, download=False)
                selected_format = next((f for f in info['formats'] if f.get('height') == int(selected_resolution)), None)
                video_title = info['title']

                if selected_format:
                    filesize = selected_format.get('filesize')
                    if filesize is not None:
                        print(f"FILE SIZE IS: {filesize}")
                        # if (filesize * 1.15) > (400 * 1024 * 1024):  # Greater than 400 MB You can SET LIMIT if you want.
                        #     return JsonResponse({'status': 'Failed', 'msg1': 'File too large'})

                    ydl.download([link]) 

            return JsonResponse({'status': 'success', 'msg2': 'Link generated Successfully', 'filename': f'{video_title}.webm'})


        except Exception as e:
            print(e)
            return JsonResponse({'status': 'Failed', 'msg1': 'Video not downloaded'})

    else:
        return render(request, 'pencilapp/youtube.html')

def download_view(request):
    if request.method == "GET" and 'filename' in request.GET:
        filename = request.GET['filename']
        
        try:
            file_path = os.path.join(settings.BASE_DIR, 'downloads', filename)
            
            print("DOWNLOAD TRIGGERED")
            print(f"FILE PATH after response : {file_path}")
            # Generator function to read the file in chunks
            def file_stream():
                with open(file_path, 'rb') as f:
                    while True:
                        data = f.read(8192)  # 8KB at a time
                        if not data:
                            break
                        yield data
                # Delete the file after streaming it
                os.remove(file_path)

            response = StreamingHttpResponse(file_stream(), content_type='video/webm')
            response['Content-Disposition'] = f'attachment; filename={filename}'
            return response

        except Exception as e:
            print(f"Something went Wrong. Exception: {e}")
            return HttpResponse("Something Went Wrong. EXCEPTION !")

    return HttpResponse('Something went wrong!')
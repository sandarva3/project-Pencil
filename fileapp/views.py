from django.shortcuts import render, HttpResponse
from django.http import FileResponse, StreamingHttpResponse
from .utils import *

def fileapp_view(request):
    if request.method == 'POST':
        from_format = request.POST['from-format']
        to_format = request.POST['to-format']
        uploaded_file = request.FILES['file-input']

        if from_format == 'pdf' and to_format == 'txt':
            file_path = pdf_txt(uploaded_file)
            if file_path is None:
                return render(request, 'fileapp/fileapp.html', {'error': 'An error occurred while converting..'})
            content_type = 'text/plain'
            filename = 'converted.txt'
        
        elif from_format == 'txt' and to_format == 'pdf':
            file_path = txt_pdf(uploaded_file)
            if file_path is None:
                return render(request, 'fileapp/fileapp.html', {'error': 'An error occured while converting..'})
            content_type = 'application/pdf'
            filename = 'converted.pdf'
        
        elif from_format in ['png','jpeg'] and to_format == 'pdf':
            file_path = image_pdf(uploaded_file)
            if file_path is None:
                return render(request, 'ffileapp/fileapp.html', {'error': 'An error occured while converting..'})
            content_type = 'application/pdf'
            filename = 'converted.pdf'

        elif from_format == 'png' and to_format == 'jpeg':
            file_path = png_jpeg(uploaded_file)
            if file_path is None:
                return render(request, 'fileapp/fileapp.html', {'error': 'An error occured while converting..'})
            content_type = "image/jpeg"
            filename = 'converted.jpg'

        elif from_format == 'jpeg' and to_format == 'png':
            file_path = jpeg_png(uploaded_file)
            if file_path is None:
                return render(request, 'fileapp/fileapp.html', {'error': 'An error occured while converting..'})
            content_type = "image/png"
            filename = 'converted.png'

        elif from_format == 'pdf' and to_format == 'epub':
            file_path = pdf_epub(uploaded_file)
            if file_path is None:
                return render(request, 'fileapp/fileapp.html', {'error': 'An error occured while converting..'})
            content_type = 'application/epub+zip'
            filename = 'converted.epub'
        else:
            return render(request, 'fileapp/fileapp.html', {'error': 'Unsupported conversion..please choose a Valid file'})
        
        def file_stream():
                with open(file_path, 'rb') as f:
                    while True:
                        data = f.read(8192)  # 8KB at a time
                        if not data:
                            break
                        yield data
                os.remove(file_path)
                
        response = StreamingHttpResponse(file_stream(), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['Success-Message'] = 'File converted successfully!'
        return response

    return render(request, 'fileapp/fileapp.html')

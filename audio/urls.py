from django.urls import path
from .views import(
    audio_view,
    downloadAudio_view,
)

urlpatterns = [
    path('', audio_view, name='audio'),
    path('audioDownload/', downloadAudio_view, name="audio_download")
]

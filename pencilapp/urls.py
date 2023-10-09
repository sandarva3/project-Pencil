from django.urls import path
from .views import(
    youtube_view,
    download_view
)

urlpatterns = [
    path('', youtube_view, name='ytpage'),
    path('download/', download_view, name="video_download")
]

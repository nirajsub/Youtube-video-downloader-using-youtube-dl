from django.shortcuts import render, redirect
from pytube import YouTube
from pytube import *
from .forms import *
import pytube
import os
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

import requests
from django.http import HttpResponse
import youtube_dl
# import yt_dlp
from .forms import DownloadForm
import re

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def download_video(request):
    global video_url
    # if request.is_ajax():
    #     video_url = request.GET.get('url')
    # form = DownloadForm(request.POST or None)
    if request.method == 'POST':
        video_url = request.POST.get('urls')
    # if form.is_valid():
    #     video_url = form.cleaned_data.get("url")
        regex = r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'

        video_id = video_url.split('=')[-1]
        print(video_url)
        if not re.match(regex,video_url):
            return HttpResponse('Enter correct url.')
        ydl_opts = {
            'format': 'bestvideo'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(
                video_url, download=False)
        video_audio_streams = []
        yt = YouTube(video_url)
        # print(yt.title)
        # pvideo = yt.streams.filter(progressive=True)
        # avideo = yt.streams.filter(adaptive=True)
        # mp4video = yt.streams.filter(file_extension='mp4')
        # audio = yt.streams.filter(only_audio=True)
        for m in meta['formats']:
            file_size = m['filesize']
            if file_size is not None:
                if file_size > 1000000000:
                    file_size = f'{round(int(file_size) / 1000000000,2)} GB'
                else:
                    file_size = f'{round(int(file_size) / 1000000,2)} MB'
            resolution = 'Audio'
            if m['height'] is not None:
                resolution = f"{m['height']}"
                                              
            video_audio_streams.append({
                'resolution': resolution,
                'extension': m['ext'],
                'file_size': file_size,
                'video_url': m['url']
            })
        video_audio_streams = video_audio_streams[::-1]
        context = {
            'video_url':video_url,
            # 'title': meta['title'], 
            'title': meta['title'], 
            'streams': video_audio_streams,
            'thumb': meta['thumbnail'],
            'duration': round(int(meta['duration'])/60, 2),
            'views': f'{int(meta["view_count"]):,}',
            'likes': meta['like_count'],
            'streams': video_audio_streams,
            # 'pvideo':pvideo,
            # 'avideo':avideo,
            # 'audio':audio,
            # 'mp4video':mp4video,
            'video_id':video_id,
        }
        return render(request, 'index.html', context)
    return render(request, 'index.html')

def downloadvideo(request, itag):
    global video_url
    homedir = os.path.expanduser("~")
    dirs = homedir + "/Downloads"
    yt = YouTube(video_url)
    title = yt.title
    stream = yt.streams.get_by_itag(itag=itag)
    down = stream.download(dirs)
    # os.rename(yt.streams.get_by_itag(itag=itag).default_filename, 'shortsdownloader.com.mp4')
    return redirect('home')
    return render(request, 'index.html')



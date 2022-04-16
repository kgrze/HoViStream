#!/usr/bin/env python

import os
import shutil
import subprocess
from generate_web_interface import generate_web_interface
from convert_to_stream import conv_to_stream

path_in_media = '/home/kgrze/HoViStream/media'
path_out_web_interface = '/home/kgrze/HoViStream/www'
path_out_stream = '/home/kgrze/HoViStream/www/stream'

def is_video_file(path):
    """Check file extension to detect valid video file"""
    fileExtension = path.rsplit('.', 1)
    if fileExtension[1] not in ['avi', 'mp4', 'mov', 'mkv', 'webm']:
        return False
    return True

def is_subtitles_file(path):
    """Check file extension to detect valid subtitle file"""
    for root, _, items in os.walk(path):
        for item in items:
            file_path = os.path.join(root, item)
            file_ext = file_path.rsplit('.', 1)
            if file_ext[1] in ['srt', 'vtt']:
                return file_path
    return None

# sudo visudo
# "kgrze ALL=(ALL) NOPASSWD: /bin/systemctl reload nginx.service"
def refresh_nginx():
    cmd = ['sudo']
    cmd.append('systemctl')
    cmd.append('reload')
    cmd.append('nginx.service')
    subprocess.call(cmd)

if os.path.exists(path_out_stream):
    shutil.rmtree(path_out_stream)
os.makedirs(path_out_stream)

list_video = []
for root, _, items in os.walk(path_in_media):
    for item in items:
        video_item = []
        file_path = os.path.join(root, item)
        if is_video_file(file_path):
            vide_title = os.path.basename(file_path).split('.')[0]
            video_item.append(vide_title)
            video_item.append(file_path)
            path_subs = is_subtitles_file(root)
            if path_subs is not None:
                video_item.append(path_subs)
            list_video.append(video_item)
for video in list_video:
    name_stream = video[0]
    path_stream = os.path.join(path_out_stream, name_stream)
    path_video = video[1]
    path_subs = video[2]
    conv_to_stream(path_video, path_stream, True, path_subs)
generate_web_interface(path_out_stream, path_out_web_interface)
refresh_nginx()
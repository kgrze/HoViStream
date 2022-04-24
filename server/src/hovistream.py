#!/usr/bin/env python

import os
import sys
import shutil
import subprocess
from generate_web_interface import generate_web_interface
from convert_to_stream import conv_to_stream
from jinja2 import Environment, FileSystemLoader

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
# put at the end of file: "${USER} ALL=(ALL) NOPASSWD: /bin/systemctl reload nginx.service"
def refresh_nginx(path_out_stream_www):
    j2_env = Environment(loader=FileSystemLoader('./templates'),trim_blocks=True)
    nginx_conf_content = j2_env.get_template('template_nginx.conf').render(path_stream=path_out_stream_www)
    nginx_conf = open('nginx.conf',"w+")
    nginx_conf.write(nginx_conf_content)
    nginx_conf.close()

    cmd = ['sudo']
    cmd.append('mv')
    cmd.append('nginx.conf')
    cmd.append('/etc/nginx/nginx.conf')
    subprocess.call(cmd)

    cmd = ['sudo']
    cmd.append('systemctl')
    cmd.append('reload')
    cmd.append('nginx.service')
    subprocess.call(cmd)

def hovistream(path_in_video, path_out_stream_www, no_encoding=True):
    path_out_stream = os.path.join(path_out_stream_www, 'stream')
    path_db_video = os.path.join(path_out_stream_www,'stream_list.txt')
    list_prev_streams = []
    db_video = None
    if os.path.exists(path_db_video) is True:
        # Video list file exists, read it and delete it
        db_video = open(path_db_video,"r")
        list_prev_streams = db_video.readlines()
        db_video.close()
        os.remove(path_db_video)
    if os.path.exists(path_out_stream_www) is False:
        os.makedirs(path_out_stream_www)
    db_video = open(os.path.join(path_out_stream_www,'stream_list.txt'),"w+")
    list_new_streams = []
    list_streams = []
    for root, _, items in os.walk(path_in_video):
        for item in items:
            video_item = []
            file_path = os.path.join(root, item)
            if is_video_file(file_path):
                vide_title = os.path.basename(file_path)
                list_streams.append(vide_title)
                if vide_title+'\n' in list_prev_streams:
                    # Stream already exists
                    continue
                else:
                    # Stream doesn't exist, need to convert video to stream
                    video_item.append(vide_title)
                    video_item.append(file_path)
                    path_subs = is_subtitles_file(root)
                    if path_subs is not None:
                        video_item.append(path_subs)
                    list_new_streams.append(video_item)
    for video in list_new_streams:
        name_stream = video[0]
        path_stream = os.path.join(path_out_stream, name_stream)
        path_video = video[1]
        if len(video) > 2:
            path_subs = video[2]
        conv_to_stream(path_video, path_stream, no_encoding, path_subs)
    for stream_string in list_prev_streams:
        stream = stream_string.split('\n')[0]
        if stream not in list_streams:
            # stream source has been deleted, delete the stream
            path_stream = os.path.join(path_out_stream, stream)
            shutil.rmtree(path_stream)
    for stream in list_streams:
        db_video.write(stream+'\n')
    db_video.close()
    generate_web_interface(path_out_stream, path_out_stream_www)
    refresh_nginx(path_out_stream_www)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please specify paths to input video and output stream location')
        sys.exit()

    if len(sys.argv) == 4:
        hovistream(os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]), sys.argv[3])
    else:
        hovistream(os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]))

# ./hovistream "/home/$USER/HoViStream/media" "/home/$USER/HoViStream/www"
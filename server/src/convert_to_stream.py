#!/usr/bin/env python

import os
import sys

if len(sys.argv) < 2:
    print('Please specify path to video file')
    sys.exit()

path_video  = sys.argv[1]

if os.path.exists(path_video) is False:
    print('Specified video file path: {} does not exist'.format(path_video))

#python convert_to_stream.py ~/Videos/House.Of.Gucci.2021.1080p.AMZN.WEBRip.DDP5.1.Atmos.x264-TEPES/HOG.mp4

# sudo ffmpeg -y -i batman.mp4 -c:v libx264 \
#  -r 24 -x264opts 'keyint=48:min-keyint=48:no-scenecut' \
#  -vf scale=-2:2160 -b:v 6000k -maxrate 6000k \
#  -movflags faststart -bufsize 8600k \
#  -profile:v main -preset fast -an "batman_2160p.mp4"

# sudo ffmpeg -y -i batman.mp4 -c:v libx264 \
#  -r 24 -x264opts 'keyint=48:min-keyint=48:no-scenecut' \
#  -vf scale=-2:1080 -b:v 4300k -maxrate 4300k \
#  -movflags faststart -bufsize 8600k \
#  -profile:v main -preset fast -an "batman_1080p.mp4"

# sudo ffmpeg -y -i batman.mp4 -c:v libx264 \
#  -r 24 -x264opts 'keyint=48:min-keyint=48:no-scenecut' \
#  -vf scale=-2:720 -b:v 3500k -maxrate 3500k \
#  -movflags faststart -bufsize 8600k \
#  -profile:v main -preset fast -an "batman_720p.mp4"

# sudo ffmpeg -y -i batman.mp4 -map 0:1 -vn -c:a aac -b:a 128k -ar 48000 -ac 2 batman_audio.m4a

# sudo packager \
# 'in=../batman.mp4,stream=audio,init_segment=audio/init.mp4,segment_template=audio/$Number$.m4s' \
# 'in=../batman_subs.vtt,stream=text,init_segment=text/init.mp4,segment_template=text/$Number$.m4s,dash_only=1' \
# 'in=../batman_subs.vtt,stream=text,segment_template=text/$Number$.vtt,hls_only=1' \
# 'in=../batman_720p.mp4,stream=video,init_segment=h264_720p/init.mp4,segment_template=h264_720p/$Number$.m4s' \
# 'in=../batman_1080p.mp4,stream=video,init_segment=h264_1080p/init.mp4,segment_template=h264_1080p/$Number$.m4s' \
# 'in=../batman_2160p.mp4,stream=video,init_segment=h264_2160p/init.mp4,segment_template=h264_2160p/$Number$.m4s' \
# --generate_static_live_mpd --mpd_output batman_dash.mpd \
# --hls_master_playlist_output batman_hls.m3u8
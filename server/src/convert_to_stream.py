#!/usr/bin/env python

import os
import subprocess

def ffmpeg_convert_video(path_input_video, path_output, scale):
    if scale in [1280, 1920, 2360]:
        cmd = ['ffmpeg']
        cmd.append('-y')
        cmd.append('-i')
        cmd.append(path_input_video)
        cmd.append('-c:v')
        cmd.append('libx264')
        cmd.append('-r')
        cmd.append('24')
        cmd.append('-x264opts')
        cmd.append('keyint=48:min-keyint=48:no-scenecut')
        cmd.append('-vf')
        cmd.append('scale='+str(scale)+':-2')
        cmd.append('-maxrate')
        cmd.append('4000K')
        cmd.append('-movflags')
        cmd.append('faststart')
        cmd.append('-bufsize')
        cmd.append('8600K')
        cmd.append('-profile:v')
        cmd.append('main')
        cmd.append('-preset')
        cmd.append('ultrafast')
        cmd.append('-crf')
        cmd.append('22')
        cmd.append('-an')
        # cmd.append('-threads')
        # cmd.append('4')
        out_name = 'video_'+str(scale)+'p'+'.mp4'
        output = os.path.join(path_output, out_name)
        cmd.append(output)
        subprocess.call(cmd)
        subprocess.call(['chmod', '755', output])
        return output

def ffmpeg_extract_audio(path_input_video, path_output):
    cmd = ['ffmpeg']
    cmd.append('-y')
    cmd.append('-i')
    cmd.append(path_input_video)
    cmd.append('-map')
    cmd.append('0:1')
    cmd.append('-vn')
    cmd.append('-c:a')
    cmd.append('aac')
    cmd.append('-b:a')
    cmd.append('128k')
    cmd.append('-ar')
    cmd.append('48000')
    cmd.append('-ac')
    cmd.append('2')
    out_name = 'audio.m4a'
    output = os.path.join(path_output, out_name)
    cmd.append(output)
    subprocess.call(cmd)
    subprocess.call(['chmod', '755', output])
    return output

def ffmpeg_convert_subtitles_to_vtt(path_input_subtitles, path_output):
    cmd = ['ffmpeg']
    cmd.append('-i')
    cmd.append(path_input_subtitles)
    cmd.append('-c:s')
    cmd.append('webvtt')
    out_name = 'subtitles.vtt'
    output = os.path.join(path_output, out_name)
    cmd.append(output)
    subprocess.call(cmd)
    subprocess.call(['chmod', '755', output])
    return output

def ffmpeg_extract_subtitles(path_input_video, path_output):
    cmd = ['ffmpeg']
    cmd.append('-i')
    cmd.append(path_input_video)
    out_name = 'subtitles.vtt'
    output = os.path.join(path_output, out_name)
    cmd.append(output)
    subprocess.call(cmd)
    if os.path.isfile(output):
        return None
    else:
        subprocess.call(['chmod', '755', output])
        return output

def qnapi_download_subtitles(path_input_video, path_output):
    subs_name = os.path.basename(path_input_video).split('.')[0]+'.srt'
    path_input_subs = os.path.join(path_input_video, subs_name)
    cmd = ['qnapi']
    cmd.append('-c')
    cmd.append('-l')
    cmd.append('pl')
    cmd.append('-lb')
    cmd.append('en')
    cmd.append(path_input_video)
    subprocess.call(cmd)
    if os.path.exists(path_input_subs) is False:
        return None
    else:
        subprocess.call(['chmod', '755', subs_name])
        path_output_subs = ffmpeg_convert_subtitles_to_vtt(path_input_subs, path_output)
        return path_output_subs

def shaka_pack_to_dash_hls(path_1280, path_1920, path_2360, path_audio, path_subs=None, path_output='.'):
    cmd = ['packager']
    cmd.append('in='+path_audio+',stream=audio,init_segment=audio/init.mp4,segment_template=audio/$Number$.m4s')
    cmd.append('in='+path_1280+',stream=video,init_segment=h264_1280/init.mp4,segment_template=h264_1280/$Number$.m4s')
    cmd.append('in='+path_1920+',stream=video,init_segment=h264_1920/init.mp4,segment_template=h264_1920/$Number$.m4s')
    cmd.append('in='+path_2360+',stream=video,init_segment=h264_2360/init.mp4,segment_template=h264_2360/$Number$.m4s')
    if path_subs is not None:
        cmd.append('in='+path_subs+',stream=text,init_segment=text/init.mp4,segment_template=text/$Number$.m4s,dash_only=1')
        cmd.append('in='+path_subs+',stream=text,segment_template=text/$Number$.vtt,hls_only=1')
    cmd.append('--generate_static_live_mpd')
    cmd.append('--mpd_output')
    cmd.append(os.path.join(path_output, 'stream_dash.mpd'))
    cmd.append('--hls_master_playlist_output')
    cmd.append(os.path.join(path_output, 'stream_hls.m3u8'))
    subprocess.call(cmd, cwd=path_output)

def conv_to_stream(path_input_video, path_output_stream_location, path_input_subtitles=None):
    if os.path.exists(path_input_video) is False:
        print('Specified video file path: {} does not exist'.format(path_input_video))
        exit(-1)
    if os.path.exists(path_output_stream_location) is False:
        print('Specified output path: {} does not exist. Creating it'.format(path_output_stream_location))
        os.makedirs(path_output_stream_location)

    path_video_1280 = ffmpeg_convert_video(path_input_video, path_output_stream_location, 1280)
    path_video_1920 = ffmpeg_convert_video(path_input_video, path_output_stream_location, 1920)
    path_video_2360 = ffmpeg_convert_video(path_input_video, path_output_stream_location, 2360)
    path_audio = ffmpeg_extract_audio(path_input_video, path_output_stream_location)

    path_subs = None
    if path_input_subtitles is not None:
        path_subs = ffmpeg_convert_subtitles_to_vtt(path_input_subtitles, path_output_stream_location)
    else:
        path_subs = ffmpeg_extract_subtitles(path_input_video, path_output_stream_location)
        if path_subs is None:
            path_subs = qnapi_download_subtitles(path_input_video, path_output_stream_location)

    shaka_pack_to_dash_hls(path_video_1280, path_video_1920, path_video_2360, path_audio, path_subs, path_output_stream_location)

    os.remove(path_video_1280)
    os.remove(path_video_1920)
    os.remove(path_video_2360)
    os.remove(path_audio)
    os.remove(path_subs)

#python convert_to_stream.py ~/Videos/House.Of.Gucci.2021.1080p.AMZN.WEBRip.DDP5.1.Atmos.x264-TEPES/HOG.mp4 .

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
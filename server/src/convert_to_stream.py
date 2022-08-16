#!/usr/bin/env python
# author: kgrze

import os
import sys
import subprocess

def print_cmd(cmd_list):
    CYELLOW = '\033[33m'
    CEND = '\033[0m'
    cmd_str = ''
    for cmd in cmd_list:
        cmd_str += cmd + ' '
    print(CYELLOW + '\n[HOVISTREAM]' + CEND)
    print(CYELLOW + cmd_str + CEND)
    print(CYELLOW + '[HOVISTREAM]\n' + CEND)


def is_subtitles_file(path):
    """Check file extension to detect valid subtitle file"""
    for root, _, items in os.walk(path):
        for item in items:
            file_path = os.path.join(root, item)
            file_ext = file_path.rsplit('.', 1)
            if file_ext[1] in ['srt', 'vtt']:
                return file_path
    return None

def ffmpeg_convert_video(path_input_video, path_output, scale):
    if scale in [1280, 1920, 2048]:
        cmd = ['ffmpeg']
        cmd.append('-y')
        cmd.append('-i')
        cmd.append(path_input_video)
        cmd.append('-c:v')
        cmd.append('libx264')
        cmd.append('-r')
        cmd.append('24')
        cmd.append('-pix_fmt')
        cmd.append('yuv420p')
        cmd.append('-x264opts')
        cmd.append('keyint=48:min-keyint=48:no-scenecut')
        cmd.append('-vf')
        cmd.append('scale='+str(scale)+':-2')
        #cmd.append('-maxrate')
        #cmd.append('4000K')
        cmd.append('-movflags')
        cmd.append('faststart')
        #cmd.append('-bufsize')
        #cmd.append('8600K')
        cmd.append('-profile:v')
        cmd.append('main')
        cmd.append('-preset')
        cmd.append('ultrafast')
        cmd.append('-crf')
        cmd.append('22')
        cmd.append('-an')
        #cmd.append('-threads')
        #cmd.append('8')
        out_name = 'video_'+str(scale)+'p'+'.mp4'
        output = os.path.join(path_output, out_name)
        cmd.append(output)
        print_cmd(cmd)
        subprocess.call(cmd)
        subprocess.call(['chmod', '755', output])
        return output

def ffmpeg_copy_video(path_input_video, path_output):
    cmd = ['ffmpeg']
    cmd.append('-y')
    cmd.append('-i')
    cmd.append(path_input_video)
    cmd.append('-c:v')
    cmd.append('copy')
    cmd.append('-pix_fmt')
    cmd.append('yuv420p')
    cmd.append('-an')
    out_name = 'video_orig.mp4'
    output = os.path.join(path_output, out_name)
    cmd.append(output)
    print_cmd(cmd)
    subprocess.call(cmd)
    subprocess.call(['chmod', '755', output])
    return output

def ffmpeg_is_h264(path_input_video):
    # cmd = ['ffprobe']
    # cmd.append(path_input_video)
    # result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    # ffprobe_out = result.stdout
    if '264' in path_input_video:
        return True
    return False

def ffmpeg_is_h265(path_input_video):
    # cmd = ['ffprobe']
    # cmd.append(path_input_video)
    # result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    # ffprobe_out = result.stdout
    if '265' in path_input_video:
        return True
    return False

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
    print_cmd(cmd)
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
    print_cmd(cmd)
    subprocess.call(cmd)
    if os.path.isfile(output):
        subprocess.call(['chmod', '755', output])
        return output
    else:
        return None

def ffmpeg_extract_subtitles(path_input_video, path_output):
    cmd = ['ffmpeg']
    cmd.append('-i')
    cmd.append(path_input_video)
    out_name = 'subtitles.vtt'
    output = os.path.join(path_output, out_name)
    cmd.append(output)
    print_cmd(cmd)
    subprocess.call(cmd)
    if os.path.isfile(output):
        subprocess.call(['chmod', '755', output])
        return output
    else:
        return None

def qnapi_download_subtitles(path_input_video, path_output):
    cmd = ['qnapi']
    cmd.append('-c')
    cmd.append('-q')
    cmd.append('-d')
    cmd.append('-l')
    cmd.append('pl')
    cmd.append('-lb')
    cmd.append('en')
    cmd.append(path_input_video)
    print_cmd(cmd)
    subprocess.call(cmd)
    path_input_video_no_ext, ext = os.path.splitext(path_input_video)
    path_subs = path_input_video_no_ext + '.srt'
    # path_input_video_parent = os.path.abspath(os.path.dirname(path_input_video))
    # path_qnapi_subs = is_subtitles_file(path_input_video_parent)
    if os.path.isfile(path_subs):
        path_output_subs = ffmpeg_convert_subtitles_to_vtt(path_subs, path_output)
        return path_output_subs
    else:
        return None

def shaka_pack_to_dash_hls(path_1920, path_audio, path_subs=None, path_output='.'):
    cmd = ['packager']
    cmd.append('in='+path_audio+',stream=audio,init_segment=audio/init.mp4,segment_template=audio/$Number$.m4s')
    cmd.append('in='+path_1920+',stream=video,init_segment=h264_1920/init.mp4,segment_template=h264_1920/$Number$.m4s')
    if path_subs is not None:
        cmd.append('in='+path_subs+',stream=text,init_segment=text/init.mp4,segment_template=text/$Number$.m4s,dash_only=1')
        cmd.append('in='+path_subs+',stream=text,segment_template=text/$Number$.vtt,hls_only=1')
    cmd.append('--generate_static_live_mpd')
    cmd.append('--mpd_output')
    cmd.append(os.path.join(path_output, 'stream_dash.mpd'))
    cmd.append('--hls_master_playlist_output')
    cmd.append(os.path.join(path_output, 'stream_hls.m3u8'))
    print_cmd(cmd)
    subprocess.call(cmd, cwd=path_output)

def shaka_pack_to_dash_hls_orig(path_video, path_audio, video_codec='h264', path_subs=None, path_output='.'):
    cmd = ['packager']
    cmd.append('in='+path_audio+',stream=audio,init_segment=audio/init.mp4,segment_template=audio/$Number$.m4s')
    cmd.append('in='+path_video+',stream=video,init_segment='+video_codec+'/init.mp4,segment_template='+video_codec+'/$Number$.m4s')
    if path_subs is not None:
        cmd.append('in='+path_subs+',stream=text,init_segment=text/init.mp4,segment_template=text/$Number$.m4s,dash_only=1')
        cmd.append('in='+path_subs+',stream=text,segment_template=text/$Number$.vtt,hls_only=1')
    cmd.append('--generate_static_live_mpd')
    cmd.append('--mpd_output')
    cmd.append(os.path.join(path_output, 'stream_dash.mpd'))
    cmd.append('--hls_master_playlist_output')
    cmd.append(os.path.join(path_output, 'stream_hls.m3u8'))
    print_cmd(cmd)
    subprocess.call(cmd, cwd=path_output)

def conv_to_stream(path_input_video, path_output_stream_location, no_encoding=False, path_input_subtitles=None):
    if os.path.exists(path_input_video) is False:
        print('Specified video file path: {} does not exist'.format(path_input_video))
        exit(-1)
    if os.path.exists(path_output_stream_location) is False:
        print('Specified output path: {} does not exist. Creating it'.format(path_output_stream_location))
        os.makedirs(path_output_stream_location)
    #Subtitles part, prefer SRT and convert to web VTT
    path_subs = None
    if path_input_subtitles is not None:
        path_subs = ffmpeg_convert_subtitles_to_vtt(path_input_subtitles, path_output_stream_location)
    if path_subs is None:
        path_subs = ffmpeg_extract_subtitles(path_input_video, path_output_stream_location)
        if path_subs is None:
            path_subs = qnapi_download_subtitles(path_input_video, path_output_stream_location)
    # Audio part, prefer AAC
    path_audio = ffmpeg_extract_audio(path_input_video, path_output_stream_location)

    if no_encoding is True:
        path_video = ffmpeg_copy_video(path_input_video, path_output_stream_location)
        shaka_pack_to_dash_hls_orig(path_video, path_audio, path_subs, path_output_stream_location)
        os.remove(path_video)
    else:
        if ffmpeg_is_h264(path_input_video):
            path_video = ffmpeg_copy_video(path_input_video, path_output_stream_location)
            shaka_pack_to_dash_hls_orig(path_video, path_audio, 'h264', path_subs, path_output_stream_location)
            os.remove(path_video)
        elif ffmpeg_is_h265(path_input_video):
            path_video = ffmpeg_copy_video(path_input_video, path_output_stream_location)
            shaka_pack_to_dash_hls_orig(path_video, path_audio, 'h265', path_subs, path_output_stream_location)
            os.remove(path_video) 
        else:
            path_video_1920 = ffmpeg_convert_video(path_input_video, path_output_stream_location, 1920)
            shaka_pack_to_dash_hls(path_video_1920, path_audio, path_subs, path_output_stream_location)
            os.remove(path_video_1920)

    os.remove(path_audio)
    if path_subs is not None:
        os.remove(path_subs)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please specify paths to input video file and output stream location')
        sys.exit()

    if len(sys.argv) == 5:
        conv_to_stream(os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]), sys.argv[3], os.path.abspath(sys.argv[4]))
    else:
        conv_to_stream(os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]))
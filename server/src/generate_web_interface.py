#!/usr/bin/env python

import os
import sys
import glob
from jinja2 import Environment, FileSystemLoader

def generate_web_interface(path_input_stream, path_output_html):
    index_html_name = 'index.html'
    path_template = './templates'
    path_index_html_full = os.path.join(path_output_html, index_html_name)
    
    if os.path.exists(path_output_html) is False:
        os.makedirs(path_output_html)
    else:
        html_files = glob.glob(path_output_html+'/*.html')
        for file in html_files:
            os.remove(file)
            
    j2_env = Environment(loader=FileSystemLoader(path_template),trim_blocks=True)

    html = open(path_index_html_full,"w+")

    html.write('<html>\n')
    html.write('\t<head>\n')
    html.write('\t\t<title>HoViStream</title>\n')
    html.write('\t\t<h1 style="color:red;">List of movies:</h1>\n')
    html.write('\t</head>\n')
    html.write('\t<body style="background-color:black;">\n')
    html.write('\t\t<ul>\n')
    for movie_name in os.listdir(path_input_stream):
        html.write('\t\t\t<li style="color:red;"><h2><a href="'+movie_name+'.html" style="color:red;">'+movie_name+'</a></h2></li>\n')
        path_movie_page = os.path.join(path_output_html, movie_name+'.html')
        if os.path.isfile(path_movie_page) is True:
            os.remove(path_movie_page)
        html_stream = open(path_movie_page,"w+")
        html_content = j2_env.get_template('template_stream.html').render(stream_name=movie_name)
        html_stream.write(html_content)
        html_stream.close
        print('Page written to '+path_movie_page)
    html.write('\t\t</ul>\n')
    html.write('\t</body>\n')
    html.write('</html>')
    html.close()
    print('Main page written to '+path_index_html_full)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please specify paths to input stream and output html location')
        sys.exit()
    else:
        generate_web_interface(os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]))
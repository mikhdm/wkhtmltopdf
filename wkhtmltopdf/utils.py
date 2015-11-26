# -*- coding: utf-8 -*-

import os
import sys
import shlex
import random
import subprocess

from itertools import chain


PY3 = sys.version_info[0] == 3


if PY3:
	text_type = str
else:
	text_type = unicode


def _options_to_args(**options):

    flags = []
    for name in sorted(options):
        value = options[name]
        if value is None:
            continue
        flags.append('--' + name.replace('_', '-'))
        if value is not True:
            flags.append(text_type(value))
    return flags


def wkhtmltopdf(pages, output=None, **kwargs): # wkhtmltopdf cmd wrapper
	if output is None:
		output = '-'
	
	options = {'quiet': True}
	options.update(kwargs)
	options.setdefault('encoding', 'utf-8')

	cmd = 'WKHTMLTOPDF_CMD' # system env variable name
	cmd = os.environ.get(cmd, 'xvfb-run wkhtmltopdf')

	args = list(chain(shlex.split(cmd), _options_to_args(**options), list(pages), [output]))
	return subprocess.check_output(args, stderr=sys.stderr)


def htmltopdf(html, delete_html=False):
	params = {
		'pages': [html],
		'dpi': 300,
		'margin_top': 15,
		'margin_bottom': 20,
		'margin_left': 20,
		'margin_right': 10,
		'header_right': '[page]',
		'header_spacing': 5,
		'no-stop-slow-scripts': True
	}

	# generate pdf file 
	blob = wkhtmltopdf(**params)
	if delete_html:
		os.remove(html)
	
	return blob


def get_temp_filename( path=None, ext="", strlen=16 ):

	digits = "".join(map(str, range(0, 10)))
	symbols = "".join(map(chr, range(97, 123))) 

	def random_string( strlen = 32 ):
		return "".join( random.sample("".join([digits, symbols]), strlen))
	
	filename = "{0}{1}".format(
		random_string( strlen ),
		ext
	)
	return filename if path is None else os.path.join( path, filename )


def tmp_path_name():
	hash_ = get_temp_filename(strlen=8)
	path = os.path.join('/tmp', '{0}.html'.format(hash_))
	return path 

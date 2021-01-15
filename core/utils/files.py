import os

text_extensions = set(['dyalog', 'apl', 'asc', 'pgp', 'sig', 'asn', 'asn1', 'b', 'bf', 'c', 'h', 'ino', 'cpp', 'c++', 'cc', 'cxx', 'hpp', 'h++', 'hh', 'hxx', 'cob', 'cpy', 'cs', 'clj', 'cljc', 'cljx', 'cljs', 'gss', 'cmake', 'cmake.in', 'coffee', 'cl', 'lisp', 'el', 'cyp', 'cypher', 'pyx', 'pxd', 'pxi', 'cr', 'css', 'cql', 'd', 'dart', 'diff', 'patch', 'dtd', 'dylan', 'dyl', 'intr', 'ecl', 'edn', 'e', 'elm', 'ejs', 'erb', 'erl', 'factor', 'forth', 'fth', '4th', 'f', 'for', 'f77', 'f90', 'f95', 'fs', 's', 'feature', 'go', 'groovy', 'gradle', 'haml', 'hs', 'lhs', 'hx', 'hxml', 'aspx', 'html', 'htm', 'handlebars', 'hbs', 'pro', 'jade', 'pug', 'java', 'jsp', 'js', 'json', 'map', 'jsonld', 'jsx', 'j2', 'jinja', 'jinja2', 'jl', 'kt', 'less', 'ls', 'lua', 'markdown', 'md', 'mkd', 'm', 'nb', 'wl', 'wls', 'mo', 'mps', 'mbox', 'nsh',
                       'nsi', 'nt', 'nq', 'mm', 'ml', 'mli', 'mll', 'mly', 'oz', 'p', 'pas', 'pl', 'pm', 'php', 'php3', 'php4', 'php5', 'php7', 'phtml', 'pig', 'txt', 'text', 'conf', 'def', 'list', 'log', 'pls', 'ps1', 'psd1', 'psm1', 'properties', 'ini', 'in', 'proto', 'BUILD', 'bzl', 'py', 'pyw', 'pp', 'q', 'r', 'R', 'rst', 'spec', 'rb', 'rs', 'sas', 'sass', 'scala', 'scm', 'ss', 'scss', 'sh', 'ksh', 'bash', 'siv', 'sieve', 'slim', 'st', 'tpl', 'sml', 'fun', 'smackspec', 'soy', 'rq', 'sparql', 'sql', 'nut', 'styl', 'swift', 'ltx', 'tex', 'v', 'sv', 'svh', 'tcl', 'textile', 'toml', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ttcn', 'ttcn3', 'ttcnpp', 'cfg', 'ttl', 'ts', 'tsx', 'webidl', 'vb', 'vbs', 'vtl', 'vhd', 'vhdl', 'vue', 'xml', 'xsl', 'xsd', 'svg', 'xy', 'xquery', 'ys', 'yaml', 'yml', 'z80', 'mscgen', 'mscin', 'msc', 'xu', 'msgenny'])

image_extensions = set(['apng', 'bmp', 'gif', 'ico', 'cur', 'jpg',
                        'jpeg', 'jfif', 'pjpeg', 'pjp', 'png', 'svg', 'tif', 'tiff', 'webp'])


def get_file_type(file_name):
    ext = os.path.splitext(file_name)[1]
    if ext.startswith('.'):
        ext = ext[1:]
    if ext in text_extensions:
        return 'text'
    elif ext in image_extensions:
        return 'image'
    else:
        return 'unknown'

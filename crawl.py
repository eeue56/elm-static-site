#!/usr/bin/env python3
import os

def build_up(dirname):
    names = []

    for (dir_path, dir_names, filenames) in os.walk(dirname):
        for just_filename in filenames:
            filename = os.path.join(dir_path, just_filename)

            if not filename.endswith('.elm'):
                continue

            if filename.endswith('/') or ('/.') in filename:
                continue

            if not has_view(filename):
                continue

            names.append(filename)

    return [ name.replace(dirname + '/', '', 1) for name in names ]


def generate_port(module_name):
    return """
port {port_name} : String
port {port_name} =
    {module_name}.view
        |> render
""".format(port_name=port_name(module_name), module_name=module_name)

def generate_import(module_name):
    return "import {filename}".format(filename=module_name)

def port_name(module_name):
    return module_name.replace('.', '').lower()

def file_name(module_name, basedir=None, with_lower=True):
    if basedir is None:
        basedir = './'
    with_basedir = basedir + module_name.replace('.', '/')

    if with_lower:
        return with_basedir.lower()
    return with_basedir

def make_folders(file_names):
    for file_name in file_names:
        if file_name.count('/') > 1 or not file_name.startswith('.'):
            dir = file_name[:file_name.rfind('/')]
            try:
                os.mkdir(dir)
            except OSError:
                pass

def generate_mapping(port, file):
    return """
echo "fs.writeFile('{file}.html', elm.ports['{port}']);" >> _main.js
""".format(port=port, file=file.lower())


def generate_vdom(module_names, basedir=None):
    """ expects a list of elm module name e.g Index.elm
    """

    port_files = { port_name(name): file_name(name, basedir=basedir) for name in module_names }

    ports = '\n'.join(generate_port(name) for name in module_names)
    imports = '\n'.join(generate_import(name) for name in module_names)
    mappings = '\n'.join(generate_mapping(port, file) for port, file in port_files.items())

    make_folders(port_files.values())

    renderer_filename = '_Renderer.elm'
    runner_filename = './runner.sh'

    template = """
module Renderer where
import Html exposing (Html)
import Native.Renderer

{imports}

render : Html -> String
render = Native.Renderer.toHtml

{ports}
""".format(imports=imports, ports=ports)

    with open(renderer_filename, 'w') as f:
        f.write(template)

    executor = """
elm make {renderer} --output=_main.js
echo "var fs = require('fs');" >> _main.js
echo "var elm = Elm.worker(Elm.Renderer);" >> _main.js
{mappings}
node _main.js

""".format(mappings=mappings, renderer=renderer_filename)

    with open(runner_filename, 'w') as f:
        f.write(executor)

    make_executable(runner_filename)

    execute_bash(runner_filename)

def clean_up(name):
    return name[:name.rfind('.elm')].replace('/', '.')

def has_view(filename):
    with open(filename) as f:
        for line in f:
            if line.startswith('view ='):
                return True
    return False

def execute_bash(filename):
    os.system(filename)

def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2    # copy R bits to X
    os.chmod(path, mode)

def main():
    print('calling examples')
    without_dots = [clean_up(example) for example in build_up('examples')]

    generate_vdom(without_dots, basedir='output/')

if __name__ == '__main__':
    main()

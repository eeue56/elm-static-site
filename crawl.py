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

            names.append(filename)

    return [ name.replace(dirname + '/', '', 1) for name in names ]


def generate_port(module_name):
    return """
port {port_name} : String
port {port_name} =
    {module_name}.view
        |> Native.Renderer.toHtml
""".format(port_name=port_name(module_name), module_name=module_name)

def generate_import(module_name):
    return "import {filename}".format(filename=module_name)

def port_name(module_name):
    return module_name.replace('.', '').lower()

def file_name(module_name, basedir=None):
    if basedir is None:
        basedir = './'
    return basedir + module_name.replace('.', '/')

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

    template = """
module Renderer where
import Native.Renderer
{imports}

{ports}
""".format(imports=imports, ports=ports)

    with open('Renderer.elm', 'w') as f:
        f.write(template)

    executor = """
elm make Renderer.elm --output=_main.js
echo "var fs = require('fs');" >> _main.js
echo "var elm = Elm.worker(Elm.Renderer);" >> _main.js
{mappings}
node _main.js

""".format(mappings=mappings)

    with open('runner.sh', 'w') as f:
        f.write(executor)

def clean_up(name):
    return name[:name.rfind('.elm')].replace('/', '.')

def main():
    print('calling examples')
    without_dots = [clean_up(example) for example in build_up('examples')]

    generate_vdom(without_dots, basedir='output/')

if __name__ == '__main__':
    main()
var fs = require('fs');
var glob = require('glob');
var linebyline = require('n-readlines');
var cmd = require('node-cmd');
var spawn = require('cross-spawn');

function listFiles(path) {
    var filelist = [];
    var files =  glob.sync(path + '**').filter(isFile);

    var files = files.filter(function(file){
      return getFilename(file).split('.')[1] === 'elm';
    }).filter(hasView).map(function(file) {
        return file.replace(path, '');
    });

    return files;
}

function generatePort(module_name) {
    var port_name = portName(module_name);
    return `
port ${port_name} : String 
port ${port_name} =
    ${module_name}.view 
        |> render`;
}

function generateImport(module_name) {
    return `import ${module_name}`;
}

function portName(module_name) {
    return module_name.replace('.','').toLowerCase();
}

function fileName(module_name, basedir, with_lower) {

    if (basedir === null) {
        basedir = './';
    } 
    var with_basedir = basedir + module_name.replace('.','/');

    if (with_lower) {
        return with_basedir.toLowerCase();
    } 
    return with_basedir;
}

function generateMapping(port, file) {
    return `echo "fs.writeFile('${file}.html', elm.ports['${port}']);" >> _main.js`;
}

function generate_vdom(module_names, basedir) {

    var port_files = [];

    for (var i = module_names.length - 1; i >= 0; i--) {
        port_files.push({
            'port' : portName(module_names[i]),
            'filename' : fileName(module_names[i], basedir, false)
        });
    }

    var ports = module_names.map(generatePort).join('\n');
    var imports = module_names.map(generateImport).join('\n');

    var port_file_values = port_files.map(function(curr) {
        return curr.filename;
    });

    var maps = port_files.map(function(curr) {
        return generateMapping(curr.port, curr.filename);
    });

    var mappings = maps.join('\n');

    makeFolders(port_file_values);


    var renderer_filename = '_Renderer.elm';
    var runner_filename = './runner.sh';

    var template = `
module Renderer where
import Html exposing (Html)
import Native.Renderer

${imports}

render : Html -> String
render = Native.Renderer.toHtml

${ports}`;

    fs.writeFile(renderer_filename, template);

    var executor = `
#!/bin/sh
elm-package install --yes
elm make ${renderer_filename} --output=_main.js
echo "var fs = require('fs');" >> _main.js
echo "var elm = Elm.worker(Elm.Renderer);" >> _main.js
${mappings}
node _main.js`;

    fs.writeFileSync(runner_filename, executor);

    executeBash(runner_filename);
}

function makeFolders(filenames) {

    filenames.forEach(function(filename) {
        if (filename.split('/').length > 1 || filename.startsWith('.') != -1) {
            var dir = filename.substring(0, filename.lastIndexOf('/'));
            try {
                fs.mkdir(dir);
            } catch (err) {
                console.error(err);
            }
        }
    });
}

function isFile(path) {
    return fs.lstatSync(path).isFile();
}

function getFilename(path) {
    var parts = path.split('/');
    return parts[parts.length - 1];
}

function hasView(filename) {
    var liner = new linebyline(filename);
    var line;

    while (line = liner.next()) {
        if (line.indexOf('view =') != -1) {
            return true;
        }
    } 
    return false;
}

function cleanUp(name) {
    var new_name = name.replace(__dirname, '');
    return new_name.split('.')[0].replace('/', '.');
}

function executeBash(filename) {
    fs.chmod(filename, 0755);
    var results = spawn('sh', [filename], { stdio: 'inherit' });

}

function main() {
    var files = listFiles('examples/').map(cleanUp);

    generate_vdom(files, 'output/');
}

main();
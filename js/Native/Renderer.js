var make = function make(localRuntime) {
    localRuntime.Native = localRuntime.Native || {};
    localRuntime.Native.Renderer = localRuntime.Native.Renderer || {};

    var toHtml = require('vdom-to-html');

    return {
        'toHtml': toHtml
    };
};

Elm.Native = Elm.Native || {};
Elm.Native.Renderer = Elm.Native.Renderer || {};
Elm.Native.Renderer.make = make;

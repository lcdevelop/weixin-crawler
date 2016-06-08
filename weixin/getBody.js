var page = require('webpage').create();
var system = require('system');
page.open(system.args[1], function(status) {
    var sc = page.evaluate(function() {
        return document.body.innerHTML;
    });
    window.setTimeout(function() {
        console.log(sc);
        phantom.exit();
    }, 100);
});

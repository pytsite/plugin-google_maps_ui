const path = require('path');

module.exports = {
    entry: [
        path.join(__dirname, 'index.js'),
        path.join(__dirname, 'widget-static-map.js'),
        path.join(__dirname, 'widget-address-input.js'),
    ],
};

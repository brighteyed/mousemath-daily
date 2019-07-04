const path = require('path');

module.exports = {
  entry: './main.js',

  output: {
    path: path.resolve(__dirname, 'public'),
    filename: 'bundle.js'
  },

  devtool: 'source-map'
};
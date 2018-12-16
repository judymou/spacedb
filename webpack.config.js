module.exports = {
  mode: 'development',
  entry: './client/index.js',
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: ['babel-loader'],
      },
    ],
  },
  resolve: {
    extensions: ['*', '.js', '.jsx'],
  },
  output: {
    path: __dirname + '/static/dist/js',
    publicPath: '/',
    filename: 'bundle.js',
  },

};

const path = require('path');
const HtmlWebPackPlugin = require("html-webpack-plugin");
const htmlPlugin = new HtmlWebPackPlugin({
 template: "./src/index.html",
 filename: "./index.html",
 favicon: "./public/favicon.ico"
});
module.exports = {
mode: 'development',
entry: './src/index.js',
output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'webpack.bundle.js',
  },
  module: {
    rules: [{
   test: /\.js$/,
   exclude: /node_modules/,
   use: {
     loader: "babel-loader"
   }
 },
  {
   test: /\.css$/,
   use: ["style-loader", "css-loader"]
 },
 {
    test: /\.js$/,
    enforce: 'pre',
    use: ['source-map-loader'],
  },
]},
devServer: {
   liveReload: true,
   historyApiFallback: true,
   proxy: {
     '/api': {
       target: 'http://localhost:5000',
       pathRewrite: { '^/api': '' },
     },
    },
 },
 plugins: [htmlPlugin]
};

var debug = process.env.NODE_ENV !== "production";
var webpack = require('webpack');
var path = require('path');
var _ = require('lodash');

var ExtractTextPlugin = require('extract-text-webpack-plugin');
var ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');

var rootAssetPath = path.join(__dirname, "reddit_web_app", "assets");
var relativeRootAssetPath = "./reddit_web_app/assets";
var outputPath = path.join(__dirname, "reddit_web_app", "static");
var publicHost = debug ? 'http://localhost:2992' : 'http://localhost';
var publicPath = publicHost + (debug ? '/assets/' : '/static/build/');


module.exports = {
  devtool: debug ? "inline-sourcemap" : null,
  entry: {
    app_js: [
      path.join(rootAssetPath, "/js/main")
    ],
    app_css: [
        path.join(rootAssetPath, '/css/main')
    ]
  },
  output: {
    path: path.join(outputPath, "build"),
    publicPath: publicPath,
    filename: "[name].[hash].js",
    chunkFilename: "[id].[hash].js",
  },
  resolve: {
    extensions: ['', '.js', '.jsx', '.css']
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        include: path.join(rootAssetPath, 'js'),
        exclude: /(node_modules|bower_components)/,
        loaders: ['babel-loader'],
      },
      {
        test: /\.css$/,
        loader: ExtractTextPlugin.extract("style-loader", "css-loader"),
      },
      {
        test: /\.(jpe?g|png|gif|svg)$/,
        loaders: [
            'file?context=' + relativeRootAssetPath + '&name=[path][name].[hash].[ext]',
            'image?bypassOnDebug&optimizationLevel=7&interlaced=false',
        ]
      },
    ]
  },
  plugins: _.concat([
      new webpack.NoErrorsPlugin(),
      new ExtractTextPlugin('[name].[hash].css'),
      new ManifestRevisionPlugin(path.join(outputPath, 'manifest.json'), {
        rootAssetPath: relativeRootAssetPath,
        ignorePaths: ['/js', '/css'],
      })
    ],
    debug ? [
        new webpack.HotModuleReplacementPlugin(),
    ] : [
        new webpack.optimize.DedupePlugin(),
        new webpack.optimize.OccurenceOrderPlugin(),
        new webpack.optimize.UglifyJsPlugin({ mangle: false, sourcemap: false }),
    ]
  ),
};

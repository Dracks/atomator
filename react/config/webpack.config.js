const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const TerserJSPlugin = require('terser-webpack-plugin');
const path = require('path');

const rootDir = __dirname + "/.."

const isProduction = process.env.NODE_ENV == "production" || false
const hash = isProduction ? ".[hash]" : "";

module.exports = {
    entry:  {
        main: path.resolve(rootDir, 'src/index.tsx')
    },
    mode: isProduction? "production" : 'development',
    node: {
        fs: 'empty'
    },
    output: {
        path: path.resolve(rootDir, '../static'),
        filename: `react/[name]${hash}.js`,
        publicPath: '/',
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: './src/index.html',
            filename: '../atomator/templates/react.html',
            inject: false,
        }),
        new MiniCssExtractPlugin({
            // Options similar to the same options in webpackOptions.output
            // both options are optional
            filename: `react/[name]${hash}.css`,
            chunkFilename: `react/[id]${hash}.css`,
        }),
    ],
    resolve: {
        extensions: ['.mjs', '.ts', '.tsx', '.js', '.jsx', '.scss'],
        modules: [ 'node_modules' ]
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                exclude: [
                    /node_modules/,
                ],
                use: [
                    {
                        loader: "ts-loader",
                        options: {
                            configFile: path.resolve(rootDir, "config/tsconfig.build.json"),
                            transpileOnly: true,
                            experimentalWatchApi: true,
                        }
                    }
                ]
            },
            {
                test: /\.s[ac]ss$/i,
                use: [
                  // Creates `style` nodes from JS strings
                  // 'style-loader',
                  // To extract in separated files
                  MiniCssExtractPlugin.loader,
                  // Translates CSS into CommonJS
                  'css-loader',
                  // Compiles Sass to CSS
                  'sass-loader',
                ],
            },
        ]
    },
    optimization: {
        splitChunks: {
            chunks: 'all',
        },
        minimizer: [new TerserJSPlugin({}), new OptimizeCSSAssetsPlugin({})],
    },
    devtool: "source-map"
}
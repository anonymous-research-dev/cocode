const argv = require('yargs').argv;
const webpack = require('webpack');
const webpackConfig = require('./webpack.config');

module.exports = params => {
    const config = webpackConfig(params);
    return {
        ...config,
        output: {
            ...config.output,
            publicPath: `/static/web/`,
        },
        devtool: argv.devtool || '#eval-source-map',
        plugins: [
            ...config.plugins,
            new webpack.LoaderOptionsPlugin({
                debug: true,
            }),
        ],
    };
};

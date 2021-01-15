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
        devtool: 'source-map',
        plugins: [
            ...config.plugins,
            new webpack.LoaderOptionsPlugin({
                minimize: true,
            }),
        ],
    };
};

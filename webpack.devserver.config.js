module.exports = {
    quiet: false,
    historyApiFallback: true,
    contentBase: './static',
    publicPath: '/web/',
    stats: {
        colors: true
    },
    headers: {
        'Access-Control-Allow-Origin': '*',
    }
};
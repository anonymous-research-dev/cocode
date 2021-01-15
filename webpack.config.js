const path = require('path');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const babelConfig = require('./.babelrc');

module.exports = params => ({
	cache: true,
	context: path.join(__dirname, './web'),
	entry: {
		main: ['./index.js'],
		brython: ['./brython.js'],
		course: ['./course.js'],
		exercise: ['./exercise.js'],
		polyfill: ['babel-polyfill'],
	},
	output: {
		path: path.join(__dirname, './static/web'),
		publicPath: `/web/`,
		filename: '[name].js',
		chunkFilename: '[chunkhash].js',
		sourceMapFilename: '[name].js.map',
	},
	resolve: {
		alias: {
			'@': path.resolve(__dirname, './static/web'),
		},
		extensions: ['.js', '.vue'],
		modules: ['node_modules'],
	},
	module: {
		rules: [
			{
				test: /\.css$/,
				use: ['vue-style-loader', 'style-loader', 'css-loader'],
			},
			{
				test: /\.scss$/,
				use: ['vue-style-loader', 'style-loader', 'css-loader', 'sass-loader'],
			},
			{
				test: /\.worker\.js$/,
				loader: 'worker-loader',
			},
			{
				test: /\.js?$/,
				include: [path.resolve(__dirname, './web/')],
				loader: 'babel-loader',
				options: babelConfig,
			},
			{
				test: /\.vue$/,
				include: [path.resolve(__dirname, './web/')],
				loader: 'vue-loader',
			},
			{
				test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
				use: [{
					loader: 'file-loader',
					options: {
						name: '[name].[ext]',
						outputPath: 'fonts/',
					},
				}],
			},
			{
				test: /\.(png|jpg|gif)$/,
				use: [{
					loader: 'file-loader',
					options: {}
				}]
			}
		],
	},
	plugins: [
		new VueLoaderPlugin(),
	],
});

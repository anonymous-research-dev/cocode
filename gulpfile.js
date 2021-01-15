const argv = require('yargs').argv
const shell = require('shelljs');
const fs = require('fs');
const express = require('express');
const http = require('http');
const httpProxy = require('http-proxy');
const findFreePort = require('find-free-port');
const glob = require('glob');
const gulp = require('gulp');
const mergeStream = require('merge-stream');
const rename = require('gulp-rename');
const PluginError = require('plugin-error');
const log = require('fancy-log');
const del = require('del');
const vinylPaths = require('vinyl-paths');
const webpack = require('webpack');
const WebpackDevServer = require('webpack-dev-server');
const webpackDevConfig = require('./webpack.config.dev');
const webpackProdConfig = require('./webpack.config.prod');
const webpackDevServerConfig = require('./webpack.devserver.config');
const spawn = require('child_process').spawn;
const host = argv.host || 'localhost';
const basePort = argv.port || 8080;
const ports = {};
const webpackConfigParams = { host, ports };

gulp.task('set-ports', callback => {
    findFreePort(basePort, basePort + 2000, host, 4, (err, port1, port2, port3, port4) => {
        if (err) {
            throw new PluginError('find-ports', 'Failed to find available ports.', err);
        }
        ports.proxy = port1;
        ports.django = port2;
        ports.webpack = port3;
        ports.redis = port4
        callback();
    });
});

gulp.task('init-python-env', callback => {
    if (!fs.existsSync("./env")) {
        if (shell.exec('python3 -m venv ./env').code !== 0) {
            throw new PluginError('init-python-env', 'Python virtual environment initialization failed.');
        }
    }
    callback();
});

gulp.task('run-pip-freeze', () => {
    if (shell.exec('./env/bin/pip3 freeze > requirements.txt').code !== 0) {
        throw new PluginError('run-pip-freeze', 'Pip freeze failed.');
    }
});

gulp.task('run-pip-install', callback => {
    if (shell.exec('./env/bin/pip3 install -r requirements.txt').code !== 0) {
        throw new PluginError('run-pip-install', 'Pip install failed.');
    }
    callback()
});

gulp.task('copy-course-files', () => {
    return glob(
        './node_modules/cocode-courses/*/materials/*/serve/*',
        (err, paths) => {
            return mergeStream(
                paths.map(path => {
                    const tokens = path.split('/');
                    const courseId = tokens[tokens.length - 5];
                    const materialId = tokens[tokens.length - 3];
                    return gulp
                        .src(path)
                        .pipe(gulp.dest(`./static/courses/${courseId}/${materialId}`));
                })
            );
        }
    );
});

gulp.task('run-develop-django', () => {
    log('[run-develop-django]', `Run Django development server on localhost:${ports.django}.`);
    const runserver = spawn('./env/bin/python', [
        'manage.py',
        'runserver',
        `localhost:${ports.django}`,
        ...(argv.settings ? ['--settings', argv.settings] : []),
        '--fromnode',
    ], { 
        stdio: 'inherit',
        env: {
            ...process.env,
            REDIS_HOST: 'localhost',
            REDIS_PORT: ports.redis,
        },
    });
    runserver.on('exit', code => {
        if (code !== 0) {
            throw new PluginError('run-develop-django', 'Django runserver failed.');
        }
    });
    process.on('SIGINT', () => {
        runserver.kill();
    });
});
gulp.task('run-webpack-dev-server', () => {
    const config = {
        ...webpackDevConfig(webpackConfigParams),
        mode: 'development',
    };
    const devServer = new WebpackDevServer(webpack(config), webpackDevServerConfig);
    devServer.listen(ports.webpack, '127.0.0.1', err => {
        if (err) {
            throw new PluginError('run-webpack-dev-server', 'Failed to run webpack dev server.', err);
        }
        log('[run-webpack-dev-server]', `Run webpack dev server on ${host}:${ports.webpack}.`);
    });
});

gulp.task('run-develop-redis', () => {
    log('[run-develop-redis]', `Run redis server on ${host}:${ports.redis}.`);
    const runserver = spawn('redis-server', [
        '--port',
        ports.redis + '',
        '--bind',
        host,
    ], { stdio: 'inherit' });
    runserver.on('exit', code => {
        if (code !== 0) {
            throw new PluginError('run-develop-redis', 'Redis failed.');
        }
    });
    process.on('SIGINT', () => {
        runserver.kill();
    });
});

gulp.task('run-proxy', () => {
    const djangoProxy = httpProxy.createProxyServer({
        target: {
            host: 'localhost',
            port: ports.django,
            ws: true,
        },
    });
    djangoProxy.on('error', err => {
        log('[run-proxy]', `Error on Django proxy.`, err);
    });
    const webpackProxy = httpProxy.createProxyServer({
        target: {
            host: '127.0.0.1',
            port: ports.webpack,
        },
    });
    webpackProxy.on('error', err => {
        log('[run-proxy]', `Error on Webpack proxy.`, err);
    });
    const app = express();
    app.all('/static/*', (req, res) => {
        req.url = req.url.slice('/static'.length); // Trim "/static" at the beginning.
        webpackProxy.web(req, res);
    });
    
    app.all('/*', (req, res) => {
        djangoProxy.web(req, res);
    });
    
    const server = http.createServer(app);
    server.on('upgrade', (req, socket, head) => {
        djangoProxy.ws(req, socket, head);
    });
    server.listen(ports.proxy);
    process.on('SIGINT', () => {
        server.close();
    });
});

gulp.task('run-dev-servers', callback => {
    log('[run-dev-servers]', `Central proxy server running on ${host}:${ports.proxy}.`);
    callback();
});

gulp.task('webpack-build', callback => {
    webpack(webpackProdConfig(webpackConfigParams), (err, stats) => {
        if (err) {
            throw new PluginError('webpack-build', err);
        }
        log('[webpack-build]', stats.toString({
            colors: true,
            chunks: !argv.quiet,
        }));
        if (stats.hasErrors()) {
            throw new PluginError('webpack-build', 'Compile errors have occurred.');
        }
        callback();
    });
});

gulp.task('rename-env', () => {
    return gulp.src('./env/**/*.po')
        .pipe(vinylPaths(del))
        .pipe(rename(path => {
            path.extname = '.pobak';
        }))
        .pipe(gulp.dest('./env'));
});

gulp.task('run-compilemessages', callback => {
    if (shell.exec('./env/bin/python manage.py compilemessages').code !== 0) {
        throw new PluginError('init-python-env', 'Python virtual environment initialization failed.');
    }
    callback();
});

gulp.task('restore-env', () => {
    return gulp.src('./env/**/*.pobak')
        .pipe(vinylPaths(del))
        .pipe(rename(path => {
            path.extname = '.po';
        }))
        .pipe(gulp.dest('./env'));
});

gulp.task('run-makemessages', callback => {
    const args = process.argv.slice(3);
    const cmdArgs = [
        './env/bin/python',
        'manage.py',
        'makemessages',
        '-i',
        'env',
        '-i',
        'static',
        '-i',
        'requirements.txt',
    ];
    args.forEach(arg => cmdArgs.push(arg));
    const cmd = cmdArgs.map(arg => `"${arg.replace(/\"/g, '\\"')}"`).join(' ');
    if (shell.exec(cmd).code !== 0) {
        throw new PluginError('init-python-env', 'Python virtual environment initialization failed.');
    }
    callback();
});

gulp.task('remove-gettext-vue', () => {
    return gulp.src('./vue-gettexts.js')
        .pipe(vinylPaths(del));
})

gulp.task('extract-gettext-vue', callback => {
    const extractPhrases = text => {
        const findAll = re => {
            let m;
            const results = [];
            do {
                m = re.exec(text);
                if (m) {
                    results.push(m[1]);
                }
            } while (m);
            return results;
        };
        const res = [
            /gettext\(\s*('[^'\\]*(?:\\.[^'\\]*)*')\s*\)/g,
            /gettext\(\s*("[^"\\]*(?:\\.[^"\\]*)*")\s*\)/g,
            /gettext\(\s*(`[^`\\]*(?:\\.[^`\\]*)*`)\s*\)/g,
        ];
        const phrases = [];
        for (const re of res) {
            findAll(re).forEach(p => phrases.push(p));
        }
        return phrases;
    };

    glob('**/*.vue', {
        ignore: [
            'node_modules/**/*',
            'static/**/*',
        ],
    }, (err, filenames) => {
        if (err) {
            throw new PluginError('naive-extract-gettext-vue', err);
        }
        const phrases = []
        for (const filename of filenames) {
            const body = fs.readFileSync(filename, { encoding: 'utf-8' });
            extractPhrases(body).forEach(p => phrases.push(p));
        }
        
        const output = [
            '// This file is auto-generated.',
            '// Please do NOT manually modify this file.',
            ...([...new Set(phrases)].map(p => `gettext(${p});`)),
        ].join('\n');
        fs.writeFileSync('./vue-gettexts.js', output);
        callback();
    });
});

gulp.task('run-makemessages-js', callback => {
    const args = process.argv.slice(3);
    const cmdArgs = [
        './env/bin/python',
        'manage.py',
        'makemessages',
        '-d',
        'djangojs',
        '-i',
        'node_modules',
        '-i',
        'static',
        '-e',
        'vue',
        '-e',
        'js',
    ];
    args.forEach(arg => cmdArgs.push(arg));
    const cmd = cmdArgs.map(arg => `"${arg.replace(/\"/g, '\\"')}"`).join(' ');
    if (shell.exec(cmd).code !== 0) {
        throw new PluginError('init-python-env', 'Python virtual environment initialization failed.');
    }
    callback();
});

gulp.task('makemessages', 
    gulp.series(
        gulp.parallel('run-makemessages', gulp.series('extract-gettext-vue', 'run-makemessages-js')), 
        'remove-gettext-vue'
    ),
)
gulp.task('compilemessages', gulp.series(
    'rename-env',
    'run-compilemessages',
    'restore-env',
));
gulp.task('pip-freeze', gulp.parallel('run-pip-freeze'));
gulp.task('postinstall', gulp.parallel(
    'copy-course-files',
    gulp.series(
        'init-python-env',
        'run-pip-install',
    ),
));

gulp.task('develop', gulp.series(
    'set-ports',
    gulp.parallel(
        'run-develop-django', 
        'run-webpack-dev-server', 
        'run-develop-redis', 
        'run-proxy',
    ),
    'run-dev-servers',
));
gulp.task('build', gulp.parallel('webpack-build'));

gulp.task('default', gulp.parallel('develop'));
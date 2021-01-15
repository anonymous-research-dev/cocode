
async function init(data) {
    self.window = self
    self.staticUrl = data.staticUrl
    self.print = msg => postMessage({
        type: 'stdout',
        value: msg,
    })
    self.printErr = msg => postMessage({
        type: 'stderr',
        value: msg,
    })
    self.sendMsg = (type, msg) => postMessage({
        type,
        value: msg
    })
    importScripts(
        self.staticUrl + 'brython/brython.js',
        self.staticUrl + 'brython/brython_stdlib.js',
        self.staticUrl + 'brython/brython_modules.js',
    )
    const paths = []
    if (data.cwdUrl) {
        paths.push(data.cwdUrl)
    }
    self.__BRYTHON__.brython({
        pythonpath: [
            ...paths,
            self.staticUrl + 'brython',
            self.staticUrl + 'brython/site-packages',
        ],
        debug: 1, // 10
    })
    self.__BRYTHON__._run_script({
        name: '__main__',
        src: 'import cocode.stdio',
    })
}

function run(data) {
    const code = self.__BRYTHON__._run_script({
        name: data.name || '__main__',
        src: data.src,
    })
    postMessage({
        type: 'done',
        value: code,
    })
}

onmessage = ({ data }) => {
    switch (data.type) {
        case 'init':
            init(data)
            break
        case 'run':
            run(data)
            break
        default:
            break
    }
}
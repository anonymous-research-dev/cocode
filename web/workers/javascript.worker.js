
const Compiler = require('@nx-js/compiler-util')

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
}

function run(data) {
    const webConsole = {
        log: (...messages) => {
            const value = messages.map(m => `${m}\n`).join('')
            postMessage({
                type: 'stdout',
                value,
            })
        },
        error: (...messages) => {
            const value = messages.map(m => `${m}\n`).join('')
            postMessage({
                type: 'stderr',
                value,
            })
        }
    }
    const grader = {
        print: (...messages) => {
            postMessage({
                type: 'grade-out',
                value: messages.map(m => `${m}\n`).join(''),
            })
        },
        setProgress: progress => {
            postMessage({
                type: 'grade-progress',
                value: `${progress}`,
            })
        },
        setStar: star => {
            postMessage({
                type: 'grade-star',
                value: `${star}`,
            })
        },
    }
    const expose = ['Date']
    let code = 0
    Compiler.expose(expose.join(','));
    try {
        const runCode = Compiler.compileCode(data.src + '\n');
        runCode({ 
            console: webConsole,
            __grader__: grader,
        });
    } catch (err) {
        webConsole.error(err.toString());
        code = 1
    }

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
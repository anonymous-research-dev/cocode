import BrythonWorkerSrc from '!!raw-loader!./workers/brython.worker.js'

function BrythonWorker() {
    window.URL = window.URL || window.webkitURL
    let blob;
    try {
        blob = new Blob([BrythonWorkerSrc], { type: 'application/javascript' })
    } catch (e) {
        window.BlobBuilder = window.BlobBuilder || window.WebKitBlobBuilder || window.MozBlobBuilder
        blob = new BlobBuilder()
        blob.append(BrythonWorkerSrc)
        blob = blob.getBlob()
    }
    return new Worker(URL.createObjectURL(blob))
}

class BrythonRunner {
    constructor(options = {}) {
        this.eventTarget = new EventTarget()
        this.brythonWorker = BrythonWorker()
        const params = {}
        params.staticUrl = this.getAbsUrl(__COCODE__.staticUrl)
        if (options.cwdUrl) {
            this.cwdUrl = options.cwdUrl
            params.cwdUrl = this.getAbsUrl(options.cwdUrl)
        }
        this.brythonWorker.postMessage({
            type: 'init',
            ...params,
        })
        this.brythonWorker.onmessage = msg => this.handleMessage(msg)
    }

    getAbsUrl(url) {
        if (url.startsWith('http://') || url.startsWith('https://')) {
            return url
        } else if (url.startsWith('/')) {
            return window.location.origin + url
        } else {
            return window.location.href + url
        }
    }

    handleMessage(msg) {
        switch (msg.data.type) {
            case 'done':
                this.done(msg.data.value)
                break;

            default:
                this.dispatch(msg.data.type, msg.data)
                break;
        }
    }

    run(src) {
        return new Promise(resolve => {
            this.done = code => resolve(code)
            this.brythonWorker.postMessage({
                type: 'run',
                src,
            })
        })
    }

    close() {
        this.brythonWorker.terminate();
    }

    on(type, listener) {
        this.eventTarget.addEventListener(type, listener)
    }

    dispatch(typeArg, detail, cancelable) {
        const event = new Event(typeArg, cancelable ? { cancelable: true } : {})
        Object.assign(event, { detail })
        return this.eventTarget.dispatchEvent(event)
    }
}

window.BrythonRunner = BrythonRunner
import BaseRunner from './base-runner'
import JavascriptWorker from '../workers/javascript.worker.js'

export default class JavascriptRunner extends BaseRunner {
    constructor(params = {}) {
        super(params)
        this.params = params
        this.eventTarget = new EventTarget()
        this.worker = JavascriptWorker()
        const workerParams = {}
        workerParams.staticUrl = __COCODE__.staticUrl
        this.worker.postMessage({
            type: 'init',
            ...workerParams,
        })
        this.worker.onmessage = msg => this.handleMessage(msg)
    }

    async init() {
        const { cwdUrl, isGrade, mainFile, value } = this.params
        if (isGrade) {
            const mainResponse = await axios.get(`${cwdUrl}/${mainFile}`)
            const mainContent = mainResponse.data
            const gradeResponse = await axios.get(`${cwdUrl}/__grade__.js`)
            const gradeContent = gradeResponse.data
            this.src = gradeContent.replace('{{main}}', mainContent).replace('{{main|jsonify}}', JSON.stringify(mainContent))
        } else {
            const response = await axios.get(`${cwdUrl}/${mainFile}`)
            this.src = response.data
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

    run() {
        return new Promise(resolve => {
            this.done = code => resolve(code)
            this.worker.postMessage({
                type: 'run',
                src: this.src,
            })
        })
    }

    close() {
        this.worker.terminate();
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
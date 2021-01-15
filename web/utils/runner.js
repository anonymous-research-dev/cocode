
import BaseRunner from './base-runner'
import JavascriptRunner from './javascript-runner'

export function createRunner(params) {
    const { mode } = params
    switch (mode) {
        case 'python3':
            return new PythonRunner(params)
        case 'javascript':
            return new JavascriptRunner(params)
    }
}

class PythonRunner extends BaseRunner {
    constructor(params = {}) {
        super(params)
        const { cwdUrl, isGrade, mainFile, value } = params
        this.instance = new BrythonRunner({ cwdUrl })
        this.isGrade = isGrade
        if (value !== undefined) {
            this.value = value
        } else {
            if (this.isGrade) {
                this.value = `import __grade__`
            } else {
                let mainLib = mainFile
                if (mainFile.endsWith('.py')) {
                    mainLib = mainFile.slice(0, mainFile.length - 3)
                }
                this.value = `import ${mainLib}`
            }
        }
    }

    on(type, listener) {
        this.instance.on(type, listener)
    }

    async run() {
        return await this.instance.run(this.value)
    }
}
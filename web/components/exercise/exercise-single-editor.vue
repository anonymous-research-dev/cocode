<template>
    <div class="exercise-single-editor u-fill">
        <div class="editor-container" ref="container"></div>
    </div>
</template>
<script>
import { throttle, debounce } from 'throttle-debounce';
import CodeMirror from 'codemirror/lib/codemirror'
import 'codemirror/mode/meta'
import 'codemirror/mode/python/python'
import 'codemirror/mode/javascript/javascript'
import 'codemirror/lib/codemirror.css'
import 'codemirror/theme/ayu-mirage.css'
import 'codemirror/keymap/sublime'

const CODE_PEEK_SIZE = 18
const DEFAULT_OPTIONS = {
    lineNumbers: true,
    lineSeparator: '\n',
    mode: undefined,
    theme: 'ayu-mirage',
    fontSize: 14,
    indentUnit: 4,
    tabSize: 4,
    indentWithTabs: false,
    lineWrapping: true,
    readOnly: false,
    smartIndent: false,
    matchBrackets: true,
    autoCloseBrackets: true,
    showTrailingSpace: true,
    keyMap: 'sublime',
    extraKeys: {
        Tab: editor => {
            if (editor.somethingSelected()) {
                editor.indentSelection('add')
            } else {
                editor.replaceSelection(
                    editor.getOption('indentWithTabs') ? '\t' : Array(editor.getOption('indentUnit') + 1).join(' '), 
                    'end', 
                    '+input'
                )
            }
        },
    },
    showInvisibles: true,
}

export default {
    name: 'exercise-single-editor',
    props: [
        'course',
        'material',
        'expMode',
    ],
    data() {
        return {
            filename: null,
            savedValue: '',
            value: '',
        }
    },
    created() {
        window.addEventListener('beforeunload', this.handleUnload);
        this.saveValueTh = throttle(1000, () => this.saveValue())
        this.updateSavedTh = throttle(1000, () => this.updateSaved())
        this.updateValueTh = throttle(1000, () => this.updateValue())
        this.addSnapTh = throttle(1000, () => this.addSnap())
    },
    mounted() {
        this.initEditor()
        this.loadValue()
    },
    beforeDestroy() {
        window.removeEventListener('beforeunload', this.handleUnload);
    },
    methods: {
        handleUnload() {
            if (this.savedValue !== this.value) {
                this.saveValue()
            }
            if (this.snaps.length > 0) {
                this.saveSnaps()
            }
        },
        initEditor() {
            const container = this.$refs.container
            this.editor = CodeMirror(container, DEFAULT_OPTIONS);
            this.editor.on('changes', (instance, changeObjs) => {
                const doc = this.editor.getDoc()
                this.value = doc.getValue()
                this.saveValueTh()
                this.updateValue()
                this.addSnapTh()
                this.$emit('edit')
            })
            this.editor.on('cursorActivity', instance => {
                this.addSnapTh()
            })
        },
        async loadValue() {
            this.filename = this.material.main_file
            this.setEditorMode()
            if (this.expMode.serverless) {
                const codeSaveKey = `code_${this.course.id}_${this.material.id}_${this.filename}`
                const loadedCode = localStorage.getItem(codeSaveKey)
                this.value = loadedCode || this.expMode.initCode || ''
            } else {
                const baseUrl = `/en/courses/${this.course.id}/materials/${this.material.id}`
                const response = await axios.get(`${baseUrl}/files/${this.filename}`)
                this.value = response.data
            }
            this.savedValue = this.value
            const doc = this.editor.getDoc()
            doc.setValue(this.value)
            doc.clearHistory()
        },
        getFileExtension() {
            if (this.filename && this.filename.includes('.')) {
                const tokens = this.filename.split('.')
                return tokens[tokens.length - 1]
            }
        },
        setEditorMode() {
            if (this.filename && this.editor) {
                const ext = this.getFileExtension()
                const mode = CodeMirror.findModeByExtension(ext)
                this.editor.setOption('mode', mode.mime || mode.mode)
            }
        },
        async saveValue() {
            const file = {
                path: this.filename,
                name: this.filename,
                type: 'text',
                is_text: true,
                value: this.value,
            }
            if (this.expMode.serverless) {
                const codeSaveKey = `code_${this.course.id}_${this.material.id}_${this.filename}`
                localStorage.setItem(codeSaveKey, this.value)
                this.savedValue = this.value
            } else {
                const baseUrl = `/en/courses/${this.course.id}/materials/${this.material.id}`
                const response = await axios.post(`${baseUrl}/files/${this.filename}`, { file })
                if (response.data.status === 200) {
                    this.savedValue = this.value
                }
            }
        },
        addSnap() {
            const selections = this.editor.listSelections()
            const line = selections[0].anchor.line
            const ch = selections[0].anchor.ch

            const doc = this.editor.getDoc()
            const lineCount = doc.lineCount()

            const lines = [];
            const halfPeekSize = Math.floor(CODE_PEEK_SIZE / 2)
            const maxLine = Math.min(lineCount, line + halfPeekSize);
            let i = Math.max(Math.min(line - halfPeekSize + 1, lineCount - CODE_PEEK_SIZE), 0);
            while((i < lineCount) && (lines.length < CODE_PEEK_SIZE)) {
                lines.push(doc.getLine(i));
                i++;
            }

            const snap = {
                type: 'edit',
                filename: this.filename,
                value: lines.join('\n'),
                line,
                ch,
                ts: Date.now(),
            }            
            this.$emit('snap', snap)
        },
        updateValue() {
            this.$emit('set-value', this.value)
        },
        updateSaved() {
            const saved = this.savedValue === this.value
            this.$emit('set-saved', saved)
        }
    },
    watch: {
        file() {
            this.loadValue()
        },
        value() {
            this.updateSavedTh()
        },
        savedValue() {
            this.updateSavedTh()
        },
    },
}
</script>
<style scoped>
    .editor-container {
        width: 100%;
        height: 100%;
    }

    .editor-container /deep/ .CodeMirror {
        width: 100%;
        height: 100%;
    }
</style>
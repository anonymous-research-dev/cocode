<template>
    <div class="code-block u-v-small-padded">
        <runner
            ref="runner"
            :mode="runnerMode"
            :value="value"
        ></runner>
        <div v-if="interactive" class="block-toolbar buttons has-addons has-background-light">
            <button class="button is-success is-small u-sharp" @click="run">
                <span class="icon is-small">
                    <i class="fa fa-play"></i>
                </span>
                <span>{{ gettext('실행') }}</span>
            </button>
            <button 
                class="button is-danger is-small u-sharp" 
                @click="reset"
                :disabled="content === value"
            >
                <span class="icon is-small">
                    <i class="fa fa-history"></i>
                </span>
                <span>{{ gettext('코드 초기화') }}</span>
            </button>
        </div>
        <div class="block-editor-container" ref="container"></div>
    </div>
</template>
<script>
import CodeMirror from 'codemirror/lib/codemirror'
import 'codemirror/mode/meta'
import 'codemirror/mode/python/python'
import 'codemirror/lib/codemirror.css'
import 'codemirror/theme/ayu-mirage.css'
import 'codemirror/keymap/sublime'
import Runner from '../runner/runner'

const DEFAULT_OPTIONS = {
  lineNumbers: false,
  lineSeparator: '\n',
  mode: undefined,
  theme: 'ayu-mirage',
  fontSize: 14,
  indentUnit: 4,
  tabSize: 4,
  indentWithTabs: false,
  lineWrapping: true,
  readOnly: false,
  smartIndent: true,
  matchBrackets: true,
  autoCloseBrackets: true,
  showTrailingSpace: true,
  keyMap: 'sublime',
  extraKeys: null,
  showInvisibles: true,
  viewportMargin: Infinity,
}

const RUNNER_MAP = {
    python: 'python3',
}

export default {
    name: 'code-block',
    props: [
        'lang',
        'content',
        'interactive',
    ],
    data() {
        return {
            gettext,
            value: '',
        }
    },
    components: {
        Runner,
    },
    created() {

    },
    mounted() {
        this.initEditor()
    },
    methods: {
        initEditor() {
            const container = this.$refs.container
            this.editor = CodeMirror(container, {
                ...DEFAULT_OPTIONS,
                mode: this.lang,
                readOnly: !this.interactive,
            });
            this.value = this.content
            this.editor.on('changes', (instance, changeObjs) => {
                const doc = this.editor.getDoc()
                this.value = doc.getValue()
            });
            this.$nextTick(() => {
                const doc = this.editor.getDoc()
                doc.setValue(this.content)
            })
        },
        run() {
            this.$refs.runner.run()
        },
        reset() {
            const doc = this.editor.getDoc()
            doc.setValue(this.content)
            this.value = this.content
        },
    },
    computed: {
        runnerMode() {
            return RUNNER_MAP[this.lang] || this.lang
        }
    }
}
</script>
<style scoped>
    .code-block /deep/ .CodeMirror {
        height: auto;
    }
    .block-toolbar {
        margin: 0;
        width: 100%;
    }
    .block-toolbar .button {
        margin: 0;
    }
</style>
<template>
    <runner-modal @close="close" v-if="running" :title="gettext('실행')" :wide="true">
        <div class="runner u-flex-h-container">
            <div class="u-flex-fill-item console-column">
                <div class="u-fill is-size-7">
                    <console-box :outputs="outputs"></console-box>
                </div>
            </div>
            <div class="u-flex-item" :class="{'u-no-display': !drawing}">
                <div class="draw-box-container">
                    <draw-box ref="drawBox"></draw-box>
                </div>
            </div>
        </div>
    </runner-modal>
</template>
<script>
import ConsoleBox from '../common/console-box'
import DrawBox from '../common/draw-box'
import RunnerModal from './runner-modal'
import { createRunner } from '../../utils/runner'
export default {
    name: 'runner',
    props: [
        'course',
        'material',
        'mode',
        'expMode',
        'value',
    ],
    components: {
        ConsoleBox,
        DrawBox,
        RunnerModal,
    },
    data() {
        return {
            gettext,
            outputs: [],
            drawing: false,
            running: false,
        }
    },
    methods: {
        async run() {
            this.outputs = []
            this.drawing = false
            this.running = true

            let params = {}
            if (this.expMode.serverless) {
                params = {
                    mode: this.material.runner,
                    value: this.value,
                    isGrade: false,
                }
            } else {
                if (this.course && this.material) {
                    params = {
                        mode: this.material.runner,
                        mainFile: this.material.main_file,
                        cwdUrl: `/en/courses/${this.course.id}/materials/${this.material.id}/files`,
                        isGrade: false,
                    }
                } else if (this.mode && this.value) {
                    params = {
                        mode: this.mode,
                        value: this.value,
                        isGrade: false,
                    }
                } else {
                    throw Exception('Either provide mode & value or course & material to the runner component.')
                }
            }

            const startTimestamp = Date.now()
            const runner = createRunner(params)
            await runner.init()

            this.addSnap('output-init')
            runner.on('stdout', e => {
                this.outputs.push({
                    type: 'out',
                    value: e.detail.value
                })
                this.addSnap('stdout', e.detail.value)
            })
            runner.on('stderr', e => {
                this.outputs.push({
                    type: 'err',
                    value: e.detail.value
                })
                this.addSnap('stderr', e.detail.value)
            })
            runner.on('robot-init', e => {
                this.drawing = true
                this.$nextTick(() => {
                    this.$refs.drawBox.initRobot()
                })
                this.addSnap('robot-init')
            })
            runner.on('robot-draw', e => {
                this.$refs.drawBox.addRobotTask(e.detail.value)
                this.addSnap('robot-draw', e.detail.value)
            })
            const code = await runner.run()

            const log = {
                type: 'run',
                duration: Date.now() - startTimestamp,
                source: this.value,
                outputs: this.outputs,
                code: code,
            }
            this.$emit('log', log)
        },
        addSnap(eventType, value) {
            const snap = {
                type: 'run',
                event: eventType,
                value: value,
                ts: Date.now(),
            }
            this.$emit('snap', snap)
        },
        close() {
            this.running = false
        },
    }
}
</script>
<style scoped>
    .draw-box-container {
        width: 320px;
        height: 320px;
    }
    .console-column {
        max-width: 100%;
    }
</style>
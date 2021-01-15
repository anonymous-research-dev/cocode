<template>
    <exercise-runner-modal @close="close" v-if="visible" :title="gettext('채점')">
        <div class="exercise-grader u-flex-v-container u-fill">
            <div class="u-flex-item u-padded has-background-white has-text-black">
                <div class="has-text-centered is-size-4">
                    <span v-if="grading">
                        {{ gettext('채점 중...') }}
                    </span>
                    <span v-else-if="progress >= 100">
                        {{ gettext('성공!') }}
                    </span>
                    <span v-else>
                        {{ gettext('다시 시도해보세요.') }}
                    </span>
                </div>
                <div class="stars-row u-v-padded is-size-1 has-text-warning has-text-centered">
                    <span class="u-h-padded" v-for="n in 3" :key="n">
                        <i v-if="n <= star" class="fa fa-star"></i>
                        <i v-else class="fa fa-star-o"></i>
                    </span>
                </div>
                <div class="progress-row">
                    <progress 
                        v-if="!grading"
                        class="progress is-info" 
                        :value="progress" 
                        max="100"
                    >
                        {{ progress }}%
                    </progress>
                    <progress v-else class="progress is-info" max="100"></progress>
                </div>
            </div>
            <div class="u-flex-fill-item console-row">
                <div class="u-fill is-size-7">
                    <console-box :outputs="outputs"></console-box>
                </div>
            </div>
        </div>
    </exercise-runner-modal>
</template>
<script>
import ExerciseRunnerModal from './exercise-runner-modal'
import ConsoleBox from '../common/console-box'
import { createRunner } from '../../utils/runner'
export default {
    name: 'exercise-grader',
    props: [
        'course',
        'material',
        'value',
        'expMode',
    ],
    components: {
        ExerciseRunnerModal,
        ConsoleBox,
    },
    data() {
        return {
            gettext,
            outputs: [],
            grading: false,
            visible: false,
            star: 0,
            progress: 0,
        }
    },
    methods: {
        async grade() {
            this.outputs = []
            this.grading = true
            this.visible = true

            const baseUrl = `/en/courses/${this.course.id}/materials/${this.material.id}`
            let params;

            if (this.expMode.serverless) {
                params = {
                    mode: this.material.runner,
                    cwdUrl: `${baseUrl}/files`,
                    value: `__code__ = '''${this.value}'''\n${this.expMode.grader}`,
                }
            } else {
                params = {
                    mode: this.material.runner,
                    mainFile: this.material.main_file,
                    cwdUrl: `${baseUrl}/files`,
                    isGrade: true,
                }
            }

            const startTimestamp = Date.now()
            const runner = createRunner(params)
            await runner.init()

            const result = {
                star: 0,
                progress: 0,
            }
            this.addSnap('output-init')
            
            // Do not listen to the standard output.

            runner.on('stderr', e => {
                this.outputs.push({
                    type: 'err',
                    value: e.detail.value
                })
                this.addSnap('stderr', e.detail.value)
            })
            runner.on('grade-out', e => {
                this.outputs.push({
                    type: 'grade',
                    value: e.detail.value
                })
                this.addSnap('grade-out', e.detail.value)
            })
            runner.on('grade-progress', e => {
                result.progress = parseInt(e.detail.value)
            })
            runner.on('grade-star', e => {
                result.star = parseInt(e.detail.value)
            })
            const code = await runner.run()

            this.star = result.star
            this.progress = result.progress
            this.grading = false

            this.addSnap('grade-result', result)

            const log = {
                type: 'grade',
                duration: Date.now() - startTimestamp,
                outputs: this.outputs,
                code: code,
                star: this.star,
                progress: this.progress,
            }
            this.$emit('log', log)
            
            if (!expMode.serverless) {
                const response = await axios.post(`${baseUrl}/state/`, result)
                if (response.data.status === 200) {
                    window.dispatchEvent(new CustomEvent('cocode-material-state-update'));
                    if (result.progress >= 100) {
                        this.$emit('pass')   
                    }
                } else {
                    console.error('Failed to update the material state.')
                }
            }
        },
        addSnap(eventType, value) {
            const snap = {
                type: 'grade',
                event: eventType,
                value: value,
                ts: Date.now(),
            }
            this.$emit('snap', snap)
        },
        close() {
            this.visible = false
        },
    }
}
</script>
<style scoped>
    .exercise-runner {
        
    }
    .stars-row {
        min-height: 5rem;
    }
</style>
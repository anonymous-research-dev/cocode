<template>
    <div class="exercise u-fill">
        <exercise-runner 
            ref="runner" 
            :course="course"
            :material="material"
            :expMode="expMode"
            :value="value"
            @snap="snap => addSnap(snap)"
            @log="log => addLog(log)"
        ></exercise-runner>
        <exercise-grader 
            ref="grader" 
            :course="course"
            :material="material"
            :expMode="expMode"
            :value="value"
            @snap="snap => addSnap(snap)"
            @log="log => addLog(log)"
            @pass="allowNextMaterial"
        ></exercise-grader>
        <div class="u-flex-h-container">
            <div class="u-flex-item readme-column">
                <div class="u-fill u-scrollable">
                    <div class="u-padded">
                        <markdown-content 
                            :content="content"
                            :course="course"
                            :material="material"
                        ></markdown-content>
                    </div>
                </div>
            </div>
            <div class="u-flex-fill-item main-column">
                <div class="u-fill u-flex-v-container">
                    <div class="toolbar-row u-flex-item">
                        <div class="buttons has-addons">
                            <button 
                                class="button is-white u-sharp" 
                                :disabled="saved"
                                @click="saveValue"
                            >
                                <span class="icon">
                                    <i class="fa fa-cloud"></i>
                                </span>
                                <span>{{ gettext('저장') }}</span>
                            </button>
                            <button 
                                class="button is-white u-sharp"
                                @click="run"
                            >
                                <span class="icon">
                                    <i class="fa fa-play"></i>
                                </span>
                                <span>{{ gettext('실행') }}</span>
                            </button>
                            <button 
                                v-if="material.gradable"
                                class="button is-light u-sharp"
                                @click="grade"
                            >
                                <span class="icon">
                                    <i class="fa fa-check"></i>
                                </span>
                                <span>{{ gettext('제출') }}</span>
                            </button>
                            <a 
                                class="button is-success u-sharp" 
                                v-if="nextMaterial"
                                :disabled="!nextMaterialAccessible"
                                :href="nextMaterialAccessible ? `/courses/${course.id}/materials/${nextMaterial.id}` : undefined"
                            >
                                <span class="icon">
                                    <i class="fa fa-arrow-right"></i>
                                </span>
                                <span>{{ gettext('다음') }}</span>
                            </a>
                        </div>
                        <div class="buttons has-addons">
                            <button 
                                v-if="(expMode.snaps === undefined) && showSnaps"
                                class="button is-danger u-sharp" 
                                @click="() => setShowSnaps(false)"
                            >
                                <span class="icon">
                                    <i class="fa fa-eye"></i>
                                </span>
                                <span>{{ gettext('동료 화면 끄기') }}</span>
                            </button>
                            <button 
                                v-if="(expMode.snaps === undefined) && !showSnaps"
                                class="button is-info u-sharp" 
                                @click="() => setShowSnaps(true)"
                            >
                                <span class="icon">
                                    <i class="fa fa-eye"></i>
                                </span>
                                <span>{{ gettext('동료 화면 켜기') }}</span>
                            </button>
                            <button 
                                v-if="!expMode.serverless"
                                class="button is-danger u-sharp" 
                                @click="reset"
                            >
                                <span class="icon">
                                    <i class="fa fa-refresh"></i>
                                </span>
                                <span>{{ gettext('코드 리셋') }}</span>
                            </button>
                        </div>
                    </div> 
                    <div class="editor-row u-flex-fill-item">
                        <template v-if="material.editor === 'single'">
                            <exercise-single-editor
                                ref="editor"
                                :course="course"
                                :material="material"
                                :expMode="expMode"
                                @set-saved="saved => setSaved(saved)"
                                @set-value="value => setValue(value)"
                                @snap="snap => addSnap(snap)"
                                @edit="() => handleCodeEdit()"
                            ></exercise-single-editor>
                        </template>
                    </div>
                </div>
            </div>
            <div 
                v-if="!expired" 
                class="u-flex-item snaps-column is-hidden-touch"
                :class="{'hidden-column': hideSnaps}"
            >
                <div class="u-fill">
                    <exercise-snaps
                        ref="snaps"
                        :course="course"
                        :material="material"
                        :show-usernames="expMode.anonymizeSnaps !== true"
                        :show-messages="!expMode.hideSnapMessages && hideSnaps"
                        :user-snaps="expMode.userSnaps"
                        @log="log => addLog(log)"
                    ></exercise-snaps>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { throttle, debounce } from 'throttle-debounce';
import MarkdownContent from './common/markdown-content'
import ExerciseRunner from './exercise/exercise-runner'
import ExerciseGrader from './exercise/exercise-grader'
import ExerciseSingleEditor from './exercise/exercise-single-editor'
import ExerciseSnaps from './exercise/exercise-snaps'
export default {
    name: 'exercise',
    props: [
        'course',
        'material',
        'nextMaterial',
        'materialAccessibleMap',
        'expMode',
        'content',
    ],
    components: {
        MarkdownContent,
        ExerciseRunner,
        ExerciseGrader,
        ExerciseSingleEditor,
        ExerciseSnaps,
    },
    data() {
        return {
            gettext,
            saved: true,
            value: '',
            snaps: [],
            logs: [],
            startTimestamp: null,
            editSeconds: -1,
            openSeconds: -1,
            updateOpenSecondsInterval: null,
            updateSecondsInterval: null,
            nextMaterialAccessible: false,
            expired: false,
            showSnaps: false,
        }
    },
    created() {
        window.addEventListener('beforeunload', this.handleUnload);
        window.addEventListener('focus', this.handleFocus);
        window.addEventListener('blur', this.handleBlur);
        this.saveSnapsTh = throttle(5000, () => this.saveSnaps())
        this.saveLogsTh = throttle(30000, () => this.saveLogs())
        this.incEditSecondsTh = throttle(1000, () => this.incEditSeconds()) 
        this.touch = debounce(20 * 60 * 1000, () => this.expire()) // Expire the client after 20 minutes of not using.
        this.touch()
        this.initRecordSeconds()
        if (this.nextMaterial && this.materialAccessibleMap[this.nextMaterial.id]) {
            this.nextMaterialAccessible = true
        }
    },
    mounted() {
        this.showDialogs()
    },
    beforeDestroy() {
        this.handleUnload()
        this.saveSnapsTh.cancel()
        this.saveLogsTh.cancel()
        window.removeEventListener('beforeunload', this.handleUnload);
        window.removeEventListener('focus', this.handleFocus);
        window.removeEventListener('blur', this.handleBlur);
    },
    methods: {
        async showDialogs() {
            if (this.expMode.message) {
                await showDialog(this.expMode.message, { mode: 'ok' })
            }
            if (this.expMode.ask_snaps) {
                await this.askSnapShow()
            }
        },
        handleUnload() {
            this.addSnap({
                type: 'browser',
                event: 'unload',
                value: null,
                ts: Date.now(),
            })
            this.saveValue()
            this.saveSnaps()
            this.saveLogs()
            this.saveSeconds()
        },
        handleFocus() {
            this.addSnap({
                type: 'browser',
                event: 'focus',
                value: null,
                ts: Date.now(),
            })
            if (this.startTimestamp && !this.updateOpenSecondsInterval) {
                this.updateOpenSecondsInterval = setInterval(() => {
                    this.updateOpenSeconds()
                }, 1000)
            }
        },
        handleBlur() {
            this.addSnap({
                type: 'browser',
                event: 'blur',
                value: null,
                ts: Date.now(),
            })
            if (this.updateOpenSecondsInterval) {
                clearInterval(this.updateOpenSecondsInterval)
                this.updateOpenSecondsInterval = null
            }
        },
        async askSnapShow() {
            const message = this.gettext('이번 문제를 푸는 동안에 화면 오른쪽에 다른 학생들이 문제 푸는 모습이 보이도록 할까요?')
            const answer = await showDialog(gettext(message), { mode: 'yesNo' })
            const log = {
                type: 'snap_answer',
                answer: answer === 'yes', 
            }
            this.addLog(log)
            this.setShowSnaps(answer === 'yes')            
        },
        setShowSnaps(showSnaps) {
            this.showSnaps = showSnaps
            const log = {
                type: 'set_show_snaps',
                value: showSnaps, 
            }
            this.addLog(log)
        },
        setSaved(saved) {
            this.saved = saved
        },
        setValue(value) {
            this.value = value
        },
        async saveValue() {
            return await this.$refs.editor.saveValue()
        },
        run() {
            this.$refs.runner.run()
        },
        grade() {
            this.$refs.grader.grade()
        },
        async reset() {
            const answer = await showDialog(gettext('코드를 리셋할까요? 수정하신 부분이 모두 사라집니다.'), { mode: 'okCancel' })
            if (answer === 'ok') {
                const baseUrl = `/en/courses/${this.course.id}/materials/${this.material.id}`
                const response = await axios.post(`${baseUrl}/reset/`)
                if (response.data.status === 200) {
                    this.$refs.editor.loadValue()
                } else {
                    console.error('Failed to reset the code.')
                }
            }
        },
        async expire() {
            try {
                this.expired = true
                await this.saveValue()
                await this.saveSeconds()
                if (this.updateOpenSecondsInterval) {
                    clearInterval(this.updateOpenSecondsInterval)
                }
                if (this.updateSecondsInterval) {
                    clearInterval(this.updateSecondsInterval)
                }
                const answer = await showDialog(gettext('일정 시간동안 사용하지 않아서 접속이 종료되었습니다. 확인 버튼을 누르시면 서버와 다시 연결됩니다.'), { mode: 'ok' })
                window.location = window.location.href
            } catch (err) {
                console.error('Failed to expire safely.')
            }
        },
        addSnap(snap) {
            this.touch()
            this.snaps.push(snap)
            this.saveSnapsTh()
        },
        async saveSnaps() {
            if (this.expMode.serverless) {
                return
            }
            const baseUrl = `/en/courses/${this.course.id}/materials/${this.material.id}`
            const snaps = this.snaps
            if (snaps.length === 0) {
                return
            }
            this.snaps = []
            try {
                const response = await axios.post(`${baseUrl}/snaps/`, { snaps })
                if (response.data.status === 200) {
                    // Do nothing.
                } else {
                    // Restore the snaps
                    this.snaps = snaps + this.snaps
                }
            } catch (err) {
                // Restore the snaps
                this.snaps = snaps + this.snaps
            }
        },
        incEditSeconds() {
            if (this.editSeconds >= 0) {
                this.editSeconds += 1
            }
        },
        handleCodeEdit() {
            this.incEditSecondsTh()
        },
        async initRecordSeconds() {
            try {
                await this.loadSeconds()
                this.startRecordSeconds()
            } catch (err) {
                console.error(err)
            }
        },
        async loadSeconds() {
            if (this.expMode.serverless) {
                this.editSeconds = 0
                this.openSeconds = 0
                return
            }
            const baseUrl = `/en/courses/${this.course.id}/materials/${this.material.id}`
            const response = await axios.get(`${baseUrl}/seconds`)
            this.editSeconds = response.data.data.edit_seconds
            this.openSeconds = response.data.data.open_seconds
        },
        startRecordSeconds() {
            this.startTimestamp = Date.now()
            this.updateOpenSecondsInterval = setInterval(() => {
                this.updateOpenSeconds()
            }, 1000)
            this.updateSecondsInterval = setInterval(() => {
                this.saveSeconds()
            }, 30000)
        },
        updateOpenSeconds() {
            const now = Date.now()
            this.openSeconds += parseInt((now - this.startTimestamp) / 1000)
            this.startTimestamp = now
        },
        async saveSeconds() {
            if (this.expMode.serverless) {
                return
            }
            const baseUrl = `/en/courses/${this.course.id}/materials/${this.material.id}`
            const data = {
                open_seconds: this.openSeconds,
                edit_seconds: this.editSeconds,
            }
            const response = await axios.post(`${baseUrl}/seconds/`, data)
        },
        addLog(log) {
            if (this.expMode.serverless) {
                return
            }
            this.logs.push({
                ...log,
                edit_seconds: this.editSeconds,
                open_seconds: this.openSeconds,
                ts: Date.now(),
            })
            this.saveLogsTh()
        },
        async saveLogs() {
            if (this.expMode.serverless) {
                return
            }
            const baseUrl = `/en/courses/${this.course.id}/materials/${this.material.id}`
            const logs = this.logs
            if (logs.length === 0) {
                return
            }
            this.logs = []
            try {
                const response = await axios.post(`${baseUrl}/logs/`, { logs })
                if (response.data.status === 200) {
                    // Do nothing.
                } else {
                    // Restore the logs
                    this.logs = logs + this.logs
                } 
            } catch (err) {
                // Restore the logs
                this.logs = logs + this.logs
            }
        },
        allowNextMaterial() {
            if (this.nextMaterial) {
                this.nextMaterialAccessible = true
            }
        }
    },
    computed: {
        hideSnaps() {
            return !this.expMode.snaps && !this.showSnaps
        }
    },
}
</script>
<style scoped>
    .exercise {

    }
    .readme-column {
        min-width: 25rem;
        width: 32%;
        max-width: 45%;
    }
    .main-column {
        width: 100%
    }
    .snaps-column {
        width: 10rem;
    }
    .hidden-column {
        width: 0;
    }
    .toolbar-row {
        display: flex;
        flex-flow: row nowrap;
        justify-content: space-between;
    }
    .toolbar-row .buttons {
        padding: 0;
        margin: 0;
    }
    .toolbar-row .buttons .button {
        margin: 0;
    }
    .editor-row {

    }
</style>
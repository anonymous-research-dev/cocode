<template>
    <div class="exercise-snaps u-fill u-scrollable">
        <div 
            v-if="showMessages" 
            class="snap-message"
        >
            <i v-if="lastMessage" class="fa fa-commenting"></i> {{ lastMessage }}
        </div>
        <div 
            class="focus-user-snap" 
            v-for="username in usernames" 
            :key="`focus-user-snap-${username}`"
            :class="{ active: focusedUsername === username }"
        >
            <div class="focus-user-snap-box">
                <div 
                    class="focus-user-snap-code u-fill" 
                    :class="{ 'u-no-display': userStates[username] !== 'edit' }"
                    v-if="userEditors[username]"
                >
                    <pre><code 
                        class="hljs" 
                        v-html="userEditors[username].highlighted"
                    ></code></pre>
                </div>
                <div 
                    class="focus-user-snap-draw u-fill" 
                    :class="{ 'u-no-display': userStates[username] !== 'draw' }"
                >
                    <draw-box :ref="`focusDrawBox${username}`"></draw-box>
                </div>
                <div 
                    class="focus-user-snap-outputs u-fill" 
                    :class="{ 'u-no-display': userStates[username] !== 'output' && userStates[username] !== 'grade' }"
                >
                    <console-box :outputs="userOutputs[username] || []" :no-padding="true"></console-box>
                </div>
            </div>
            <div class="focus-user-text" :class="{ 'grade': userStates[username] === 'grade' }">
                <span v-if="userTexts[username]">{{ userTexts[username] }}</span>
            </div>
            <div class="focus-user-label" v-if="username">
                <template v-if="!showUsernames || username.startsWith('exp__')">
                    {{ gettext('익명') }} ({{ usernames.indexOf(username) + 1 }})
                </template>
                <template v-else>
                    {{ username }}
                </template>
            </div>
        </div>
        <div 
            class="user-snap" 
            v-for="username in usernames" 
            :key="`user-snap-${username}`"
            @mouseover="() => focusSnap(username)"
            @mouseleave="() => unfocusSnap()"
        >
            <div class="user-snap-box">
                <div 
                    class="user-snap-code u-fill" 
                    :class="{ 'u-no-display': userStates[username] !== 'edit' }"
                    v-if="userEditors[username]"
                >
                    <pre><code 
                        class="hljs" 
                        v-html="userEditors[username].blockified"
                    ></code></pre>
                </div>
                <div 
                    class="user-snap-draw u-fill" 
                    :class="{ 'u-no-display': userStates[username] !== 'draw' }"
                >
                    <draw-box :ref="`drawBox${username}`"></draw-box>
                </div>
                <div 
                    class="user-snap-outputs u-fill" 
                    :class="{ 'u-no-display': userStates[username] !== 'output' && userStates[username] !== 'grade' }"
                >
                    <console-box :outputs="userOutputs[username] || []" :no-padding="true"></console-box>
                </div>
            </div>
            <div class="user-text" :class="{ 'grade': userStates[username] === 'grade' }">
                <span v-if="userTexts[username]">{{ userTexts[username] }}</span>
            </div>
            <div class="user-label">
                <template v-if="!showUsernames || username.startsWith('exp__')">
                    {{ gettext('익명') }} ({{ usernames.indexOf(username) + 1 }})
                </template>
                <template v-else>
                    {{ username }}
                </template>
            </div>
        </div>
    </div>
</template>
<script>
import highlight, { blockify } from '../../utils/highlight';
import ConsoleBox from '../common/console-box'
import DrawBox from '../common/draw-box'
const EXT_LANG_MAP = {
    py: 'python',
}
const SNAP_RELOAD_COOLTIME = 15000
const MAX_SNAP_SLEEP = 15000
const TEST_SNAPS = require('./test-snaps.json') // TEST SNAPS loading code.

export default {
    name: 'exercise-snaps',
    props: [
        'course',
        'material',
        'showUsernames',
        'showMessages',
        'userSnaps',
    ],
    components: {
        ConsoleBox,
        DrawBox,
    },
    data() {
        return {
            gettext,
            userSnapsMap: null,
            userSnapTimestampDeltaMap: {},
            usernames: [],
            userEditors: {},
            userStates: {},
            userTexts: {},
            userTextTimestamps: {},
            userOutputs: {},
            actions: [],
            lastMessageTimeStamp: 0,
            lastMessage: '',
            focusedUsername: null,
            focusTimestamp: null,
            focusUsernames: [],
            focusState: null,
            focusEditor: null,
            stopped: false,
        }
    },
    created() {
        this.loadSnaps()
        this.messageInterval = setInterval(() => this.createSnapMessage(), 1000);
    },
    beforeDestroy() {
        this.stopped = true
    },
    methods: {
        async loadSnaps() {
            if (this.userSnaps) {
                this.userSnapsMap = this.userSnaps
                this.playSnaps()
            } else {
                const baseUrl = `/en/courses/${this.course.id}/materials/${this.material.id}`
                const response = await axios.get(`${baseUrl}/snaps/`)
                if (response.data.status === 200) {
                    this.userSnapsMap = response.data.data.user_snaps_dict
                    this.playSnaps()
                }
            }
        },
        playSnaps() {
            const usernames = Object.keys(this.userSnapsMap)
            for (const username of usernames) {
                const snaps = this.userSnapsMap[username]
                if (snaps.length === 0) {
                    continue
                }
                this.userSnapTimestampDeltaMap[username] = Date.now() - snaps[0].ts
                this.playSnap(username, 0)
            }
        },
        playSnap(username, cursor) {
            if (this.stopped) {
                return
            }
            const snaps = this.userSnapsMap[username]
            const now = Date.now()
            const delta = this.userSnapTimestampDeltaMap[username]
            const isNextSnap = cursor < snaps.length - 1
            this.handleSnap(username, snaps[cursor])

            if (isNextSnap) {
                const waitDuration = snaps[cursor + 1].ts + delta - now
                if (waitDuration > MAX_SNAP_SLEEP) {
                    this.userSnapTimestampDeltaMap[username] = now - (snaps[cursor + 1].ts - MAX_SNAP_SLEEP)
                    setTimeout(() => this.playSnap(username, cursor + 1), MAX_SNAP_SLEEP)
                } else if (waitDuration > 0) {
                    setTimeout(() => this.playSnap(username, cursor + 1), waitDuration)
                } else {
                    this.playSnap(username, cursor + 1)
                }
            } else {
                this.userSnapTimestampDeltaMap[username] = now - (snaps[0].ts - SNAP_RELOAD_COOLTIME)
                setTimeout(() => this.playSnap(username, 0), SNAP_RELOAD_COOLTIME)
            }
        },
        setUserText(username, text, duration) {
            const now = Date.now()
            Vue.set(this.userTexts, username, text)
            Vue.set(this.userTextTimestamps, username, now)
            if (duration) {
                setTimeout(() => {
                    if (this.userTextTimestamps[username] === now) {
                        Vue.set(this.userTexts, username, null)
                        Vue.set(this.userTextTimestamps, username, Date.now())
                    }
                }, duration)
            }
        },
        handleSnap(username, snap) {
            if (!this.usernames.includes(username)) {
                this.usernames.push(username)
            }
            // Backward compatibility.
            if (snap.type === undefined) {
                snap.type = 'edit'
            }

            if (snap.type === 'edit') {
                const splitFilename = snap.filename.split('.')
                const ext = splitFilename[splitFilename.length - 1]
                const lang = EXT_LANG_MAP[ext]
                Vue.set(this.userEditors, username, {
                    highlighted: highlight(snap.value, lang),
                    blockified: blockify(snap.value, lang),
                    ...snap,
                })
                Vue.set(this.userStates, username, 'edit')
                this.setUserText(username, gettext('수정 중...'), 1500)
                // Users edit code too much.
                this.actions.push({
                    username,
                    action: 'edit',
                    ts: Date.now(),
                })
            } else if (snap.type === 'run') {
                if (snap.event === 'robot-init') {
                    Vue.set(this.userStates, username, 'draw')
                    this.$refs[`drawBox${username}`][0].initRobot()
                    this.$refs[`focusDrawBox${username}`][0].initRobot()
                    this.actions.push({
                        username,
                        action: 'robot',
                        ts: Date.now(),
                    })
                } else if (snap.event === 'robot-draw') {
                    if (this.userStates[username] !== 'draw') {
                        Vue.set(this.userStates, username, 'draw')
                    }
                    this.$refs[`drawBox${username}`][0].addRobotTask(snap.value)
                    this.$refs[`focusDrawBox${username}`][0].addRobotTask(snap.value)
                } else if (snap.event === 'output-init') {
                    if (this.userStates[username] !== 'draw') {
                        Vue.set(this.userStates, username, 'draw')
                    }
                    Vue.set(this.userOutputs, username, [])
                } else if (snap.event === 'stdout' || snap.event === 'stderr') {
                    if (this.userStates[username] !== 'output') {
                        Vue.set(this.userStates, username, 'output')
                    }
                    const outputType = {
                        stdout: 'out',
                        stderr: 'err',
                    }[snap.event]
                    Vue.set(this.userOutputs, username, [
                        ...(this.userOutputs[username] || []),
                        { type: outputType, value: snap.value },
                    ])
                    this.actions.push({
                        username,
                        action: outputType,
                        ts: Date.now(),
                    })
                }
                this.setUserText(username, gettext('실행 중...'))
            } else if (snap.type === 'grade') {
                if (snap.event === 'output-init') {
                    if (this.userStates[username] !== 'grade') {
                        Vue.set(this.userStates, username, 'grade')
                    }
                    Vue.set(this.userOutputs, username, [])
                    this.setUserText(username, gettext('채점 중...'))
                    this.actions.push({
                        username,
                        action: 'grade',
                        ts: Date.now(),
                    })
                } else if (snap.event === 'stderr' || snap.event === 'grade-out') {
                    if (this.userStates[username] !== 'grade') {
                        Vue.set(this.userStates, username, 'grade')
                    }
                    const outputType = {
                        'stderr': 'err',
                        'grade-out': 'grade',
                    }[snap.event]
                    Vue.set(this.userOutputs, username, [
                        ...(this.userOutputs[username] || []),
                        { type: outputType, value: snap.value },
                    ])
                    this.actions.push({
                        username,
                        action: outputType,
                        ts: Date.now(),
                    })
                } else if (snap.event === 'grade-result') {
                    const passed = snap.value.progress >= 100
                    const message = passed ? gettext('채점 완료: 통과') : gettext('채점 완료: 통과 실패')
                    const stars = []
                    for (let i = 0; i < 3; i++) {
                        stars.push(i < snap.value.star ? '★' : '☆')
                    }
                    const starText = passed ? ` (${stars.join('')})` : ''
                    // this.setUserText(username, `${message}${starText}`, 3000)
                    this.setUserText(username, `${message}`, 3000)
                    this.actions.push({
                        username,
                        action: `grade-${passed ? 'pass' : 'fail'}`,
                        ts: Date.now(),
                    })
                }
            }
        },
        focusSnap(username) {
            this.focusTimestamp = Date.now()
            this.focusUsernames = this.usernames.slice(0)
            this.focusedUsername = username
            this.focusState = this.userStates[username]
            this.focusEditor = this.userEditors[username]
        },
        unfocusSnap() {
            const log = {
                type: 'snap_focus',
                duration: Date.now() - this.focusTimestamp,
                username: this.focusedUsername,
                usernames: this.focusUsernames,
                state: this.focusState,
                editor: this.focusEditor,
            }
            this.focusedUsername = null
            this.$emit('log', log)
        },
        createSnapMessage() {
            const interval = 5000
            const now = Date.now()
            if ((now - this.lastMessageTimeStamp) < interval) {
                return this.lastMessage
            }
            this.lastMessageTimeStamp = now
            const actionUsernames = {}
            while (this.actions.length > 0) {
                const action = this.actions.pop()
                let username = `${gettext('익명')} (${this.usernames.indexOf(action.username) + 1})`
                if (this.showUsernames && !action.username.startsWith('exp__')) {
                    username = action.username
                }
                if (!actionUsernames[action.action]) {
                    actionUsernames[action.action] = [username]
                } else if (!actionUsernames[action.action].includes(username)) {
                    actionUsernames[action.action].push(username)
                }
            }
            
            const messages = []
            const actionKeys = Object.keys(actionUsernames)
            for (const actionKey of actionKeys) {
                const count = actionUsernames[actionKey].length
                let countText = `${count}${gettext('명이')}`
                if (count === 1) {
                    countText = `${actionUsernames[actionKey][0]}이(가)`
                }
                switch (actionKey) {
                    case 'edit':
                        messages.push(`${countText} ${gettext('코드 수정')}`)
                        break
                    case 'robot':
                        messages.push(`${countText} ${gettext('로봇 코드 실행')}`)
                        break
                    case 'out':
                        messages.push(`${countText} ${gettext('코드 실행')}`)
                        break
                    case 'err':
                        messages.push(`${countText} ${gettext('에러 확인')}`)
                        break
                    case 'grade':
                        messages.push(`${countText} ${gettext('채점 결과 확인')}`)
                        break
                    // case 'grade-pass':
                    //     messages.push(`${countText} ${gettext('채점 결과 확인')}`)
                    //     break
                    // case 'grade-fail':
                    //     messages.push(`${countText} ${gettext('채점에서 발견된 문제 확인')}`)
                    //     break
                    default:
                        break
                }
            }

            if (messages.length === 0) {
                return ''
            }

            const message = `${messages.join(', ')} ${gettext('중입니다.')}`

            this.lastMessageTimeStamp = now
            this.lastMessage = message
            return message
        },
    },
    computed: {
        // snapMessage() {
        //     const interval = 5000
        //     const now = Date.now()
        //     if ((now - this.lastMessageTimeStamp) < interval) {
        //         return this.lastMessage
        //     }
        //     this.lastMessageTimeStamp = now
        //     const actionUsernames = {}
        //     while (this.actions.length > 0) {
        //         const action = this.actions.pop()
        //         let username = `${gettext('익명')} (${this.usernames.indexOf(action.username) + 1})`
        //         if (this.showUsernames && !action.username.startsWith('exp__')) {
        //             username = action.username
        //         }
        //         if (!actionUsernames[action.action]) {
        //             actionUsernames[action.action] = [username]
        //         } else if (!actionUsernames[action.action].includes(username)) {
        //             actionUsernames[action.action].push(username)
        //         }
        //     }
            
        //     const messages = []
        //     const actionKeys = Object.keys(actionUsernames)
        //     for (const actionKey of actionKeys) {
        //         const count = actionUsernames[actionKey].length
        //         let countText = `${count}${gettext('명이')}`
        //         if (count === 1) {
        //             countText = `${actionUsernames[actionKey][0]}이(가)`
        //         }
        //         switch (actionKey) {
        //             case 'edit':
        //                 messages.push(`${countText} ${gettext('코드 수정')}`)
        //                 break
        //             case 'robot':
        //                 messages.push(`${countText} ${gettext('로봇 코드 실행')}`)
        //                 break
        //             case 'out':
        //                 messages.push(`${countText} ${gettext('코드 실행')}`)
        //                 break
        //             case 'err':
        //                 messages.push(`${countText} ${gettext('에러 확인')}`)
        //                 break
        //             case 'grade':
        //                 messages.push(`${countText} ${gettext('채점')}`)
        //                 break
        //             case 'grade-pass':
        //                 messages.push(`${countText} ${gettext('채점 결과 확인')}`)
        //                 break
        //             case 'grade-fail':
        //                 messages.push(`${countText} ${gettext('채점에서 발견된 문제 확인')}`)
        //                 break
        //             default:
        //                 break
        //         }
        //     }

        //     if (messages.length === 0) {
        //         return ''
        //     }

        //     const message = `${messages.join(', ')} ${gettext('중입니다.')}`

        //     this.lastMessageTimeStamp = now
        //     this.lastMessage = message
        //     return message
        // },
        // snapMessageIndividual() {
        //     if (this.actions.length === 0) {
        //         return ''
        //     }
        //     const lastAction = this.actions[this.actions.length - 1]
        //     let username = `${gettext('익명')} (${this.usernames.indexOf(lastAction.username) + 1})`
        //     if (this.showUsernames && !lastAction.username.startsWith('exp__')) {
        //         username = lastAction.username
        //     }
        //     switch (lastAction.action) {
        //         case 'edit':
        //             return `[${username}] ${gettext('코드를 수정합니다.')}`
        //         case 'robot':
        //             return `[${username}] ${gettext('로봇을 조종하고 있습니다.')}`
        //         case 'out':
        //             return `[${username}] ${gettext('코드를 실행했습니다.')}`
        //         case 'err':
        //             return `[${username}] ${gettext('코드에서 에러가 발생했습니다.')}`
        //         case 'grade':
        //             return `[${username}] ${gettext('코드를 채점하고 있습니다.')}`
        //         case 'grade-pass':
        //             return `[${username}] ${gettext('채점 완료! 모든 테스트를 통과했습니다.')}`
        //         case 'grade-fail':
        //             return `[${username}] ${gettext('채점 중 테스트 통과에 실패했습니다.')}`
        //         default:
        //             return ''
        //     }
        // },
        // snapMessageClass() {
        //     return ''
        // },
        // snapMessageClassIndividual() {
        //     if (this.actions.length === 0) {
        //         return ''
        //     }
        //     const lastAction = this.actions[this.actions.length - 1]
        //     switch (lastAction.action) {
        //         case 'err':
        //         case 'grade-fail':
        //             return 'is-error-text'
        //         case 'grade':
        //         case 'grade-pass':
        //             return 'is-grader-text'
        //         default:
        //             return ''
        //     }
        // },
    }
}
</script>
<style scoped>
    .exercise-snaps {
        position: relative;
        border-left: 1px solid #ddd;
    }
    .snap-message {
        position: fixed;
        z-index: 699;
        top: 0;
        left: 0;
        width: 100vw;
        height: 1.5rem;
        line-height: 1.5rem;
        font-size: 1rem;
        color: #ddd;
        text-align: center;
    }
    .is-error-text {
        color: #fc3d03;
    }
    .is-grader-text {
        color: #60afee;
        font-weight: bold;
    }
    .user-snap {
        width: 10rem;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
    }
    .user-snap:hover {
        background-color: #ddd;
    }
    .user-snap-box {
        height: 6rem;
        width: 8rem;
    }
    .user-snap-code pre {
        padding: 0;
        height: 100%;
        width: 100%;
        overflow-x: auto;
        overflow-y: auto;
    }
    .user-snap-code code {
        height: 100%;
        width: 100%;
        overflow-x: auto;
        overflow-y: auto;
        font-size: 0.3rem;
        line-height: 0.3rem;
    }
    .user-snap-outputs {
        background-color: #000;
        color: #fff;
        font-size: 0.4rem;
        line-height: 0.4rem;
    }
    .user-text {
        border-top: 1px solid #222;
        background-color: #000;
        color: #fff;
        width: 100%;
        height: 1.2rem;
        font-size: 0.75rem;
        line-height: 1.2rem;
        text-align: center;
    }
    .user-text.grade {
        color: #60afee
    }
    .user-label {
        width: 100%;
        height: 1rem;
        font-size: 0.8rem;
        text-align: center;
    }
    .focus-user-snap {
        position: fixed;
        right: 10rem;
        bottom: 0;
        background-color: #fff;
        z-index: 699;
        padding: 0.5rem 0.5rem;
        opacity: 0;
    }
    .focus-user-snap.active {
        opacity: 1;
    }
    .focus-user-snap-box {
        height: 17rem;
        width: 21rem;
    }
    .focus-user-snap-code pre {
        padding: 0;
        height: 100%;
        width: 100%;
        overflow-x: auto;
        overflow-y: auto;
    }
    .focus-user-snap-code code {
        height: 100%;
        width: 100%;
        overflow-x: auto;
        overflow-y: auto;
        font-size: 0.8rem;
        line-height: 0.8rem;
    }
    .focus-user-snap-outputs {
        background-color: #000;
        color: #fff;
        font-size: 0.8rem;
        line-height: 0.8rem;
    }
    .focus-user-text {
        border-top: 1px solid #222;
        background-color: #000;
        color: #fff;
        width: 100%;
        height: 1.5rem;
        font-size: 0.8rem;
        line-height: 1.5rem;
        text-align: center;
    }
    .focus-user-text.grade {
        color: #60afee
    }
    .focus-user-label {
        width: 100%;
        height: 1rem;
        font-size: 0.8rem;
        font-weight: bold;
        text-align: center;
    }
</style>
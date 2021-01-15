<template>
    <runner
        ref="runner"
        :course="course"
        :material="material"
        :expMode="expMode"
        :value="value"
        @snap="snap => $emit('snap', snap)"
        @log="log => $emit('log', log)"
    ></runner>
</template>
<script>
import Runner from '../runner/runner'
export default {
    name: 'exercise-runner',
    props: [
        'course',
        'material',
        'expMode',
        'value',
    ],
    components: {
        Runner,
    },
    methods: {
        run() {
            return this.$refs.runner.run()
        },
    }
}
</script>
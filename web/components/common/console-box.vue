<template>
    <div class="console-box u-fill u-scrollable" ref="consoleBox">
        <div class="outputs is-family-code" :class="{'outputs-padded': !noPadding}" ref="container"><span
            v-for="(output, i) in outputs"
            class="output"
            :key="i"
            :class="{
                'output-error': output.type === 'err',
                'output-grade': output.type === 'grade',
            }"
        >{{ output.value }}</span></div>
    </div>
</template>
<script>
export default {
    name: 'console-box',
    props: [
        'outputs',
        'noPadding',
    ],
    data() {
        return {
            box: null,
            robotDrawer: null,
        }
    },
    mounted() {
        this.scroll()
    },
    methods: {
        scroll() {
            this.$nextTick(() => {
                const container = this.$refs.container
                container.scrollTo(0, container.scrollHeight);
            })
        },
    },
    watch: {
        outputs() {
            this.scroll()
        }
    }
}
</script>
<style scoped>
    .console-box {
           
    }
    .outputs {
        white-space: pre-wrap;
        word-break: break-all;
        overflow-y: auto;
        height: 100%;
        padding: 0.2rem;
    }
    .outputs-padded {
        padding: 1rem;
    }
    .output-error {
        color: #fd7358;
    }
    .output-grade {
        color: #60afee
    }
</style>
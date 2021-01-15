<template>
    <div v-if="visible" class="dialog-modal modal is-active">
        <div class="modal-background"></div>
        <div class="modal-card">
            <header v-if="title" class="modal-card-head">
                <p class="modal-card-title">{{ title }}</p>
                <button class="delete" aria-label="close" @click="() => action('close')"></button>
            </header>
            <section class="modal-card-body">
                {{ body }}
            </section>
            <footer class="modal-card-foot">
                <template v-if="mode === 'ok' || !mode">
                    <button class="button is-success" @click="() => action('ok')">{{ gettext('확인') }}</button>
                </template>
                <template v-else-if="mode === 'okCancel'">
                    <button class="button is-success" @click="() => action('ok')">{{ gettext('확인') }}</button>
                    <button class="button" @click="() => action('cancel')">{{ gettext('취소') }}</button>
                </template>
                <template v-else-if="mode === 'yesNo'">
                    <button class="button is-success" @click="() => action('yes')">{{ gettext('네') }}</button>
                    <button class="button" @click="() => action('no')">{{ gettext('아니오') }}</button>
                </template>
                <template v-else-if="mode === 'retryCancel'">
                    <button class="button is-success" @click="() => action('retry')">{{ gettext('다시 시도') }}</button>
                    <button class="button" @click="() => action('cancel')">{{ gettext('취소') }}</button>
                </template>
            </footer>
        </div>
    </div>
</template>
<script>
export default {
    name: 'dialog-modal',
    data() {
        return {
            gettext,
            visible: false,
            title: '',
            body: '',
            mode: '',
            resolve: null,
        }
    },
    methods: {
        show(body, params) {
            this.body = body
            this.title = params.title || gettext('알림')
            this.mode = params.mode || ''
            this.visible = true
            return new Promise((resolve, _) => {
                this.resolve = resolve
            })
        },
        action(value) {
            const resolve = this.resolve
            this.resolve = null
            this.visible = false
            resolve(value)
        },
    },
}
</script>
<style scoped>
    .dialog-modal {
        z-index: 999;
    }
</style>
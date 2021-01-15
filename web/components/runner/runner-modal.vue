<template>
    <div class="modal-shade" @click="close">
        <div 
            class="modal-window has-background-black has-text-white"
            :class="{
                'modal-window-wide': wide,
            }"
            @click="ignore"
        >
            <div class="u-flex-v-container u-fill">
                <div class="u-flex-item">
                    <nav class="level has-background-primary" v-if="title">
                        <div class="level-left">
                            <div class="level-item">
                                <span class="tag is-primary">
                                    {{ title }}
                                </span>
                            </div>
                        </div>
                        <div class="level-right">
                            <div class="level-item">
                                <button class="button is-primary" @click="close">
                                    <span class="icon">
                                        <i class="fa fa-close"></i>
                                    </span>
                                </button>
                            </div>
                        </div>
                    </nav>
                </div>
                <div class="u-flex-fill-item">
                    <div class="u-fill">
                        <slot></slot>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: 'runner-modal',
    props: [
        'title',
        'wide',
    ],
    methods: {
        ignore(e) {
            e.stopPropagation()
        },
        close() {
            this.$emit('close')
        },
    }
}
</script>
<style scoped>
    .level {
        margin: 0
    }
    .modal-shade {
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(0, 0, 0, 0.5);
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 700;
        cursor: pointer;
    }
    .modal-window {
        width: 80%;
        max-width: 50rem;
        height: 80%;
        z-index: 710;
        cursor: default;
    }
    .modal-window-wide {
        max-width: 70rem;
    }
    .title-row {
        display: flex;
        justify-content: space-between;
    }
</style>
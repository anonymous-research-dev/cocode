<template>
    <div>
        <div class="modal-shade" @click="() => $emit('close')"></div>
        <div class="modal-background">
            <div class="modal-window has-background-white has-text-black" @click="ignore">
                <nav class="level has-background-primary has-text-white" v-if="title">
                    <div class="level-left">
                        <div class="level-item">
                            <span class="tag is-primary">
                                {{ title }}
                            </span>
                        </div>
                    </div>
                    <div class="level-right">
                        <div class="level-item">
                            <button class="button is-primary">
                                <span class="icon">
                                    <i class="fa fa-close"></i>
                                </span>
                            </button>
                        </div>
                    </div>
                </nav>
                <slot></slot>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: 'modal',
    props: [
        'title',
    ],
    methods: {
        ignore(e) {
            e.stopPropagation()
        }
    }
}
</script>
<style scoped>
    .modal-shade {
        background: rgba(0, 0, 0, 0.5);
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 700;
        cursor: pointer;
    }
    .modal-background {
        display: flex;
        align-items: center;
        justify-content: center;
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 705;
    }
    .modal-window {
        width: 80%;
        max-width: 50rem;
        min-height: 20rem;
        max-height: 80%;
        z-index: 710;
        cursor: default;
    }
    .title-row {
        display: flex;
        justify-content: space-between;
    }
</style>
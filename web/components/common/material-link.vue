<template>
    <a
        class="material-link has-text-black is-size-6"
        :class="{
            'has-background-white-bis': active,
            'disabled-link': !accessible,
        }"
        :href="accessible ? `/courses/${course.id}/materials/${material.id}` : undefined"
    >
        <div class="material-icon">
            <i v-if="material.type === 'exercise'" class="fa fa-pencil"></i>
            <i v-else-if="material.type === 'article'" class="fa fa-file-text-o"></i>
            <i v-else-if="material.type === 'survey'" class="fa fa-check"></i>
        </div>
        <div class="material-progress">
            <progress 
                class="progress is-success is-small" 
                :value="getProgress(material)" 
                max="100"
            >
                {{ getProgress(material) }}%
            </progress>
        </div>
        <div 
            class="material-title has-text-weight-bold"
            :class="{
                'has-text-black': !active && accessible,
                'has-text-grey': !accessible,
                'has-text-link': active,
            }"
        >
            {{ material.name }}
            <i v-if="!accessible" class="lock-icon fa fa-lock"></i>
        </div>
        <div v-if="material.type === 'exercise'" class="material-stars">
            <span class="has-text-warning" v-for="n in 3" :key="n">
                <i v-if="n <= getStar(material)" class="fa fa-star"></i>
                <i v-else class="fa fa-star-o"></i>
            </span>
        </div>
    </a>
</template>
<script>
export default {
    name: 'material-link',
    props: [
        'course',
        'material',
        'materialStatesMap',
        'active',
        'accessible',
    ],
    methods: {
        getProgress(material) {
            if (this.materialStatesMap[material.id]) {
                return this.materialStatesMap[material.id].progress
            } else {
                return 0
            }
        },
        getStar(material) {
            if (this.materialStatesMap[material.id]) {
                return this.materialStatesMap[material.id].star
            } else {
                return 0
            }
        },
    }
}
</script>
<style scoped>
    .material-link {
        padding: 1rem 1rem;
        border-top: 1px solid #aaaaaa;
        display: flex;
        flex-flow: row nowrap;
        cursor: pointer;
        align-items: center;
    }
    .material-link:hover {
        text-decoration: underline;
    }
    .disabled-link { 
        cursor: not-allowed;
    }
    .material-icon {
        padding-right: 1rem;
    }
    .lock-icon {
        padding-left: 0.25rem;
    }
    .material-title {

    }
    .material-progress {
        padding-right: 1rem;
    }
    .material-progress progress {
        width: 1rem;
    }
    .material-stars {
        padding-left: 1rem;
    }
</style>
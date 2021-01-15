<template>
    <div class="course">
        <div class="course-description is-size-6 u-v-large-padded">
            {{ course.description }}
        </div>
        <div 
            v-for="(chapter, i) in course.chapters" 
            :key="`chapter-${i}`"
            class="chapter u-v-large-padded"
        >
            <div class="chapter-title has-text-primary is-size-4 has-text-weight-bold u-v-padded">
                {{ chapter.name }}
            </div>
            <div class="chapter-description is-size-6 u-v-padded">
                {{ chapter.description }}
            </div>
            <div class="chapter-materials u-v-padded">
                <material-link
                    v-for="(material, j) in chapter.materials"
                    :key="`material-${i}-${j}`"
                    :course="course"
                    :material="material"
                    :materialStatesMap="materialStatesMap"
                    :accessible="materialAccessibleMap[material.id]"
                ></material-link>
            </div>
        </div>
        </div>
    </div>
</template>
<script>
import MaterialLink from './common/material-link'
export default {
    name: 'course',
    props: [
        'course',
        'initMaterialStatesMap',
        'initMaterialAccessibleMap',
    ],
    components: {
        MaterialLink,
    },
    data() {
        return {
            materialStatesMap: {},
            materialAccessibleMap: {},
        }
    },
    created() {
        this.materialAccessibleMap = this.initMaterialAccessibleMap
        this.materialStatesMap = this.initMaterialStatesMap
        window.addEventListener('cocode-material-state-update', this.loadStates)
    },
    beforeDestroy() {
        window.removeEventListener('cocode-material-state-update', this.loadStates)
    },
    methods: {
        async loadStates() {
            const baseUrl = `/en/courses/${this.course.id}`
            const response = await axios.get(`${baseUrl}/state_maps`)
            this.materialStatesMap = response.data.data.material_states_dict
            this.materialAccessibleMap = response.data.data.material_accessible_dict
        },
    },
    watch: {
    }
}
</script>
<style scoped>
    .course {

    }
    .chapter {
        border-top: 1px solid #aaaaaa;
    }
</style>
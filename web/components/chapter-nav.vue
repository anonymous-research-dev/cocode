<template>
    <div class="chapter-nav">
        <a class="button is-white is-fullwidth" :href="`/courses/${course.id}`">
            <span class="icon is-small">
                <i class="fa fa-home"></i>
            </span>
            <span>{{ gettext('돌아가기') }}</span>
        </a>
        <div class="materials">
            <material-link
                v-for="(currMaterial, j) in materials"
                :key="`material-${j}`"
                :course="course"
                :material="currMaterial"
                :materialStatesMap="materialStatesMap"
                :active="material.id === currMaterial.id"
                :accessible="materialAccessibleMap[currMaterial.id]"
            ></material-link>
        </div>
        <a 
            class="button is-white is-fullwidth"
            :class="{
                'disabled-link': !nextChapterAccessible,
                'has-text-grey': !nextChapterAccessible,
            }"
            v-if="nextLinkMaterial"
            :href="nextChapterAccessible ? `/courses/${course.id}/materials/${nextLinkMaterial.id}` : undefined"
        >
            <span class="icon is-small">
                <i v-if="nextChapterAccessible" class="fa fa-arrow-right"></i>
                <i v-else class="fa fa-lock"></i>
            </span>
            <span>{{ gettext('다음 장으로 이동') }}</span>
        </a>
    </div>
</template>
<script>
import MaterialLink from './common/material-link'
export default {
    name: 'chapter-nav',
    props: [
        'course',
        'material',
        'initMaterialStatesMap',
        'initMaterialAccessibleMap',
    ],
    components: {
        MaterialLink,
    },
    data() {
        return {
            gettext,
            materialStatesMap: {},
            materialAccessibleMap: {},
            materials: [],
            nextLinkMaterial: null,
            nextChapterAccessible: true,
        }
    },
    created() {
        this.materialAccessibleMap = this.initMaterialAccessibleMap
        this.materialStatesMap = this.initMaterialStatesMap
        this.setMaterials()
        window.addEventListener('cocode-material-state-update', this.loadStates)
    },
    beforeDestroy() {
        window.removeEventListener('cocode-material-state-update', this.loadStates)
    },
    methods: {
        setMaterials() {
            this.course.chapters.forEach((chapter, i) => {
                const isCurrChapter = chapter.materials.filter(material => (
                    material.id === this.material.id
                )).length > 0
                if (isCurrChapter) {
                    this.materials = chapter.materials
                    if (i + 1 < this.course.chapters.length) {
                        const materials = this.course.chapters[i + 1].materials
                        if (materials) {
                            this.nextLinkMaterial = materials[0]
                            this.nextChapterAccessible = this.materialAccessibleMap[materials[0].id]
                        }
                    }
                }
            })
        },
        async loadStates() {
            const baseUrl = `/en/courses/${this.course.id}`
            const response = await axios.get(`${baseUrl}/state_maps`)
            this.materialStatesMap = response.data.data.material_states_dict
            this.materialAccessibleMap = response.data.data.material_accessible_dict
            if (this.nextLinkMaterial) {
                this.nextChapterAccessible = this.materialAccessibleMap[this.nextLinkMaterial.id]
            }
        },
    },
    watch: {
        
    }
}
</script>
<style scoped>
    .chapter-nav {

    }
    .materials {
        border-bottom: 1px solid #aaaaaa;
    }
    .disabled-link { 
        cursor: not-allowed;
    }
</style>
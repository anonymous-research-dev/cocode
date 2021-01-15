<template>
    <div class="article-text u-fill u-scrollable">
        <div class="u-narrow-container u-padded">
            <markdown-content
                :course="course"
                :material="material"
                :content="content"
            ></markdown-content>
            <div class="u-v-padded">
                <a 
                    class="button is-success" 
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
        </div>
    </div>
</template>
<script>
import MarkdownContent from './common/markdown-content'

export default {
    name: 'article-text',
    props: [
        'course',
        'materialStatesMap',
        'material',
        'nextMaterial',
        'content',
    ],
    components: {
        MarkdownContent,
    },
    data() {
        return {
            gettext,
            nextMaterialAccessible: false,
        }
    },
    created() {

    },
    mounted() {
        this.updateProgress()
    },
    methods: {
        async updateProgress() {
            const state = this.materialStatesMap[this.material.id]
            const progress = state ? state.progress : 0
            if (progress < 100) {
                const baseUrl = `/en/courses/${this.course.id}/materials/${this.material.id}`
                const response = await axios.post(`${baseUrl}/state/`, { progress: 100 })
                if (response.data.status === 200) {
                    window.dispatchEvent(new CustomEvent('cocode-material-state-update'));
                    if (this.nextMaterial) {
                        this.nextMaterialAccessible = true
                    }
                } else {
                    console.error('Failed to update the material state.')
                }
            } else {
                if (this.nextMaterial) {
                    this.nextMaterialAccessible = true
                }
            }
        }
    },
    watch: {
        
    }
}
</script>
<style scoped>
    .article-text {

    }
</style>
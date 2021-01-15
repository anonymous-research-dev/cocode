<template>
    <div class="markdown-content content" ref="container">
        <vue-markdown 
            :source="source"
            :breaks="false"
            @rendered="postprocess"
        ></vue-markdown>
    </div>
</template>
<script>
import Vue from 'vue'
import CodeBlock from './code-block'

export default {
    name: 'markdown-content',
    props: [
        'course',
        'material',
        'content',
    ],
    data() {
        return {
            source: ''
        }
    },
    created() {
        this.preprocess()
    },
    mounted() { 
        this.postprocess()
    },
    methods: {
        preprocess() {
            // Replace image sources.
            const staticUrl = __COCODE__.staticUrl
            const imageExp = /(?:!\[(.*?)\]\((.*?)\))/g
            this.source = this.content.replace(imageExp, (match, g1, g2) => {
                if (g2.startsWith('./serve/') || g2.startsWith('serve/')) {
                    const filename = g2.slice(g2.indexOf('serve/') + 'serve/'.length)
                    return `![${g1}](${staticUrl}/courses/${this.course.id}/${this.material.id}/${filename})`    
                } else {
                    return match
                }
            })
        },
        postprocess() {
            const langs = ['python']
            const container = this.$refs.container
            if (container) {
                for (const lang of langs) {
                    const className = `language-${lang}`
                    const interactiveClassName = `language-${lang}--run`
                    const blocks = [
                        ...container.querySelectorAll(`code.${className}`),
                        ...container.querySelectorAll(`code.${interactiveClassName}`),
                    ]
                    blocks.forEach(block => {
                        const interactive = block.classList.contains(interactiveClassName)
                        const content = block.textContent
                        const blockContainer = document.createElement('div')
                        blockContainer.className = 'code-block-container'
                        const preElement = block.parentNode
                        preElement.parentNode.replaceChild(blockContainer, preElement);
                        this.renderCodeBlock(blockContainer, lang, content, interactive)
                    })
                }
            }
        },
        renderCodeBlock(targetElement, lang, content, interactive) {
            var CodeBlockComponent = Vue.extend(CodeBlock)
            var instance = new CodeBlockComponent({
                propsData: { lang, content, interactive },
            })
            // instance.$slots.default = [ 'Click me!' ]
            instance.$mount() 
            targetElement.appendChild(instance.$el)
        }
    },
    watch: {
        content() {
            this.preprocess()
        }
    }
}
</script>
<style scoped>
    .markdown-content {

    }
</style>
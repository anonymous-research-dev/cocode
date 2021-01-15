<template>
    <div class="survey u-fill u-scrollable">
        <div class="u-narrow-container u-padded">
            <div class="u-v-padded">
                <markdown-content
                    :course="course"
                    :material="material"
                    :content="content"
                ></markdown-content>
            </div>
            <div class="survey-form u-v-padded has-text-grey-dark">
                <div class="survey-item" v-for="question in questions" :key="question.id">
                    <div v-if="question.type === 'content'" class="question-form content-item">
                        <div class="u-v-padded has-text-weight-bold has-text-block">
                            {{ question.value }}
                        </div>
                    </div>
                    <div v-else-if="question.type === 'radio'" class="question-form">
                        <div class="u-v-small-padded has-text-weight-bold">
                            {{ question.question }}
                            <i v-if="!question.optional" class="fa fa-asterisk required-icon has-text-danger"></i>
                        </div>
                        <div v-if="question.description" class="u-v-small-bottom-padded is-size-6 has-text-grey-dark">
                            {{ question.description }}
                        </div>
                        <div class="control">
                            <label class="radio" v-for="option in question.options" :key="option">
                                <input type="radio" :name="question.id" :value="option" v-model="answers[question.id]" @input="handleInput">
                                {{ option }}
                            </label>
                        </div>
                    </div>
                    <div v-else-if="question.type === 'text'" class="question-form">
                        <div class="u-v-small-padded has-text-weight-bold">
                            {{ question.question }}
                            <i v-if="!question.optional" class="fa fa-asterisk required-icon has-text-danger"></i>
                        </div>
                        <div v-if="question.description" class="u-v-small-bottom-padded is-size-7 has-text-grey-dark">
                            {{ question.description }}
                        </div>
                        <div class="control">
                            <input class="input" type="text" v-model="answers[question.id]" @input="handleInput">
                        </div>
                    </div>
                    <div v-else-if="question.type === 'long_text'" class="question-form">
                        <div class="u-v-small-padded has-text-weight-bold">
                            {{ question.question }}
                            <i v-if="!question.optional" class="fa fa-asterisk required-icon has-text-danger"></i>
                        </div>
                        <div v-if="question.description" class="u-v-small-bottom-padded is-size-6 has-text-grey-dark">
                            {{ question.description }}
                        </div>
                        <div class="control">
                            <textarea class="textarea" v-model="answers[question.id]" @input="handleInput"></textarea>
                        </div>
                    </div>
                    <div v-else-if="question.type === 'likert_5'" class="question-form">
                        <div class="u-v-small-padded has-text-weight-bold">
                            {{ question.question }}
                            <i v-if="!question.optional" class="fa fa-asterisk required-icon has-text-danger"></i>
                        </div>
                        <div v-if="question.description" class="u-v-small-bottom-padded is-size-6 has-text-grey-dark">
                            {{ question.description }}
                        </div>
                        <div class="control">
                            <label class="radio">
                                <input type="radio" :name="question.id" :value="'likert_1'" v-model="answers[question.id]" @input="handleInput">
                                {{ gettext('매우 그렇지 않다') }}
                            </label>
                            <label class="radio">
                                <input type="radio" :name="question.id" :value="'likert_2'" v-model="answers[question.id]" @input="handleInput">
                                {{ gettext('그렇지 않다') }}
                            </label>
                            <label class="radio">
                                <input type="radio" :name="question.id" :value="'likert_3'" v-model="answers[question.id]" @input="handleInput">
                                {{ gettext('보통이다') }}
                            </label>
                            <label class="radio">
                                <input type="radio" :name="question.id" :value="'likert_4'" v-model="answers[question.id]" @input="handleInput">
                                {{ gettext('그렇다') }}
                            </label>
                            <label class="radio">
                                <input type="radio" :name="question.id" :value="'likert_5'" v-model="answers[question.id]" @input="handleInput">
                                {{ gettext('매우 그렇다') }}
                            </label>
                        </div>
                    </div>
                </div>
            </div>
            <div class="u-v-padded">
                <div v-if="nextMaterial && !nextMaterialAccessible" class="u-v-small-padded has-text-danger is-size-7">
                    {{ gettext('모든 필수 질문에 답을 입력해주세요.') }} 
                    <i class="fa fa-asterisk required-icon"></i>
                </div>
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
import { throttle, debounce } from 'throttle-debounce';
import MarkdownContent from './common/markdown-content'

export default {
    name: 'survey',
    props: [
        'course',
        'materialStatesMap',
        'material',
        'nextMaterial',
        'content',
        'questions',
        'initAnswers',
    ],
    components: {
        MarkdownContent,
    },
    data() {
        return {
            gettext,
            nextMaterialAccessible: false,
            answers: { ...this.initAnswers },
        }
    },
    created() {
        this.uploadAnswersDb = debounce(1000, this.uploadAnswers);
        this.updateProgress()
    },
    mounted() {
        
    },
    methods: {
        handleInput() {
            this.uploadAnswersDb()
        },
        async uploadAnswers() {
            const baseUrl = `/en/courses/${this.course.id}/materials/${this.material.id}`
            const response = await axios.post(`${baseUrl}/survey_answers/`, { answers: this.answers })
            if (response.data.status === 200) {
                this.updateProgress()
            } else {
                console.error('Failed to update the material state.')
            }
        },
        isValid() {
            for (const question of this.questions) {
                if (question.id && !question.optional) {
                    const value = this.answers[question.id]
                    if (value === undefined || value === '') {
                        return false
                    }
                }
            }
            return true
        },
        async updateProgress() {
            const state = this.materialStatesMap[this.material.id]
            const progress = state ? state.progress : 0
            if (this.isValid() && progress < 100) {
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
            } else if (progress >= 100) {
                if (this.nextMaterial) {
                    this.nextMaterialAccessible = true
                }
            }
        }
    },
    watch: {
        answers() {
            console.log('watch answers', this.answers)
        }
    }
}
</script>
<style scoped>
    .survey-form {
        margin: 2rem 0;
        font-size: 1rem;
    }
    .survey-item {
        padding: 1rem 0;
    }
    .content-item {
        font-size: 1.25rem;
    }
    .required-icon {
        padding-left: 0.25rem;
    }
</style>
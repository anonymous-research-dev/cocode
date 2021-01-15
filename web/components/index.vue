<template>
    <div class="index">
        <div class="u-v-padded">
            <span class="is-size-3">
                {{ gettext('모든 과목') }}
            </span>
        </div>
        <div class="all-courses u-v-padded">
            <div
                v-for="courseId in index.featured" 
                class="course-card card" 
                :key="courseId"
            >
                <div class="card-content">
                    <div class="media">
                        <!-- <div class="media-left">
                            <figure class="image is-48x48">
                            <img src="https://bulma.io/images/placeholders/96x96.png" alt="Placeholder image">
                            </figure>
                        </div> -->
                        <div class="media-content">
                            <a 
                                class="
                                    course-title
                                    title
                                    is-4
                                    has-text-link
                                    has-text-weight-bold
                                "
                                :href="`./${courseId}`"
                            >
                                {{ index.courses[courseId].name }}
                            </a>
                            <!-- <p class="subtitle is-6">@johnsmith</p> -->
                        </div>
                    </div>
                    <div class="content">
                        {{ index.courses[courseId].description }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: 'index',
    props: [
        'index',
    ],
    data() {
        return {
            gettext,
        }
    },
    created() {

    },
    methods: {

    },
    watch: {
        
    }
}
</script>
<style scoped>
    .index {

    }
    .course-title {

    }
</style>
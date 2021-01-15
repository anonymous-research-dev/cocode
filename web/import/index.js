// JS libraries
import 'bulma-extensions/dist/js/bulma-extensions'
import './style-form'
import Vue from 'vue/dist/vue'
import Axios from 'axios/dist/axios'
import Jquery from 'jquery/dist/jquery'
import QueryString from 'query-string'

// Vue.js components
import VueMarkdown from 'vue-markdown'

// Export to global scope.
window.Vue = Vue
window.axios = Axios
window.$ = window.jquery = Jquery
window.QueryString = QueryString

// Take CSRF Token.
window.setCsrfToken = token => {
    axios.defaults.headers.common['X-CSRFToken'] = token
}

// Register to Vue.js
Vue.component('vue-markdown', VueMarkdown)

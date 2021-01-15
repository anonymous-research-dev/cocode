
import './style'
import './import'
import Index from './components/index'
import DialogModal from './components/dialog-modal'

window.__COCODE__ = window.__COCODE__ || {}
window.setStaticUrl = url => (window.__COCODE__.staticUrl = url)

Vue.component('index', Index)
Vue.component('dialog-modal', DialogModal)
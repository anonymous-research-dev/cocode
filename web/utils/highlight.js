import hljs from 'highlight.js/lib/highlight'
import javascript from 'highlight.js/lib/languages/javascript'
import python from 'highlight.js/lib/languages/python'

hljs.registerLanguage('javascript', javascript)
hljs.registerLanguage('python', python)

export default function highlight(code, language) {
    return hljs.highlightAuto(code, [language]).value
}

function esc(s) {
    return s
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
}

function unesc(s) {
    return s
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&amp;/g, '&')
}

function replacer(match, g1, g2, g3, offset, string) {
    const prefix = match.startsWith('>') ? '>' : ''
    const block = esc(unesc(g2).replace(/[^₩`~!@#$%^&*()-=_+\[\]\\{}|;':",./<>?\s]/g, '█'))
    const suffix = match.endsWith('<') ? '<' : ''
    return prefix + block + suffix
}

export function blockify(code, language) {
    const highlighted = highlight(code, language)
    return highlighted.replace(/(>|^)([^<>]*)(<|$)/g, replacer)
}
function styleForms() {
    $('.styled-form input[type=text],input[type=password],input[type=email],input[type=tel],input[type=number]').addClass('input')
    $('.styled-form textarea').addClass('textarea')
    $('.styled-form select').wrap('<div class="select"></div>')
    $('.styled-form input[type=radio]').parent().addClass('radio').unwrap()
}

window.addEventListener('load', styleForms)
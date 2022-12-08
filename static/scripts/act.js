const buy_open = document.querySelector('.buy-open')
const sell_open = document.querySelector('.sell-open')
const buy_btn = document.querySelector('.buy-btn')
const sell_btn = document.querySelector('.sell-btn')
const buy_box = document.querySelector('.act-buy-box')
const sell_box = document.querySelector('.act-sell-box')
const buy_cont = document.querySelector('.buy-cont')
const sell_cont = document.querySelector('.sell-cont')
const buy_cost = document.querySelector('.buy-cost')
const sell_cost = document.querySelector('.sell-cost')
const buy_input = document.querySelector('.buy-input')
const sell_input = document.querySelector('.sell-input')

const dialog_error = document.querySelector('.error')

const searchString = new URLSearchParams(window.location.search);
let buy_opened = false
let sell_opened = false

buy_open.addEventListener('click', () => {
    if (buy_opened == false) {
        buy_cont.classList.remove('hide')
        buy_cost.classList.add('hide')
        buy_btn.classList.remove('hide')
        buy_open.innerHTML = '<i class="uil uil-multiply"></i>'
        buy_opened = true
    } else if (buy_opened == true){
        buy_cont.classList.add('hide')
        buy_cost.classList.remove('hide')
        buy_btn.classList.add('hide')
        buy_open.innerHTML = 'Купить'
        buy_opened = false
    }
})

sell_open.addEventListener('click', () => {
    if (sell_opened == false) {
        sell_cont.classList.remove('hide')
        sell_cost.classList.add('hide')
        sell_btn.classList.remove('hide')
        sell_open.innerHTML = '<i class="uil uil-multiply"></i>'
        sell_opened = true
    } else if (sell_opened == true){
        sell_cont.classList.add('hide')
        sell_cost.classList.remove('hide')
        sell_btn.classList.add('hide')
        sell_open.innerHTML = 'Продать'
        sell_opened = false
    }
})


buy_btn.addEventListener('click', () => {
    const xhr = new XMLHttpRequest()
    xhr.open('POST', '/api', true)
    let body = {
        action: 'buy',
        act_id: '',
        cost: '',
        utoken: '',
        amount: 0,
    }
    body.act_id = searchString.get('id')
    let cost = buy_cost.innerHTML.replace('$', '').replace('₽', '').replace('€', '')
    body.cost = cost
    body.utoken = getCookie('token')
    body.amount = buy_input.value
    body = JSON.stringify(body)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.send(body)
    xhr.onload = () => {
        if (xhr.response == 'NO_MONEY') {
            dialog_error.innerHTML = 'Недостаточно средств. <br> Нажмите в любом месте для закрытия.'
            dialog_error.style.visibility = 'visible'
        }
    }
})

sell_btn.addEventListener('click', () => {
    const xhr = new XMLHttpRequest()
    xhr.open('POST', '/api', true)
    let body = {
        action: 'sell',
        act_id: '',
        cost: '',
        utoken: '',
        amount: 0,
    }
    body.act_id = searchString.get('id')
    body.cost = buy_cost.innerHTML.replace('$', '')
    body.cost = buy_cost.innerHTML.replace('€', '')
    body.cost = sell_cost.innerHTML.replace('₽', '')
    body.utoken = getCookie('token')
    body.amount = sell_input.value
    body = JSON.stringify(body)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.send(body)
    xhr.onload = () => {
        if (xhr.response == 'NO_SHARES') {
            dialog_error.innerHTML = 'У вас не таких акций. <br> Нажмите в любом месте для закрытия.'
            dialog_error.style.visibility = 'visible'
        }
    }
})

function getCookie(name) {

    var matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
}

document.addEventListener('click', ()=> {
    dialog_error.style.visibility = 'hidden'
})
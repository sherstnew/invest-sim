const buy_btn = document.querySelector('.buy-btn')
const sell_btn = document.querySelector('.sell-btn')
const buy_box = document.querySelector('.act-buy-box')
const sell_box = document.querySelector('.act-sell-box')
const buy_cont = document.querySelector('.buy-cont')
const sell_cont = document.querySelector('.sell-cont')

buy_btn.addEventListener('click', () => {
    buy_box.style.width = '150px'
    buy_cont.classList.remove('hide')
})

sell_btn.addEventListener('click', () => {
    sell_box.style.width = '200px'
    sell_cont.classList.remove('hide')
})
let account = ''
let accounts = ''
let token = document.cookie.replace(/(?:(?:^|.*;\s*)token\s*\=\s*([^;]*).*$)|^.*$/, "$1")

const auth = new XMLHttpRequest()
auth.open('POST', '/api', true)
let body = {
    action: 'accounts'
}
body = JSON.stringify(body)
auth.setRequestHeader('Content-Type', 'application/json')
auth.send(body)

auth.onload = () => {
    if (auth.status == '200') {
        accounts = JSON.parse(auth.response).accounts
        accounts = accounts.replaceAll('(', '')
        accounts = accounts.replaceAll(')', '')
        accounts = accounts.replaceAll("'", '')
        accounts = accounts.replaceAll(' ', '')
        accounts = accounts.replaceAll('&#39;', '')
        accounts = accounts.split(';')
        accounts.pop()
        accounts.forEach(acc => {
            acc = acc.split(',')
            acc[0] = acc[0].replaceAll("'", "")
            if (token == '') {
                location = '/login'
            } else if (token == acc[0]) {
                account = acc
            }
        })
    }
}
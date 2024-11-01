// static/js/main.js

document.querySelector('.menu-toggle').addEventListener('click', function() {
    const menu = document.querySelector('.menu-items');
    menu.classList.toggle('show');
});

function confirmLogout() {
    if (confirm('ログアウトしますか？')) {
        document.getElementById('logout-form').submit();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const message = document.getElementById('message');
    if (message) {
        message.classList.add('show');
        setTimeout(function() {
            message.classList.remove('show');
        }, 5000);
    }
});
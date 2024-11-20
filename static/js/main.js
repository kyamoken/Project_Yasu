// static/js/main.js

let navToggleTimeout = null;
document.querySelector('.menu-toggle').addEventListener('click', function() {
    const menu = document.querySelector('.menu-items');
    if (menu.classList.contains('show')) {
        menu.classList.remove('show');
        clearTimeout(navToggleTimeout);
        navToggleTimeout = setTimeout(() => {
            menu.style.display = 'none';
        }, 500);
    } else {
        clearTimeout(navToggleTimeout);
        menu.style.display = 'block';
        navToggleTimeout = setTimeout(() => {
            menu.classList.add('show');
        }, 20);
   }
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
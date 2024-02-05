
document.addEventListener('DOMContentLoaded', function () {
    const logoutForm = document.querySelector('#logout-form');
    const logoutLoader = document.querySelector('#logout-form .logout-loader .lds-ripple-cont')
    logoutForm.addEventListener("submit", function (){
        logoutLoader.classList.add('active');
    });

});
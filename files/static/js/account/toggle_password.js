const togglePassword = document.querySelectorAll('.togglePassword');
// const togglePasswordConfirm = document.querySelector('#togglePasswordConfirm');
const password = document.querySelectorAll('.password');
// const password_confirm = document.querySelector('#password_confirm');

// array.forEach(element => {
    
// });

var counter = 0
togglePassword.forEach(element => {
    var currentPassword = password[counter]
    element.addEventListener('click', function (e) {
        var type = currentPassword.getAttribute('type') === 'password' ? 'text' : 'password';
        currentPassword.setAttribute('type', type);
        this.classList.toggle('bi-eye');
    });
    counter += 1
});

// togglePassword.addEventListener('click', function (e) {
//     const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
//     password.setAttribute('type', type);
//     this.classList.toggle('bi-eye');
// });

// togglePasswordConfirm.addEventListener('click', function (e) {
//     const type = password_confirm.getAttribute('type') === 'password' ? 'text' : 'password';
//     password_confirm.setAttribute('type', type);
//     this.classList.toggle('bi-eye');
// });
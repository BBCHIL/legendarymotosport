const optionsMenu = document.querySelector('.user__options-container')

function isLogged() {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${'auth_token'}=`);
    if (parts.length === 2) {
        return true
    }else {
        return false
    }
}
const logged = isLogged();

function hideOptions() {
    if (!logged) {
        optionsMenu.style.display = 'none';
    }
}

hideOptions()
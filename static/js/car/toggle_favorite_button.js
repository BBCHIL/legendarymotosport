const favoriteButton = document.querySelector('#add-favorite-button')

function isLogged() {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${'auth_token'}=`);
    if (parts.length === 2) {
        return true
    }else {
        return false
    }
}
const logged = isLogged()

function toggleFavoriteButton() {
    if (logged) {
        favoriteButton.style.display = 'flex'
    };
};


toggleFavoriteButton()

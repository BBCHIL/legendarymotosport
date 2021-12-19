const hamburgerMenu = document.querySelector('.menu__box')
const topMenu = document.querySelector('.nav-top__list')


function isLogged() {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${'auth_token'}=`);
    if (parts.length === 2) {
        return true
    }else {
        return false
    }
}

function getOption() {
    // returns li elem with login or logout link depending
    // if user is logged or not
    const li_cls = "nav-top__element";
    const a_cls = "nav-top__link";

    var li_elem = document.createElement('li');
    var link = document.createElement('a');
    
    li_elem.setAttribute("class", li_cls);
    link.setAttribute("class", a_cls);
    
    const logged = isLogged();
    if (logged) {
        var href = "/account/logout/"
        var text = "LOGOUT"
    } else {
        var href = "/account/login/"
        var text = "LOGIN"
    }

    var text = document.createTextNode(text);

    link.appendChild(text);
    link.setAttribute("href", href);

    li_elem.appendChild(link);

    return li_elem
}

function addOption(menu, option) {
    menu.appendChild(option);
}

addOption(hamburgerMenu, getOption());
addOption(topMenu, getOption());
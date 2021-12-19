var dangerZone = document.querySelectorAll(".car__danger")
var dangerButton = document.querySelector("#toggleDanger")

// console.log(dangerZone)

function toggleDanger(element) {
    var display = (element.style.display === 'flex') ? 'none': 'flex';
    element.style.display = display
}

dangerZone.forEach(element => {
    dangerButton.addEventListener('click', function (e) {
        toggleDanger(element)
    })
});



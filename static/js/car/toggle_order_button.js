const toggleSubmitButton = document.querySelectorAll('.color-container__choice');

toggleSubmitButton.forEach(element => {
    {
        element.addEventListener('click', function (e) {
            if (logged) {
                document.getElementById('toggleSubmit').style.display = 'block'
            }
            else {
                var msg = "You have to be logged in to make orders"
                alert(msg)
            }
        });
    }    
});

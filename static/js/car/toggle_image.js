var loadFile = function(event) {
    var image = document.getElementById('output');
    var logo = document.getElementById('logo-output');
    image.src = URL.createObjectURL(event.target.files[0]);
    logo.display = 'flex';
};
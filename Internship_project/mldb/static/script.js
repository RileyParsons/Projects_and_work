/*

// cannot get this to work
document.addEventListener("DOMContentLoaded", function(){

    function loadContent(url, elementId){
        fetch(url).then(response =>{
            if (!response.ok){
                throw new Error('HTTP error ${response.status}');
            }
            return response.text();
        })
    .then(data =>{
        document.getElementById(elementId).innerHTML = data;
    }).catch(error=>{
        // console.error('Error loading content: ', error);
    });
}
// loadContent("{% static 'nav.html' %}", "nav");
// loadContent("{% static 'footer.html' %}", "footer");
});
*/
document.addEventListener("DOMContentLoaded", function() {
    var input = document.getElementById('img');
    var preview = document.getElementById('preview');

    input.addEventListener('change', function() {
        var file = this.files[0];

        if (file) {
            var reader = new FileReader();

            reader.onload = function(event) {
                preview.src = event.target.result;
            }

            reader.readAsDataURL(file);
        } else {
            preview.src = "";
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('train_form');
    var loader = document.getElementById('loader');

    form.addEventListener('submit', function() {
        // Display the loader when the form is submitted
        loader.style.display = 'block';
    });
});
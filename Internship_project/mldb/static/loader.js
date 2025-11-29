document.getElementById('loader').style.display = "none";
const loading = document.querySelector("input[id='train_now']");

loading.addEventListener('click', (event)=>{
   document.getElementById('loader').style.display = "block";
});
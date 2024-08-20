const speakbtn = document.getElementById('speak');
const textbtn = document.getElementById('text');
const regulamin = document.getElementById('regulamin');


speakbtn.addEventListener('click', function() {
    alert("Upewnij się, że twoje słuchawki oraz mikrofon działają prawidłowo")
    location.href = "ai_speaking.html"
});

textbtn.addEventListener('click', function() {
    location.href = "ai_texting.html"
});

regulamin.addEventListener('click', function() {
    location.href = "regulamin.html"
});
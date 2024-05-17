// Sayfa kaydırıldığında tetiklenecek olay
window.onscroll = function() {
    // Sayfanın en altına gelinip gelinmediğini kontrol et
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
        // Yeni içerik ekleyerek sayfanın altını genişlet
        for (let i = 0; i < 100; i++) { // Daha fazla içerik eklemek için döngü
            document.getElementById("content").innerHTML += "🐴<br>";
        }
    }
};

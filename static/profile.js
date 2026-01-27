// Hamburger menu
const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("navLinks");

hamburger.addEventListener("click", e => {
    e.stopPropagation();
    navLinks.classList.toggle("active");
});

document.addEventListener("click", e => {
    if (navLinks.classList.contains("active") && !navLinks.contains(e.target)) {
        navLinks.classList.remove("active");
    }
});

navLinks.addEventListener("click", e => e.stopPropagation());

// Mobile dropdown toggle
document.querySelectorAll(".dropdown > a").forEach(item => {
    item.addEventListener("click", e => {
        if (window.innerWidth <= 768) {
            e.preventDefault();
            item.parentElement.classList.toggle("open");
        }
    });
});


// Profile picture upload handler (demo)
const uploadForm = document.getElementById("uploadForm");
if (uploadForm) {
    uploadForm.addEventListener("submit", e => {
        e.preventDefault();
        const input = document.getElementById("profilePicInput");
        if (input.files && input.files[0]) {
            // Demo: preview uploaded image
            const reader = new FileReader();
            reader.onload = function (ev) {
                const img = document.querySelector(".profile-pic-wrapper img");
                if (img) img.src = ev.target.result;
                else {
                    const wrapper = document.querySelector(".profile-pic-wrapper");
                    wrapper.innerHTML = `<img src="${ev.target.result}" class="profile-pic">`;
                }
            }
            reader.readAsDataURL(input.files[0]);
        }
    });
}

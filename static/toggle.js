document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".toggle-button, .sub-toggle").forEach(btn => {
        btn.addEventListener("click", () => {
            btn.classList.toggle("active");
            const next = btn.nextElementSibling;
            if (next && (next.classList.contains("checkbox-group") || next.classList.contains("sub-list"))) {
                next.style.display = next.style.display === "block" ? "none" : "block";
            }
        });
    });
});


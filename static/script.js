document.addEventListener("DOMContentLoaded", () => {
    const rows = document.querySelectorAll(".styled-table tbody tr");

    rows.forEach(row => {
        // Animación al pasar el ratón
        row.addEventListener("mouseenter", () => {
            row.style.transition = "background-color 0.5s ease";
            row.style.backgroundColor = "#16a085";
            row.style.color = "white";
        });

        row.addEventListener("mouseleave", () => {
            row.style.transition = "background-color 0.5s ease";
            row.style.backgroundColor = "";
            row.style.color = "#2c3e50";
        });
    });
});

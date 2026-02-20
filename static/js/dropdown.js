document.addEventListener("DOMContentLoaded", () => {
    const dropdowns = document.querySelectorAll(".dropdown-container");

    dropdowns.forEach(dropdown => {
        const input = dropdown.querySelector(".dropdown-input");
        const list = dropdown.querySelector(".dropdown-list");
        const hidden = dropdown.querySelector(".dropdown-hidden");
        const items = dropdown.querySelectorAll(".dropdown-item");

        input.addEventListener("focus", () => {
            list.style.display = "block";
        });

        input.addEventListener("input", () => {
            const filter = input.value.toLowerCase();

            items.forEach(item => {
                const search = item.dataset.search.toLowerCase();
                item.style.display = search.includes(filter) ? "block" : "none";
            });
        });

        items.forEach(item => {
            item.addEventListener("click", () => {
                input.value = item.textContent.trim();
                hidden.value = item.dataset.id;
                list.style.display = "none";
            });
        });

        document.addEventListener("click", (e) => {
            if (!dropdown.contains(e.target)) {
                list.style.display = "none";
            }
        });
    });
});

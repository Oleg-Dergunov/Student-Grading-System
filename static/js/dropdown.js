document.addEventListener("DOMContentLoaded", () => {
    const dropdowns = document.querySelectorAll(".dropdown-container");

    dropdowns.forEach(dropdown => {
        const input = dropdown.querySelector(".dropdown-input");
        const list = dropdown.querySelector(".dropdown-list");
        const hidden = dropdown.querySelector(".dropdown-hidden");
        const items = dropdown.querySelectorAll(".dropdown-item");

        // Opening a list
        input.addEventListener("focus", () => {
            list.style.display = "block";
        });

        // Entering text manually
        input.addEventListener("input", () => {
            const value = input.value.trim().toLowerCase();

            // The user types → save it in hidden
            hidden.value = input.value.trim();

            // Фильтрация списка
            items.forEach(item => {
                const search = item.dataset.search.toLowerCase();
                item.style.display = search.includes(value) ? "block" : "none";
            });
        });

        // Selecting an item from a list
        items.forEach(item => {
            item.addEventListener("click", () => {
                const label = item.textContent.trim();
                const id = item.dataset.id;

                // Show the selected label
                input.value = label;

                // Put the ID (not the text) in hidden
                hidden.value = id;

                list.style.display = "none";
            });
        });

        // Click outside the component
        document.addEventListener("click", (e) => {
            if (!dropdown.contains(e.target)) {
                list.style.display = "none";
            }
        });
    });
});


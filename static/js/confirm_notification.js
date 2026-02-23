document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll("[data-confirm-action]").forEach(function(row) {
        row.addEventListener("click", function() {
            const message = this.dataset.confirmMessage || "Are you sure?";
            const targetFormId = this.dataset.confirmAction;
            const form = document.getElementById(targetFormId);

            if (!form) {
                console.error(`Form with id="${targetFormId}" not found`);
                return;
            }

            if (confirm(message)) {
                form.submit();
            }
        });
    });
});

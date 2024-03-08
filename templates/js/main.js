document.addEventListener('DOMContentLoaded', e => {
for (let checkbox of document.querySelectorAll('input[type=checkbox]')) {
    checkbox.value = checkbox.checked ? 1 : 0;
    checkbox.addEventListener('change', e => {
            e.target.value = e.target.checked ? 1 : 0;
        });
    }
});

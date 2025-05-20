function updatePresent(row) {
    let total = document.getElementById('total' + row).textContent;
    let absent = document.getElementById('absent' + row).value;
    let present = total - absent;
    document.getElementById('present' + row).textContent = present;
}

// function updateAbsentees(year) {
//     let selectedNames = [];
//     let checkboxes = document.querySelectorAll(`input[name='${year}_absentees[]']:checked`);
//     checkboxes.forEach(function(checkbox) {
//         selectedNames.push(checkbox.value);
//     });
//     document.getElementById(`${year}_absent_names`).value = selectedNames.join(", ");
// }


// Toggles the visibility of the dropdown content
function toggleDropdown(button) {
    const dropdown = button.nextElementSibling;
    dropdown.classList.toggle('show');
}

// Closes all dropdowns if clicked outside
window.onclick = function(event) {
    if (!event.target.matches('.btn-secondary')) {
        document.querySelectorAll('.dropdown-content').forEach((dropdown) => {
            dropdown.classList.remove('show');
        });
    }
};

// Updates the text box with selected absentees
function updateAbsentees(year) {
    const checkboxes = document.querySelectorAll(`input[name="${year}_absentees[]"]:checked`);
    const selectedNames = Array.from(checkboxes).map(cb => cb.value);
    document.getElementById(`${year}_absent_names`).value = selectedNames.join(', ');
}

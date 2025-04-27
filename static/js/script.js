function updatePresent(row) {
    let total = parseInt(document.getElementById('total' + row).textContent);  // Ensure the total is a number
    let absent = parseInt(document.getElementById('absent' + row).value) || 0;  // Default to 0 if absent is empty or not a number
    let present = total - absent;

    // Ensure that present is not negative (if absent is larger than total, it should be set to 0)
    present = present < 0 ? 0 : present;

    document.getElementById('present' + row).textContent = present;
}

function updateAbsentees(year) {
    let selectedNames = [];
    let checkboxes = document.querySelectorAll(`input[name='${year}_absentees[]']:checked`);
    checkboxes.forEach(function(checkbox) {
        selectedNames.push(checkbox.value);
    });
    document.getElementById(`${year}_absent_names`).value = selectedNames.join(", ");
}
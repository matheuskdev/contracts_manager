document.addEventListener('DOMContentLoaded', function () {
    const changePdfCheckbox = document.querySelector('input[name="change_pdf"]');
    const pdfFieldContainer = document.querySelector('.field-pdf');  // Ajuste o seletor conforme necessário
    const startDateField = document.querySelector('input[name="start_date"]');
    const endDateField = document.querySelector('input[name="end_date"]');

    function togglePdfField() {
        if (changePdfCheckbox && pdfFieldContainer) {
            if (changePdfCheckbox.checked) {
                pdfFieldContainer.style.display = 'block';
            } else {
                pdfFieldContainer.style.display = 'none';
            }
        }
    }

  
});
// admin_contract.js

document.addEventListener('DOMContentLoaded', function() {
    const startDateField = document.querySelector('#id_start_date');
    const endDateField = document.querySelector('#id_end_date');

    if (startDateField) {
        startDateField.addEventListener('change', function() {
            let dateValue = startDateField.value;
            if (dateValue) {
                let [day, month, year] = dateValue.split('/');
                if (day && month && year) {
                    startDateField.value = `${year}-${month}-${day}`;
                }
            }
        });
    }

    if (endDateField) {
        endDateField.addEventListener('change', function() {
            let dateValue = endDateField.value;
            if (dateValue) {
                let [day, month, year] = dateValue.split('/');
                if (day && month && year) {
                    endDateField.value = `${year}-${month}-${day}`;
                }
            }
        });
    }
});

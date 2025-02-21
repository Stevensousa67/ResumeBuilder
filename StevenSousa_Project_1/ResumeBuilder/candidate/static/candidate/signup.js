document.addEventListener('DOMContentLoaded', () => {
    // Function to update the total number of forms
    function updateTotalForms(prefix) {
        let totalForms = document.getElementById(`id_${prefix}-TOTAL_FORMS`);
        let formCount = parseInt(totalForms.value);
        totalForms.value = formCount + 1;
    }

    // Function to add a new form
    function addForm(prefix, emptyFormSelector, formContainerSelector) {
        let totalForms = document.getElementById(`id_${prefix}-TOTAL_FORMS`);
        let formIdx = parseInt(totalForms.value);
        let emptyForm = document.querySelector(emptyFormSelector);
        let newForm = emptyForm.cloneNode(true);
        
        newForm.classList.remove('hidden-form');
        newForm.classList.add('experience-form'); // Ensure the class is added for new forms
        newForm.style.display = 'block';

        const inputs = newForm.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            let oldName = input.getAttribute('name');
            if (oldName) {
                // Replace __prefix__ with the current index for Django formsets
                let newName = oldName.replace('__prefix__', formIdx);
                let newId = `id_${newName}`;
                input.setAttribute('name', newName);
                input.setAttribute('id', newId);
                input.value = '';
                if (input.type === 'checkbox') input.checked = false;
                console.log(`Renamed ${oldName} to ${newName} with ID ${newId}`);
            }
        });

        document.querySelector(formContainerSelector).appendChild(newForm);
        updateTotalForms(prefix);

        // Reset Present checkbox and apply end_date logic for new form
        const presentCheckbox = newForm.querySelector("input[name^='experiences'][name$='-present']");
        const endDateInput = newForm.querySelector("input[name^='experiences'][name$='-end_date']");
        console.log('New Form Added - Present Checkbox:', presentCheckbox, 'End Date Input:', endDateInput);
        if (presentCheckbox) presentCheckbox.checked = false; // Start with unchecked
        if (endDateInput) endDateInput.disabled = false; // Enable end_date by default

        // Ensure the new form’s toggle works
        toggleEndDateField(newForm);
    }

    // Toggle the end_date field based on the "Present" checkbox state
    function toggleEndDateField(form) {
        const presentCheckbox = form.querySelector("input[name^='experiences'][name$='-present']");
        const endDateInput = form.querySelector("input[name^='experiences'][name$='-end_date']");

        console.log('Toggling for Form:', form);
        console.log('Present Checkbox Found:', presentCheckbox);
        console.log('End Date Input Found:', endDateInput);

        if (!presentCheckbox) {
            console.error('Present checkbox not found in form:', form);
            return;
        }
        if (!endDateInput) {
            console.error('End date input not found in form:', form);
            return;
        }

        // If "Present" is checked, disable the end_date input
        endDateInput.disabled = presentCheckbox.checked;
        console.log(`Set ${endDateInput.name}.disabled = ${endDateInput.disabled}`);
    }

    // Listen to changes in the "Present" checkbox
    document.addEventListener('change', event => {
        if (event.target.matches("input[name^='experiences'][name$='-present']")) {
            console.log('Checkbox Changed - Target:', event.target, 'Name:', event.target.name, 'Checked:', event.target.checked);
            const form = event.target.closest('.experience-form');
            if (!form) {
                console.error('No .experience-form found for:', event.target);
                return;
            }
            toggleEndDateField(form);
        }
    });

    // Initially, ensure the correct state is applied to all existing experience forms
    document.querySelectorAll('.experience-form').forEach(form => {
        console.log('Initializing Form:', form);
        toggleEndDateField(form);
    });

    // Add experience, project, course, and reference forms
    document.getElementById('add-experience').addEventListener('click', () => {
        addForm('experiences', '#empty-experience-form', '#experience-forms');
    });

    document.getElementById('add-project').addEventListener('click', () => {
        addForm('projects', '#empty-project-form', '#project-forms');
    });

    document.getElementById('add-course').addEventListener('click', () => {
        addForm('courses', '#empty-course-form', '#course-forms');
    });

    document.getElementById('add-reference').addEventListener('click', () => {
        addForm('references', '#empty-reference-form', '#reference-forms');
    });
});
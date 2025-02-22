document.addEventListener('DOMContentLoaded', () => {
    function getNextIndex(prefix) {
        const existingForms = document.querySelectorAll(`.${prefix}-form:not(#empty-${prefix}-form)`);
        let maxIndex = -1;
        console.log(`Checking active forms for ${prefix}:`, existingForms);

        existingForms.forEach(form => {
            const inputs = form.querySelectorAll('[name]');
            console.log(`Form inputs for ${prefix}:`, inputs);
            inputs.forEach(input => {
                console.log(`Input name: ${input.name}`);
                const match = input.name.match(new RegExp(`${prefix}-(\\d+)-`));
                if (match) {
                    const index = parseInt(match[1]);
                    console.log(`Found index ${index} in ${input.name}`);
                    if (index > maxIndex) maxIndex = index;
                }
            });
        });

        console.log(`Max index for ${prefix}: ${maxIndex}`);
        return maxIndex + 1; // Next available index
    }

    function updateTotalForms(prefix, count) {
        let totalForms = document.getElementById(`id_${prefix}-TOTAL_FORMS`);
        totalForms.value = count;
        console.log(`Updated ${prefix}-TOTAL_FORMS to ${count}`);
    }

    function addForm(prefix, emptyFormSelector, formContainerSelector) {
        let formIdx = getNextIndex(prefix);
        console.log(`Adding ${prefix} form with index ${formIdx}`);

        let emptyForm = document.querySelector(emptyFormSelector);
        let newForm = emptyForm.cloneNode(true);

        newForm.classList.remove('hidden-form');
        newForm.classList.add(`${prefix}-form`);
        newForm.style.display = 'block';
        newForm.removeAttribute('id'); // Remove the ID to avoid duplicate IDs

        // Update names and IDs with the new index
        newForm.querySelectorAll('[name], [id]').forEach(element => {
            if (element.name) {
                element.setAttribute('name', element.name.replace('__prefix__', formIdx));
            }
            if (element.id) {
                element.setAttribute('id', element.id.replace('__prefix__', formIdx));
            }
        });

        // Reset values for the new form
        newForm.querySelectorAll('input, select, textarea').forEach(input => {
            input.value = '';
            if (input.type === 'checkbox') input.checked = false;
        });

        // Append the new form to the container
        const container = document.querySelector(formContainerSelector);
        container.appendChild(newForm);

        // Update TOTAL_FORMS based on actual active forms (excluding template)
        const totalForms = document.querySelectorAll(`.${prefix}-form:not(#empty-${prefix}-form)`).length;
        updateTotalForms(prefix, totalForms);

        // For experience forms, reset and apply end_date logic
        if (prefix === 'experiences') {
            toggleEndDateField(newForm);
        }
    }

    function toggleEndDateField(form) {
        const presentCheckbox = form.querySelector("input[name^='experiences'][name$='-present']");
        const endDateInput = form.querySelector("input[name^='experiences'][name$='-end_date']");

        if (!presentCheckbox || !endDateInput) return;

        endDateInput.disabled = presentCheckbox.checked;
    }

    document.addEventListener('change', event => {
        if (event.target.matches("input[name^='experiences'][name$='-present']")) {
            const form = event.target.closest('.experiences-form');
            if (!form) return;
            toggleEndDateField(form);
        }
    });

    // Initialize existing forms
    document.querySelectorAll('.experiences-form').forEach(form => {
        toggleEndDateField(form);
    });

    document.getElementById('add-experience').addEventListener('click', () => {
        addForm('experiences', '#empty-experience-form', '#experience-forms');
    });

    document.getElementById('add-project').addEventListener('click', () => {
        addForm('projects', '#empty-project-form', '#project-forms');
    });

    document.getElementById('add-reference').addEventListener('click', () => {
        addForm('references', '#empty-reference-form', '#reference-forms');
    });
});
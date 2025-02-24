document.addEventListener('DOMContentLoaded', () => {
    function getNextIndex(prefix) {
        const existingForms = document.querySelectorAll(`.${prefix}-form:not(#empty-${prefix}-form)`);
        let maxIndex = -1;
        console.log(`Checking active forms for ${prefix}:`, existingForms);

        existingForms.forEach(form => {
            const inputs = form.querySelectorAll('[name]');
            inputs.forEach(input => {
                const match = input.name.match(new RegExp(`${prefix}-(\\d+)-`));
                if (match) {
                    const index = parseInt(match[1]);
                    if (index > maxIndex) maxIndex = index;
                }
            });
        });

        console.log(`Max index for ${prefix}: ${maxIndex}`);
        return maxIndex + 1;
    }

    function updateTotalForms(prefix, count) {
        let totalForms = document.getElementById(`id_${prefix}-TOTAL_FORMS`);
        if (totalForms) {
            totalForms.value = count;
            console.log(`Updated ${prefix}-TOTAL_FORMS to ${count}`);
        }
    }

    function addForm(prefix, emptyFormSelector, formContainerSelector) {
        let formIdx = getNextIndex(prefix);
        console.log(`Adding ${prefix} form with index ${formIdx}`);

        let emptyForm = document.querySelector(emptyFormSelector);
        if (!emptyForm) {
            console.error(`Empty form not found: ${emptyFormSelector}`);
            return;
        }
        let newForm = emptyForm.cloneNode(true);

        newForm.classList.remove('hidden-form');
        newForm.classList.add(`${prefix}-form`);
        newForm.style.display = 'block';
        newForm.removeAttribute('id');

        newForm.querySelectorAll('[name], [id]').forEach(element => {
            if (element.name) {
                element.setAttribute('name', element.name.replace('__prefix__', formIdx));
            }
            if (element.id) {
                element.setAttribute('id', element.id.replace('__prefix__', formIdx));
            }
        });

        newForm.querySelectorAll('input, select, textarea').forEach(input => {
            input.value = '';
            if (input.type === 'checkbox') input.checked = false;
        });

        const container = document.querySelector(formContainerSelector);
        if (!container) {
            console.error(`Container not found: ${formContainerSelector}`);
            return;
        }
        container.appendChild(newForm);
        console.log(`Appended new ${prefix} form`, newForm);

        const totalForms = document.querySelectorAll(`.${prefix}-form:not(#empty-${prefix}-form)`).length;
        updateTotalForms(prefix, totalForms);

        if (prefix === 'experiences') {
            toggleEndDateField(newForm);
        }
    }

    function toggleEndDateField(form) {
        const presentCheckbox = form.querySelector("input[name^='experiences'][name$='-present']");
        const endDateInput = form.querySelector("input[name^='experiences'][name$='-end_date']");
        if (presentCheckbox && endDateInput) {
            endDateInput.disabled = presentCheckbox.checked;
        }
    }

    document.addEventListener('change', event => {
        if (event.target.matches("input[name^='experiences'][name$='-present']")) {
            const form = event.target.closest('.experiences-form');
            if (form) toggleEndDateField(form);
        }
    });

    document.querySelectorAll('.experiences-form').forEach(form => {
        toggleEndDateField(form);
    });

    function bindAddButtons() {
        const addButtons = {
            'experiences': document.getElementById('add-experience'),
            'projects': document.getElementById('add-project'),
            'references': document.getElementById('add-reference')
        };

        Object.entries(addButtons).forEach(([prefix, button]) => {
            if (button && !button.dataset.listenerAdded) {
                button.addEventListener('click', (e) => {
                    e.preventDefault();
                    addForm(prefix, `#empty-${prefix}-form`, `#${prefix}-forms`);
                });
                button.dataset.listenerAdded = 'true';
                console.log(`Added listener for ${prefix} button`);
            } else if (!button) {
                console.log(`No ${prefix} button found on this step`);
            }
        });
    }

    bindAddButtons();
    document.getElementById('signup-form').addEventListener('submit', () => {
        setTimeout(bindAddButtons, 100);
    });
});
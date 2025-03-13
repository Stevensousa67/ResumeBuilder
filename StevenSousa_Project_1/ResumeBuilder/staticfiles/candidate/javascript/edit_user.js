document.addEventListener('DOMContentLoaded', () => {
    console.log('Current step:', window.currentStep);

    if (window.currentStep === 'profile_select') {
        const radioButtons = document.querySelectorAll('input[name="profile_select-profile_option"]');
        console.log('Radio buttons found:', radioButtons);  // Debug
        console.log('Radio buttons count:', radioButtons.length);  // Debug
        console.log('First radio button:', radioButtons[0]);  // Debug

        const existingContainer = document.getElementById('existing-profile-container');
        const newContainer = document.getElementById('new-profile-container');
        console.log('Containers:', {existingContainer, newContainer});  // Debug

        if (radioButtons.length === 0) {
            console.error("No profile selection radio buttons found. Checking broader selector...");
            const allRadios = document.querySelectorAll('input[type="radio"]');
            console.log('All radio inputs:', allRadios);  // Debug
            return;
        }
        if (!existingContainer || !newContainer) {
            console.error("Profile containers missing.");
            return;
        }

        console.log("Initial state:", {
            existingContainer: existingContainer.style.display,
            newContainer: newContainer.style.display,
            selected: document.querySelector('input[name="profile_select-profile_option"]:checked')?.value
        });

        function toggleProfileSelection() {
            const selectedValue = document.querySelector('input[name="profile_select-profile_option"]:checked')?.value;
            console.log("Radio changed:", selectedValue);

            if (selectedValue === 'new') {
                newContainer.style.display = 'block';
                existingContainer.style.display = 'none';
            } else {
                newContainer.style.display = 'none';
                existingContainer.style.display = 'block';
            }
        }

        toggleProfileSelection();
        radioButtons.forEach(radio => {
            radio.addEventListener('change', toggleProfileSelection);
        });
    }

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

    if (window.currentStep === 'experience') {
        document.addEventListener('change', event => {
            if (event.target.matches("input[name^='experiences'][name$='-present']")) {
                const form = event.target.closest('.experiences-form');
                if (form) toggleEndDateField(form);
            }
        });

        document.querySelectorAll('.experiences-form').forEach(form => {
            toggleEndDateField(form);
        });
    }

    function bindAddButtons() {
        const addButtons = {};

        if (window.currentStep === 'experience') {
            addButtons['experiences'] = document.getElementById('add-experience');
        } else if (window.currentStep === 'projects') {
            addButtons['projects'] = document.getElementById('add-project');
        } else if (window.currentStep === 'references') {
            addButtons['references'] = document.getElementById('add-reference');
        }

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

    const editUserForm = document.getElementById('edit-user-form');
    if (editUserForm) {
        editUserForm.addEventListener('submit', () => {
            setTimeout(bindAddButtons, 100);
        });
    } else {
        console.error('edit-user-form not found');
    }
});
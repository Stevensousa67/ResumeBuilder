// candidate/static/candidate/js/signup.js
document.addEventListener('DOMContentLoaded', function() {
    // Add more reference forms
    document.getElementById('add-reference').addEventListener('click', function() {
        const formset = document.getElementById('reference-forms');
        const totalForms = document.querySelector('#id_references-TOTAL_FORMS');
        const formCount = parseInt(totalForms.value);
        const newForm = formset.children[0].cloneNode(true);
        newForm.innerHTML = newForm.innerHTML.replace(/references-\d+/g, `references-${formCount}`);
        newForm.querySelectorAll('input, textarea, select').forEach(input => input.value = '');
        formset.appendChild(newForm);
        totalForms.value = formCount + 1;
        updateFormCounts();
    });

    // Add more project forms
    document.getElementById('add-project').addEventListener('click', function() {
        const formset = document.getElementById('project-forms');
        const totalForms = document.querySelector('#id_projects-TOTAL_FORMS');
        const formCount = parseInt(totalForms.value);
        const newForm = formset.children[0].cloneNode(true);
        newForm.innerHTML = newForm.innerHTML.replace(/projects-\d+/g, `projects-${formCount}`);
        newForm.querySelectorAll('input, textarea, select').forEach(input => input.value = '');
        formset.appendChild(newForm);
        totalForms.value = formCount + 1;
        updateFormCounts();
    });

    // Add more experience forms
    document.getElementById('add-experience').addEventListener('click', function() {
        const formset = document.getElementById('experience-forms');
        const totalForms = document.querySelector('#id_experiences-TOTAL_FORMS');
        const formCount = parseInt(totalForms.value);
        const newForm = formset.children[0].cloneNode(true);
        newForm.innerHTML = newForm.innerHTML.replace(/experiences-\d+/g, `experiences-${formCount}`);
        newForm.querySelectorAll('input, textarea, select').forEach(input => input.value = '');
        formset.appendChild(newForm);
        totalForms.value = formCount + 1;
        updateFormCounts();
    });

    // Add more classes forms
    document.getElementById('add-classes').addEventListener('click', function() {
        const formset = document.getElementById('classes-forms');
        const totalForms = document.querySelector('#id_classes-TOTAL_FORMS');
        const formCount = parseInt(totalForms.value);
        const newForm = formset.children[0].cloneNode(true);
        newForm.innerHTML = newForm.innerHTML.replace(/classes-\d+/g, `classes-${formCount}`);
        newForm.querySelectorAll('input, textarea, select').forEach(input => input.value = '');
        formset.appendChild(newForm);
        totalForms.value = formCount + 1;
        updateFormCounts();
    });

    function removeForm(button) {
        button.parentElement.remove();
        updateFormCounts();
    }

    function updateFormCounts() {
        ['references', 'projects', 'experiences', 'classes'].forEach(prefix => {
            const forms = document.querySelectorAll(`#${prefix}-forms .${prefix}-form`);
            const totalForms = document.querySelector(`#id_${prefix}-TOTAL_FORMS`);
            if (totalForms) totalForms.value = forms.length;
        });
    }
});
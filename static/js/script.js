document.addEventListener('DOMContentLoaded', function() {
    const namesContainer = document.getElementById('names-container');
    const addNameBtn = document.getElementById('add-name-btn');
    const savePlayerListForm = document.getElementById('save-player-list-form');
    const namesForSavingContainer = document.getElementById('names-for-saving-container');
    const generateGroupsForm = document.getElementById('generate-groups-form');
    const groupTypeSelect = document.getElementById('group-type');
    const numGroupsInputDiv = document.getElementById('num-groups-input');
    const groupSizeInputDiv = document.getElementById('group-size-input');
    const numGroupsInput = document.getElementById('num-groups');
    const groupSizeInput = document.getElementById('group-size');

    function addNameField(nameValue = '') {
        const wrapper = document.createElement('div');
        wrapper.classList.add('name-input-wrapper');

        const newInput = document.createElement('input');
        newInput.type = 'text';
        newInput.name = 'name[]';
        newInput.placeholder = 'Name der Person';
        newInput.value = nameValue;
        newInput.required = true;

        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.classList.add('remove-name-btn');
        removeBtn.setAttribute('aria-label', 'Namenfeld entfernen');
        removeBtn.innerHTML = '&times;';

        removeBtn.addEventListener('click', function() {
            if (namesContainer.querySelectorAll('.name-input-wrapper').length > 1) {
                wrapper.remove();
                updateSaveButtonState();
            } else {
                newInput.value = '';
            }
        });

        wrapper.appendChild(newInput);
        wrapper.appendChild(removeBtn);
        namesContainer.appendChild(wrapper);
        newInput.focus();
        updateSaveButtonState();
    }

    function updateSaveButtonState() {
        const saveButton = savePlayerListForm ? savePlayerListForm.querySelector('.save-btn') : null;
        if (saveButton) {
            const hasNames = Array.from(namesContainer.querySelectorAll('input[name="name[]"]')).some(input => input.value.trim() !== '');
            saveButton.disabled = !hasNames;
        }
    }

    if (addNameBtn) {
        addNameBtn.addEventListener('click', function() {
            addNameField();
        });
    }

    namesContainer.addEventListener('click', function(event) {
        if (event.target.classList.contains('remove-name-btn')) {
            const wrapper = event.target.closest('.name-input-wrapper');
            if (wrapper) {
                if (namesContainer.querySelectorAll('.name-input-wrapper').length > 1) {
                    wrapper.remove();
                    updateSaveButtonState();
                } else {
                    wrapper.querySelector('input[name="name[]"]').value = '';
                    updateSaveButtonState();
                }
            }
        }
    });

    if (namesContainer && namesContainer.querySelectorAll('input[name="name[]"]').length === 0) {
        addNameField();
    } else if (namesContainer) {
        const allNameInputs = Array.from(namesContainer.querySelectorAll('input[name="name[]"]'));
        let focused = false;
        if (allNameInputs.length > 0) {
            const lastInput = allNameInputs[allNameInputs.length - 1];
            if (lastInput.value.trim() === '') {
                lastInput.focus();
                focused = true;
            } else {
                for (const input of allNameInputs) {
                    if (input.value.trim() === '') {
                        input.focus();
                        focused = true;
                        break;
                    }
                }
            }
        }
        if (!focused && namesContainer.querySelectorAll('input[name="name[]"]').length > 0) {
            addNameField();
        }
    }

    if (groupTypeSelect && numGroupsInputDiv && groupSizeInputDiv) {
        function toggleGroupInputs() {
            if (groupTypeSelect.value === 'num_groups') {
                numGroupsInputDiv.style.display = 'block';
                groupSizeInputDiv.style.display = 'none';
                numGroupsInput.setAttribute('required', 'true');
                groupSizeInput.removeAttribute('required');
            } else if (groupTypeSelect.value === 'group_size') {
                numGroupsInputDiv.style.display = 'none';
                groupSizeInputDiv.style.display = 'block';
                numGroupsInput.removeAttribute('required');
                groupSizeInput.setAttribute('required', 'true');
            } else {
                numGroupsInputDiv.style.display = 'none';
                groupSizeInputDiv.style.display = 'none';
                numGroupsInput.removeAttribute('required');
                groupSizeInput.removeAttribute('required');
            }
        }

        groupTypeSelect.addEventListener('change', toggleGroupInputs);
        toggleGroupInputs();
    }

    if (savePlayerListForm && namesContainer && namesForSavingContainer) {
        savePlayerListForm.addEventListener('submit', function(event) {
            namesForSavingContainer.innerHTML = '';
            const nameInputs = namesContainer.querySelectorAll('input[name="name[]"]');
            nameInputs.forEach(input => {
                if (input.value.trim() !== '') {
                    const hiddenInput = document.createElement('input');
                    hiddenInput.type = 'hidden';
                    hiddenInput.name = 'names[]';
                    hiddenInput.value = input.value.trim();
                    namesForSavingContainer.appendChild(hiddenInput);
                }
            });
            if (namesForSavingContainer.children.length === 0) {
                alert('Bitte gib mindestens einen Namen ein, um die Liste zu speichern.');
                event.preventDefault();
            }
        });
    }

    if (namesContainer && generateGroupsForm) {
        namesContainer.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                const target = event.target;
                if (target.matches('input[name="name[]"]')) {
                    const allNameInputs = Array.from(namesContainer.querySelectorAll('input[name="name[]"]'));
                    const currentIndex = allNameInputs.indexOf(target);
                    const currentInputValue = target.value.trim();

                    if (currentIndex === allNameInputs.length - 1 && currentInputValue !== '') {
                        addNameField();
                    } else if (currentInputValue === '' || (currentIndex === allNameInputs.length - 1 && currentInputValue === '')) {
                        generateGroupsForm.submit();
                    } else if (currentIndex < allNameInputs.length - 1 && currentInputValue !== '') {
                        const nextInput = allNameInputs[currentIndex + 1];
                        if (nextInput) {
                            nextInput.focus();
                        }
                    }
                }
            }
        });
    }
    updateSaveButtonState();
});
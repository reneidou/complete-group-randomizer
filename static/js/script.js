document.addEventListener('DOMContentLoaded', function() {
    // Grundlegende Elemente
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
    
    // Erweiterte Elemente
    const modeRadios = document.querySelectorAll('input[name="mode"]');
    const sportSelection = document.getElementById('sport-selection');
    const toggleAdvanced = document.getElementById('toggle-advanced');
    const advancedOptions = document.getElementById('advanced-options');
    const minRatingInput = document.getElementById('min-rating');
    const maxRatingInput = document.getElementById('max-rating');
    const ratingDirection = document.getElementById('rating-direction');
    const addRoleBtn = document.getElementById('add-role-btn');
    const rolesContainer = document.getElementById('roles-container');
    const addPreferenceBtn = document.getElementById('add-preference-btn');
    const preferencesContainer = document.getElementById('preferences-container');

    // Funktion zum Hinzufügen eines Namensfeldes
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
                updateRatingInputs();
                updatePreferenceOptions();
            } else {
                newInput.value = '';
            }
        });

        wrapper.appendChild(newInput);
        wrapper.appendChild(removeBtn);
        namesContainer.appendChild(wrapper);
        newInput.focus();
        updateSaveButtonState();
        updateRatingInputs();
        updatePreferenceOptions();
    }

    // Save-Button Status aktualisieren
    function updateSaveButtonState() {
        const saveButton = savePlayerListForm ? savePlayerListForm.querySelector('.save-btn') : null;
        if (saveButton) {
            const hasNames = Array.from(namesContainer.querySelectorAll('input[name="name[]"]')).some(input => input.value.trim() !== '');
            saveButton.disabled = !hasNames;
        }
    }

    // Modus- und Sportart-Auswahl
    if (modeRadios) {
        modeRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.value === 'sport' && sportSelection) {
                    sportSelection.style.display = 'block';
                } else if (sportSelection) {
                    sportSelection.style.display = 'none';
                }
            });
        });
    }

    // Erweiterte Optionen ein-/ausblenden
    if (toggleAdvanced && advancedOptions) {
        toggleAdvanced.addEventListener('click', function() {
            if (advancedOptions.style.display === 'none') {
                advancedOptions.style.display = 'block';
                this.textContent = 'Erweiterte Optionen ausblenden';
                initAdvancedOptions();
            } else {
                advancedOptions.style.display = 'none';
                this.textContent = 'Erweiterte Optionen anzeigen';
            }
        });
    }

    // Bewertungsfelder aktualisieren
    function updateRatingInputs() {
        if (!minRatingInput || !maxRatingInput || !ratingDirection) return;
        
        const minRating = parseFloat(minRatingInput.value) || 1;
        const maxRating = parseFloat(maxRatingInput.value) || 5;
        const dir = ratingDirection.value;
        
        const ratingContainer = document.getElementById('rating-container');
        if (!ratingContainer) return;
        
        ratingContainer.innerHTML = '';
        
        const nameInputs = namesContainer.querySelectorAll('input[name="name[]"]');
        nameInputs.forEach(input => {
            if (input.value.trim() !== '') {
                const wrapper = document.createElement('div');
                wrapper.classList.add('rating-input-wrapper');
                
                const label = document.createElement('label');
                label.textContent = input.value;
                label.style.display = 'block';
                label.style.marginBottom = '5px';
                
                const ratingInput = document.createElement('input');
                ratingInput.type = 'number';
                ratingInput.name = `rating_${input.value}`;
                ratingInput.min = minRating;
                ratingInput.max = maxRating;
                ratingInput.step = '0.1';
                ratingInput.value = (minRating + maxRating) / 2;
                ratingInput.style.width = '100px';
                
                wrapper.appendChild(label);
                wrapper.appendChild(ratingInput);
                ratingContainer.appendChild(wrapper);
            }
        });
    }

    // Rollen hinzufügen
    function addRoleField() {
        if (!rolesContainer) return;
        
        const roleEntry = document.createElement('div');
        roleEntry.classList.add('role-entry');
        roleEntry.innerHTML = `
            <input type="text" placeholder="Rollenname" class="role-name" style="width: 150px;">
            <input type="number" placeholder="Min" min="0" class="role-min" style="width: 60px;">
            <input type="number" placeholder="Max" min="0" class="role-max" style="width: 60px;">
            <button type="button" class="button-x-small remove-role">&times;</button>
        `;
        rolesContainer.appendChild(roleEntry);
    }

    // Präferenzen hinzufügen
    function addPreferenceField() {
        if (!preferencesContainer) return;
        
        const playerOptions = Array.from(namesContainer.querySelectorAll('input[name="name[]"]'))
            .filter(input => input.value.trim() !== '')
            .map(input => `<option value="${input.value}">${input.value}</option>`)
            .join('');
        
        const preferenceEntry = document.createElement('div');
        preferenceEntry.classList.add('preference-entry');
        preferenceEntry.innerHTML = `
            <select class="preference-player" style="margin-right: 10px;">
                <option value="">Spieler wählen</option>
                ${playerOptions}
            </select>
            <select class="preference-type" style="margin-right: 10px;">
                <option value="must">muss mit</option>
                <option value="avoid">darf nicht mit</option>
            </select>
            <select class="preference-target">
                <option value="">Zielspieler wählen</option>
                ${playerOptions}
            </select>
            <button type="button" class="button-x-small remove-preference">&times;</button>
        `;
        preferencesContainer.appendChild(preferenceEntry);
    }

    // Präferenzoptionen aktualisieren
    function updatePreferenceOptions() {
        const playerOptions = Array.from(namesContainer.querySelectorAll('input[name="name[]"]'))
            .filter(input => input.value.trim() !== '')
            .map(input => `<option value="${input.value}">${input.value}</option>`)
            .join('');
        
        document.querySelectorAll('.preference-player, .preference-target').forEach(select => {
            const currentValue = select.value;
            select.innerHTML = `<option value="">Spieler wählen</option>${playerOptions}`;
            select.value = currentValue;
        });
    }

    // Erweiterte Optionen initialisieren
    function initAdvancedOptions() {
        updateRatingInputs();
        updatePreferenceOptions();
        
        // Event-Listener für Rollen und Präferenzen
        if (minRatingInput && maxRatingInput && ratingDirection) {
            minRatingInput.addEventListener('change', updateRatingInputs);
            maxRatingInput.addEventListener('change', updateRatingInputs);
            ratingDirection.addEventListener('change', updateRatingInputs);
        }
        
        if (addRoleBtn) {
            addRoleBtn.addEventListener('click', addRoleField);
        }
        
        if (addPreferenceBtn) {
            addPreferenceBtn.addEventListener('click', addPreferenceField);
        }
        
        // Entfernen-Buttons
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('remove-role')) {
                e.target.closest('.role-entry').remove();
            }
            if (e.target.classList.contains('remove-preference')) {
                e.target.closest('.preference-entry').remove();
            }
        });
    }

    // Gruppenoptionen anzeigen/verstecken
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

    // Namensliste für das Speichern vorbereiten
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

    // Enter-Tasten-Verhalten in Namensfeldern
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

    // Initialisierung
    if (namesContainer && namesContainer.querySelectorAll('input[name="name[]"]').length === 0) {
        addNameField();
    } else if (namesContainer) {
        updateSaveButtonState();
        updateRatingInputs();
        updatePreferenceOptions();
    }
    
    // Sportart-Auswahl initialisieren
    if (modeRadios && sportSelection) {
        modeRadios.forEach(radio => {
            if (radio.checked && radio.value === 'sport') {
                sportSelection.style.display = 'block';
            }
        });
    }
});
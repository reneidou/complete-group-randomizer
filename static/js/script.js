document.addEventListener('DOMContentLoaded', function() {
    const namesContainer = document.getElementById('names-container');
    const addNameBtn = document.getElementById('add-name-btn');
    const savePlayerListForm = document.getElementById('save-player-list-form');
    const namesForSavingContainer = document.getElementById('names-for-saving-container');
    const generateGroupsForm = document.getElementById('generate-groups-form'); // Das Hauptformular für die Generierung

    // Elemente für Gruppenoptionen (falls vorhanden)
    const groupTypeSelect = document.getElementById('group-type');
    const numGroupsInputDiv = document.getElementById('num-groups-input');
    const groupSizeInputDiv = document.getElementById('group-size-input');
    const numGroupsInput = document.getElementById('num-groups');
    const groupSizeInput = document.getElementById('group-size');

    // Funktion zum Hinzufügen eines neuen Namensfeldes
    function addNameField(nameValue = '') {
        const wrapper = document.createElement('div');
        wrapper.classList.add('name-input-wrapper');

        const newInput = document.createElement('input');
        newInput.type = 'text';
        newInput.name = 'name[]'; // Wichtig für Flask, um eine Liste zu erhalten
        newInput.placeholder = 'Name der Person';
        newInput.value = nameValue;
        newInput.required = true; // Namesfelder sind jetzt immer required

        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.classList.add('remove-name-btn');
        removeBtn.setAttribute('aria-label', 'Namenfeld entfernen');
        removeBtn.innerHTML = '&times;'; // HTML-Entität für ein 'x'

        removeBtn.addEventListener('click', function() {
            if (namesContainer.querySelectorAll('.name-input-wrapper').length > 1) {
                // Nur löschen, wenn mehr als ein Feld vorhanden ist
                wrapper.remove();
                updateSaveButtonState(); // Aktualisiere den Zustand des Speicher-Buttons
            } else {
                // Wenn es das letzte Feld ist, leere es einfach
                newInput.value = '';
            }
        });

        wrapper.appendChild(newInput);
        wrapper.appendChild(removeBtn);
        namesContainer.appendChild(wrapper);

        // Setze den Fokus auf das neu hinzugefügte Feld
        newInput.focus();

        updateSaveButtonState(); // Aktualisiere den Zustand des Speicher-Buttons
    }

    // Funktion zur Aktualisierung des Save-Buttons-Zustands
    // Der Save-Button sollte nur aktiv sein, wenn mindestens ein Name eingegeben wurde.
    function updateSaveButtonState() {
        const saveButton = savePlayerListForm ? savePlayerListForm.querySelector('.save-btn') : null;
        if (saveButton) {
            const hasNames = Array.from(namesContainer.querySelectorAll('input[name="name[]"]')).some(input => input.value.trim() !== '');
            saveButton.disabled = !hasNames;
        }
    }


    // Event Listener für "Namen hinzufügen" Button
    if (addNameBtn) {
        addNameBtn.addEventListener('click', function() {
            addNameField();
        });
    }

    // Event Listener für "Namenfeld entfernen" Buttons (für initial geladene Felder)
    namesContainer.addEventListener('click', function(event) {
        if (event.target.classList.contains('remove-name-btn')) {
            const wrapper = event.target.closest('.name-input-wrapper');
            if (wrapper) {
                if (namesContainer.querySelectorAll('.name-input-wrapper').length > 1) {
                    wrapper.remove();
                    updateSaveButtonState();
                } else {
                    // Wenn es das letzte Feld ist, leere es einfach
                    wrapper.querySelector('input[name="name[]"]').value = '';
                    updateSaveButtonState();
                }
            }
        }
    });


    // Initialisiere die Namesfelder beim Laden der Seite
    // Wenn keine Namen geladen wurden (z.B. bei einem Neuladen ohne Daten), füge ein Startfeld hinzu
    if (namesContainer && namesContainer.querySelectorAll('input[name="name[]"]').length === 0) {
        addNameField();
    } else if (namesContainer) {
        // Falls Namen geladen wurden, stelle sicher, dass der remove-button funktioniert
        // und fokussiere das letzte Feld (falls leer) oder das erste leere Feld
        const allNameInputs = Array.from(namesContainer.querySelectorAll('input[name="name[]"]'));
        let focused = false;
        if (allNameInputs.length > 0) {
            const lastInput = allNameInputs[allNameInputs.length - 1];
            if (lastInput.value.trim() === '') {
                lastInput.focus();
                focused = true;
            } else {
                // Finde das erste leere Feld und fokussiere es
                for (const input of allNameInputs) {
                    if (input.value.trim() === '') {
                        input.focus();
                        focused = true;
                        break;
                    }
                }
            }
        }
        // Wenn kein Feld leer ist und Namen geladen wurden, füge ein neues leeres Feld hinzu und fokussiere es
        if (!focused && namesContainer.querySelectorAll('input[name="name[]"]').length > 0) {
            addNameField();
        }
    }

    // Logik für die Anzeige von Gruppenanzahl oder Gruppengröße
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
                // Standard: Beide ausblenden oder nur eins anzeigen, je nach Präferenz
                numGroupsInputDiv.style.display = 'none';
                groupSizeInputDiv.style.display = 'none';
                numGroupsInput.removeAttribute('required');
                groupSizeInput.removeAttribute('required');
            }
        }

        groupTypeSelect.addEventListener('change', toggleGroupInputs);
        toggleGroupInputs(); // Initialer Aufruf beim Laden der Seite
    }

    // Logic for copying names to the hidden form for saving
    if (savePlayerListForm && namesContainer && namesForSavingContainer) {
        savePlayerListForm.addEventListener('submit', function(event) {
            // Lösche alle vorherigen Input-Felder im namesForSavingContainer
            namesForSavingContainer.innerHTML = '';

            // Füge neue Input-Felder für jeden Namen aus namesContainer hinzu
            const nameInputs = namesContainer.querySelectorAll('input[name="name[]"]');
            nameInputs.forEach(input => {
                // Nur Namen hinzufügen, die nicht leer sind
                if (input.value.trim() !== '') {
                    const hiddenInput = document.createElement('input');
                    hiddenInput.type = 'hidden';
                    hiddenInput.name = 'names[]'; // Ein anderer Name, um Konflikte zu vermeiden
                    hiddenInput.value = input.value.trim();
                    namesForSavingContainer.appendChild(hiddenInput);
                }
            });
            // Verhindere das Absenden, wenn keine Namen zum Speichern vorhanden sind
            if (namesForSavingContainer.children.length === 0) {
                alert('Bitte gib mindestens einen Namen ein, um die Liste zu speichern.');
                event.preventDefault();
            }
        });
    }

    // Enter-Tasten-Verhalten in Namensfeldern
    if (namesContainer && generateGroupsForm) {
        namesContainer.addEventListener('keydown', function(event) {
            // Überprüfen, ob die Enter-Taste (Key 'Enter') gedrückt wurde
            if (event.key === 'Enter') {
                event.preventDefault(); // Verhindere das Standard-Formular-Submit

                const target = event.target;
                // Prüfen, ob das Event von einem Namens-Inputfeld kommt
                if (target.matches('input[name="name[]"]')) {
                    const allNameInputs = Array.from(namesContainer.querySelectorAll('input[name="name[]"]'));
                    const currentIndex = allNameInputs.indexOf(target);
                    const currentInputValue = target.value.trim();

                    // Fall 1: Letztes Namensfeld und nicht leer -> neues Feld hinzufügen
                    if (currentIndex === allNameInputs.length - 1 && currentInputValue !== '') {
                        addNameField();
                    }
                    // Fall 2: Letztes Namensfeld und leer ODER irgendein Feld ist leer -> Gruppen generieren
                    // Leere Felder werden später im Flask-Backend ignoriert (oder sollten es werden)
                    else if (currentInputValue === '' || (currentIndex === allNameInputs.length - 1 && currentInputValue === '')) {
                        generateGroupsForm.submit(); // Sende das Hauptformular ab
                    }
                    // Fall 3: Nicht das letzte Feld und nicht leer -> Fokus auf nächstes Feld
                    else if (currentIndex < allNameInputs.length - 1 && currentInputValue !== '') {
                        const nextInput = allNameInputs[currentIndex + 1];
                        if (nextInput) {
                            nextInput.focus();
                        }
                    }
                }
            }
        });
    }
    updateSaveButtonState(); // Initialer Check beim Laden der Seite
});
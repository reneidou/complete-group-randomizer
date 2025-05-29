document.addEventListener('DOMContentLoaded', function() {
    const namesContainer = document.getElementById('names-container');
    const addNameBtn = document.getElementById('add-name-btn');
    const savePlayerListForm = document.getElementById('save-player-list-form');
    const namesForSavingContainer = document.getElementById('names-for-saving-container');
    const generateGroupsForm = document.getElementById('generate-groups-form'); // Das Hauptformular für die Generierung

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
        newInput.required = true;

        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.classList.add('remove-name-btn');
        removeBtn.setAttribute('aria-label', 'Namenfeld entfernen');
        removeBtn.textContent = 'x';
        removeBtn.addEventListener('click', function() {
            // Sicherstellen, dass immer mindestens ein Namensfeld übrig bleibt
            if (namesContainer.children.length > 1) {
                namesContainer.removeChild(wrapper);
            } else {
                alert("Es muss mindestens ein Namensfeld vorhanden sein.");
            }
        });

        wrapper.appendChild(newInput);
        wrapper.appendChild(removeBtn);
        namesContainer.appendChild(wrapper);

        // Fokus auf das neue Eingabefeld setzen
        newInput.focus();
    }

    // Beim Laden der Seite sicherstellen, dass die remove-Buttons ihre Event Listener haben
    namesContainer.querySelectorAll('.remove-name-btn').forEach(button => {
        button.addEventListener('click', function() {
            if (namesContainer.children.length > 1) {
                namesContainer.removeChild(button.closest('.name-input-wrapper'));
            } else {
                alert("Es muss mindestens ein Namensfeld vorhanden sein.");
            }
        });
    });

    // Event Listener für "Weiteren Namen hinzufügen" Button
    if (addNameBtn) {
        addNameBtn.addEventListener('click', function() {
            addNameField();
        });
    }

    // Logik zum Umschalten zwischen "Anzahl Gruppen" und "Gruppengrösse"
    function updateGroupInputsVisibility() {
        if (groupTypeSelect.value === 'num_groups') {
            numGroupsInputDiv.style.display = 'block';
            groupSizeInputDiv.style.display = 'none';
            numGroupsInput.required = true;
            numGroupsInput.disabled = false; // Wichtig: Aktivieren, wenn sichtbar
            groupSizeInput.required = false;
            groupSizeInput.disabled = true; // Wichtig: Deaktivieren, wenn unsichtbar
        } else { // group_size
            numGroupsInputDiv.style.display = 'none';
            groupSizeInputDiv.style.display = 'block';
            numGroupsInput.required = false;
            numGroupsInput.disabled = true; // Wichtig: Deaktivieren, wenn unsichtbar
            groupSizeInput.required = true;
            groupSizeInput.disabled = false; // Wichtig: Aktivieren, wenn sichtbar
        }
    }

    if (groupTypeSelect) {
        groupTypeSelect.addEventListener('change', updateGroupInputsVisibility);
        // Initialen Zustand beim Laden der Seite setzen
        updateGroupInputsVisibility();
    }


    // Event Listener für das Speichern der PlayerList
    if (savePlayerListForm) {
        savePlayerListForm.addEventListener('submit', function(event) {
            // Entferne alle alten Hidden-Felder, falls vorhanden
            while (namesForSavingContainer.firstChild) {
                namesForSavingContainer.removeChild(namesForSavingContainer.firstChild);
            }

            // Sammle alle aktuellen Namen aus den Eingabefeldern
            const currentNameInputs = namesContainer.querySelectorAll('input[name="name[]"]');
            currentNameInputs.forEach(input => {
                // Füge alle Namen hinzu, auch leere, damit die Reihenfolge stimmt, wenn wir später eine Bearbeitungsfunktion bauen
                const hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = 'name[]';
                hiddenInput.value = input.value.trim(); // Trimme den Wert, aber behalte leere Felder
                namesForSavingContainer.appendChild(hiddenInput);
            });

            // Für die Speicherung der PlayerList MÜSSEN Namen vorhanden sein
            const actualNames = Array.from(currentNameInputs).filter(input => input.value.trim() !== '');
            if (actualNames.length === 0) {
                alert("Bitte gib Namen ein, um die Liste zu speichern.");
                event.preventDefault(); // Verhindert das Absenden des Formulars
            }
        });
    }

    // Logik für Enter-Taste in den Namensfeldern
    if (namesContainer) {
        namesContainer.addEventListener('keydown', function(event) {
            // Überprüfen, ob die Enter-Taste (Key 13) gedrückt wurde
            if (event.key === 'Enter') {
                event.preventDefault(); // Verhindere das Standard-Formular-Submit

                const target = event.target;
                // Prüfen, ob das Event von einem Namens-Inputfeld kommt
                if (target.matches('input[name="name[]"]')) {
                    const allNameInputs = Array.from(namesContainer.querySelectorAll('input[name="name[]"]'));
                    const currentIndex = allNameInputs.indexOf(target);
                    const currentInputValue = target.value.trim();

                    // Fall 1: Cursor in einem leeren Textfeld -> Gruppen generieren
                    if (currentInputValue === '') {
                        generateGroupsForm.submit(); // Sende das Hauptformular ab
                    } 
                    // Fall 2: Letztes Namensfeld und nicht leer -> neues Feld hinzufügen
                    else if (currentIndex === allNameInputs.length - 1) {
                        addNameField();
                    } 
                    // Fall 3: Nicht das letzte Feld und nicht leer -> Fokus auf nächstes Feld
                    else {
                        const nextInput = allNameInputs[currentIndex + 1];
                        if (nextInput) {
                            nextInput.focus();
                        }
                    }
                }
            }
        });
    }
});
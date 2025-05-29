document.addEventListener('DOMContentLoaded', function() {
    const namesContainer = document.getElementById('names-container');
    const addNameBtn = document.getElementById('add-name-btn');
    const savePlayerListForm = document.getElementById('save-player-list-form');
    const namesForSavingContainer = document.getElementById('names-for-saving-container');

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
    }

    // Initialen Zustand beim Laden der Seite: Wenn keine Namen geladen sind,
    // stelle sicher, dass es mindestens zwei leere Felder gibt (oder die Standardfelder in Jinja).
    // Wenn Namen geladen sind, werden sie von Jinja direkt gerendert, also kein JS nötig.
    if (namesContainer.children.length === 0) {
        addNameField();
        addNameField(); // Füge standardmässig zwei Felder hinzu, falls keine geladen wurden
    }

    addNameBtn.addEventListener('click', function() {
        addNameField();
    });

    // Logik zum Umschalten zwischen "Anzahl Gruppen" und "Gruppengrösse"
    const groupTypeSelect = document.getElementById('group-type');
    const numGroupsInputDiv = document.getElementById('num-groups-input');
    const groupSizeInputDiv = document.getElementById('group-size-input');
    const numGroupsInput = document.getElementById('num-groups');
    const groupSizeInput = document.getElementById('group-size');


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

    groupTypeSelect.addEventListener('change', updateGroupInputsVisibility);

    // Initialen Zustand beim Laden der Seite setzen
    // Simuliert ein Change-Event, um die korrekte Anzeige beim ersten Laden zu gewährleisten
    updateGroupInputsVisibility();


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
                if (input.value.trim() !== '') { // Füge nur nicht-leere Namen hinzu
                    const hiddenInput = document.createElement('input');
                    hiddenInput.type = 'hidden';
                    hiddenInput.name = 'name[]';
                    hiddenInput.value = input.value.trim();
                    namesForSavingContainer.appendChild(hiddenInput);
                }
            });

            if (namesForSavingContainer.children.length === 0) {
                alert("Bitte gib Namen ein, um die Liste zu speichern.");
                event.preventDefault(); // Verhindert das Absenden des Formulars
            }
        });
    }
});
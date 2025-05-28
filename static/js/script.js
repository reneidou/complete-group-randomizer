document.addEventListener('DOMContentLoaded', function() {
    // Logik für das Hinzufügen neuer Namenfelder
    const addNameBtn = document.getElementById('add-name-btn');
    const namesContainer = document.getElementById('names-container');

    addNameBtn.addEventListener('click', function() {
        const newInput = document.createElement('input');
        newInput.type = 'text';
        newInput.name = 'name[]'; // Wichtig für Flask, um eine Liste zu erhalten
        newInput.placeholder = 'Name der Person';
        newInput.required = true;
        namesContainer.appendChild(newInput);
    });

    // Logik zum Umschalten zwischen "Anzahl Gruppen" und "Gruppengrösse"
    const groupTypeSelect = document.getElementById('group-type');
    const numGroupsInputDiv = document.getElementById('num-groups-input');
    const groupSizeInputDiv = document.getElementById('group-size-input');

    groupTypeSelect.addEventListener('change', function() {
        if (groupTypeSelect.value === 'num_groups') {
            numGroupsInputDiv.style.display = 'block';
            groupSizeInputDiv.style.display = 'none';
            // Setze 'required' Attribut basierend auf Sichtbarkeit
            document.getElementById('num-groups').required = true;
            document.getElementById('group-size').required = false;
        } else {
            numGroupsInputDiv.style.display = 'none';
            groupSizeInputDiv.style.display = 'block';
            // Setze 'required' Attribut basierend auf Sichtbarkeit
            document.getElementById('num-groups').required = false;
            document.getElementById('group-size').required = true;
        }
    });

    // Initialen Zustand beim Laden der Seite setzen
    // Simuliert ein Change-Event, um die korrekte Anzeige beim ersten Laden zu gewährleisten
    groupTypeSelect.dispatchEvent(new Event('change'));
});
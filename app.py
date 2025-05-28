from flask import Flask, render_template, request
import random # Importiere das random-Modul für Zufallsfunktionen

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_groups():
    names = [name.strip() for name in request.form.getlist('name[]') if name.strip()] # Namen bereinigen und leere entfernen
    group_type = request.form['group_type']

    # Überprüfen, ob genügend Namen vorhanden sind
    if not names:
        # Wenn keine Namen eingegeben wurden, leite zurück zur Startseite mit einer Fehlermeldung
        # (Später fügen wir echte Flash-Nachrichten hinzu)
        return render_template('index.html', error_message="Bitte gib mindestens einen Namen ein.")

    num_people = len(names)
    random.shuffle(names) # Mische die Namen zufällig

    groups = []

    if group_type == 'num_groups':
        try:
            num_groups = int(request.form['num_groups'])
            if num_groups <= 0:
                raise ValueError("Anzahl Gruppen muss positiv sein.")
            if num_groups > num_people:
                num_groups = num_people # Nicht mehr Gruppen als Personen erstellen
                # Später eine Warnung ausgeben
        except ValueError:
            return render_template('index.html', error_message="Ungültige Anzahl Gruppen eingegeben.")

        # Gleichmässige Verteilung der Namen auf die Gruppen
        for i in range(num_groups):
            groups.append([])

        for i, name in enumerate(names):
            groups[i % num_groups].append(name)

    else: # group_type == 'group_size'
        try:
            group_size = int(request.form['group_size'])
            if group_size <= 0:
                raise ValueError("Gruppengrösse muss positiv sein.")
        except ValueError:
            return render_template('index.html', error_message="Ungültige Gruppengrösse eingegeben.")

        if group_size == 0: # Division durch Null verhindern, falls jemand 0 eingibt, was durch min="1" verhindert werden sollte
             return render_template('index.html', error_message="Gruppengrösse kann nicht Null sein.")

        # Teilen in Gruppen basierend auf der Grösse
        for i in range(0, num_people, group_size):
            group = names[i:i + group_size]
            groups.append(group)

        # Optional: Umgang mit Rest (z.B. letzte Gruppe kleiner oder Namen verteilen)
        # Für jetzt lassen wir die letzte Gruppe einfach kleiner.
        # Später hier komplexere Logik, wie z.B. gleichmässiges Verteilen der Reste.


    # Übergibt die generierten Gruppen an ein neues Template 'results.html'
    return render_template('results.html', groups=groups)


if __name__ == '__main__':
    app.run(debug=True)
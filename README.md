# Zufallsgenerator für Gruppen und Teams

Ein vielseitiger Web-App-Generator zur dynamischen und intelligenten Gruppeneinteilung für Projekte, Sport oder beliebige Anwendungsfälle.

---

## Inhaltsverzeichnis

* [Über dieses Projekt](#über-dieses-projekt)
* [Funktionen](#funktionen)
* [Monetarisierung](#monetarisierung)
* [Technologien](#technologien)
* [Installation und Nutzung](#installation-und-nutzung)
* [Beitrag leisten](#beitrag-leisten)
* [Lizenz](#lizenz)
* [Kontakt](#kontakt)

---

## Über dieses Projekt

Dieses Projekt ist eine innovative Web-App, die die Erstellung von zufälligen Gruppen und Teams revolutioniert. Anders als bestehende Generatoren bietet sie eine Fülle von erweiterten, optionalen Funktionen, um die Gruppeneinteilung an individuelle Bedürfnisse anzupassen – sei es für schulische Projekte, Sportmannschaften oder andere kollaborative Umgebungen. Die App ist darauf ausgelegt, intuitiv und schnell bedienbar zu sein, auch ohne Registrierung, bietet aber umfassende Speicher- und Verwaltungsfunktionen für registrierte Nutzer.

---

## Funktionen

Der Zufallsgenerator wird die folgenden Hauptfunktionen bieten:

### Basis-Gruppen-Generierung
* **Modus-Auswahl (Optional):** Wahl zwischen "Projekt-Teams", "Sport-Teams" oder "Standard-Modus" (für zukünftige erweiterte Hilfsfunktionen).
* **Sportarten-Auswahl (Optional):** Möglichkeit zur Auswahl spezifischer Sportarten oder eines allgemeinen "Standard-Modus".
* **Namen und Gruppen eingeben:** Einfache Eingabe von Namen, mit der Möglichkeit, leere Felder zu löschen und der Cursor springt automatisch ins nächste Feld.
    * **Schnelleingabe:** Drücken der Enter-Taste erstellt ein neues Namensfeld. Befindet sich der Cursor in einem leeren Feld, startet Enter den Generator und ignoriert die übrigen leeren Felder.
* **Gruppengrösse/-anzahl:** Auswahl der gewünschten Gruppengrösse oder der Anzahl der zu erstellenden Gruppen.
* **Ergebnis-Darstellung:** Übersichtliche Anzeige der zufällig generierten Gruppen.

### Erweiterte Funktionen (Modulweise aktivierbar)
Die folgenden Funktionen können optional mit einem Klick hinzugefügt werden, um die Benutzeroberfläche übersichtlich zu halten:

* **Ratings pro Teilnehmer (Optional):**
    * Eingabe individueller Ratings pro Teilnehmer.
    * **Flexible Rating-Spanne:** Die Spanne kann vollständig individuell gewählt und gespeichert werden (z.B. 1-5, 0-50, 4-16, -10-30, oder sogar absteigend wie 70-20, wobei die niedrigere Zahl die "bessere" ist).
* **Rollen/Tags und Verteilung (Optional):**
    * Definition von Rollenbezeichnungen/Tags (z.B. "Verteidiger", "Zuspieler").
    * Festlegung der gewünschten Verteilung der Rollen in den Gruppen.
    * Zufällige Verteilung der Namen basierend auf ihren Rollen.
    * **Warnsystem:** Automatische Warnung bei zu wenigen oder zu vielen Personen einer Rolle.
    * **Lösungsvorschläge:** Optionen zur Anpassung der Rollen (temporär/permanent ändern, Reservespieler zuordnen) oder Systemempfehlungen.
* **Team- und Gruppenpräferenzen (Optional):**
    * Festlegung, welche Personen unbedingt zusammen in einer Gruppe sein sollen und welche auf keinen Fall.
    * **Konfliktmanagement:** System gibt eine Warnung aus, wenn Präferenzen nicht vollständig erfüllt werden können. Benutzer kann Eingaben anpassen oder einen Kompromissvorschlag des Systems annehmen.
* **Dynamische Rating-Anpassung nach Spielergebnissen (Optional):**
    * Möglichkeit, nach der Gruppeneinteilung Punktestände (Plus-/Minuspunkte) pro Gruppe einzutragen.
    * Automatisches, proportionales Anpassen der individuellen Personen-Ratings basierend auf den Gruppenpunkten.

### Datenmanagement und Benutzerfreundlichkeit
* **Speicherung von Eingaben (optionaler Login):**
    * **Gast-Nutzung:** App ist voll funktionsfähig ohne Login und Speicherung.
    * **Registrierung/Login:** Möglichkeit zur Registrierung und Anmeldung, um eingegebene Namen, Teams und Gruppenergebnisse jederzeit abzurufen und zu speichern.
    * **Nahtlose Datenübergabe:** Aktuelle, nicht gespeicherte Eingaben bleiben auch nach dem Registrierungs-/Login-Prozess erhalten.
* **Verwaltung gespeicherter Daten:**
    * **Teams:** Speicherung von Namenslisten (als "Teams" bezeichnet), optional mit Ratings, Rollen und Präferenzen. Ermöglicht schnellen Zugriff auf oft genutzte Personenpools (z.B. eine Schulklasse oder Sportmannschaft).
    * **Groups:** Speicherung spezifischer Gruppenkonstellationen ("Groups") innerhalb eines gespeicherten "Teams", um vergangene Einteilungen wieder einsehen oder damit weiterarbeiten zu können.
    * Möglichkeit, gespeicherte Teams und Groups zu löschen.
* **Interaktive Ergebnis-Anzeige:**
    * **Drag & Drop:** Einfaches Ändern der Gruppenzusammenstellung per Drag & Drop im Ergebnisbereich.
    * **Undo/Redo:** Rückgängigmachen und Wiederherstellen von Änderungen.
    * **Rating-Anzeige:** Ein- und Ausblenden von Personen-Ratings und berechneten Gruppen-Ratings.
    * **Teilen von Ergebnissen:** Generieren von Resultatfeld-Links oder QR-Codes zum einfachen Teilen der Gruppeneinteilung.

---

## Monetarisierung

Das Projekt ist darauf ausgelegt, über **PythonAnywhere** veröffentlicht und monetarisiert zu werden. Dies kann durch Werbeanzeigen auf der Plattform oder durch Premium-Funktionen für registrierte Benutzer (z.B. erweiterter Speicherplatz, detailliertere Statistiken, werbefreie Nutzung) geschehen.

---

## Technologien

Das Projekt wird voraussichtlich die folgenden Technologien verwenden:

* **Frontend (Webseite):** HTML, CSS, JavaScript (mit einem Framework wie **React** oder **Vue.js** für eine dynamische und interaktive Benutzeroberfläche aufgrund der Komplexität der UI-Elemente wie Drag&Drop und modulare Funktionen).
* **Backend:** **Python** mit dem **Flask** Web Framework.
* **Datenbank:** **SQLite** für die einfache Entwicklung und Migration, später eventuell PostgreSQL für Skalierbarkeit auf PythonAnywhere.
* **Versionskontrolle:** **Git** und **GitHub** für ein sauberes Versionsmanagement und zur Vermeidung von Datenverlust.

---

## Installation und Nutzung

Detaillierte Anweisungen zur Installation und lokalen Nutzung werden hier nach Projektfortschritt bereitgestellt. Ziel ist die Veröffentlichung auf PythonAnywhere.

### Lokale Entwicklungsumgebung einrichten
*Voraussetzungen:* **Python**, **VS Code** und **Git** sind auf deinem System installiert.

1.  **Projektordner erstellen:**
    * Öffne deinen Dateimanager (Explorer unter Windows, Finder unter macOS).
    * Erstelle einen neuen Ordner an einem beliebigen Ort, z.B. `C:\Projekte\Zufallsgenerator` (Windows) oder `/Users/DeinName/Projekte/Zufallsgenerator` (macOS).
2.  **Projekt in VS Code öffnen:**
    * Öffne **Visual Studio Code**.
    * Klicke auf **"File" (Datei)** -> **"Open Folder..." (Ordner öffnen...)**
    * Navigiere zu dem soeben erstellten `Zufallsgenerator`-Ordner und klicke auf **"Select Folder" (Ordner auswählen)**.
3.  **Terminal in VS Code öffnen:**
    * In VS Code: Klicke auf **"Terminal"** in der oberen Menüleiste -> **"New Terminal" (Neues Terminal)**. Ein Terminal-Fenster öffnet sich unten in VS Code und ist bereits im `Zufallsgenerator`-Ordner.
4.  **Virtuelle Umgebung erstellen:**
    * Im VS Code Terminal, gib ein und drücke Enter:
        ```bash
        python -m venv venv
        ```
    * *(Warte, bis der Vorgang abgeschlossen ist. Ein neuer Ordner namens `venv` erscheint in deinem Projektordner.)*
5.  **Virtuelle Umgebung aktivieren:**
    * **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    * *(Du siehst `(venv)` vor deinem Prompt, was anzeigt, dass die virtuelle Umgebung aktiv ist.)*
6.  **Flask installieren:**
    * Stelle sicher, dass `(venv)` im Terminal-Prompt steht.
    * Gib ein und drücke Enter:
        ```bash
        pip install Flask
        ```

### Erste Flask-Anwendung erstellen (Minimalbeispiel)

1.  **`app.py` erstellen:**
    * Klicke im VS Code auf das **"New File" (Neue Datei)** Symbol im Explorer-Bereich (linker Seitenleiste) neben deinem `Zufallsgenerator`-Ordner.
    * Gib den Namen `app.py` ein und drücke Enter.
2.  **Code einfügen:**
    * Kopiere den folgenden Code in die `app.py`-Datei:
        ```python
        # app.py
        from flask import Flask, render_template, request, redirect, url_for, session
        import os

        app = Flask(__name__)
        # Für Sessions ist ein geheimer Schlüssel notwendig
        app.secret_key = os.urandom(24) # Erzeugt einen zufälligen Schlüssel bei jedem Start, für Produktion einen festen Schlüssel verwenden!

        # Eine einfache Startseite
        @app.route('/')
        def index():
            return render_template('index.html')

        if __name__ == '__main__':
            app.run(debug=True)
        ```
3.  **`templates` Ordner erstellen:**
    * Klicke im VS Code Explorer auf das **"New Folder" (Neuer Ordner)** Symbol im Explorer-Bereich neben deinem `Zufallsgenerator`-Ordner.
    * Gib den Namen `templates` ein und drücke Enter.
4.  **`index.html` erstellen:**
    * Klicke im VS Code Explorer mit der rechten Maustaste auf den neu erstellten `templates`-Ordner.
    * Wähle **"New File" (Neue Datei)**.
    * Gib den Namen `index.html` ein und drücke Enter.
5.  **HTML-Code einfügen:**
    * Kopiere den folgenden HTML-Code in die `index.html`-Datei:
        ```html
        <!DOCTYPE html>
        <html lang="de">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Zufallsgenerator</title>
            <style>
                body { font-family: sans-serif; text-align: center; margin-top: 50px; }
                h1 { color: #333; }
            </style>
        </head>
        <body>
            <h1>Willkommen beim Zufallsgenerator für Gruppen!</h1>
            <p>Das ist der Startpunkt deines Projekts, Renato.</p>
        </body>
        </html>
        ```
6.  **Flask-Anwendung starten:**
    * Gehe zurück zum VS Code Terminal (stelle sicher, dass die virtuelle Umgebung aktiv ist).
    * Gib ein und drücke Enter:
        ```bash
        python app.py
        ```
    * Du solltest eine Ausgabe sehen, die `* Running on http://127.0.0.1:5000` enthält.
7.  **Webseite im Browser öffnen:**
    * Öffne deinen Webbrowser.
    * Gib in die Adressleiste ein: `http://127.0.0.1:5000` und drücke Enter.
    * Du solltest die Überschrift "Willkommen beim Zufallsgenerator für Gruppen!" sehen.

### Versionskontrolle mit Git und GitHub einrichten

Jetzt, da du eine grundlegende App hast, ist es wichtig, sie unter Versionskontrolle zu stellen.

1.  **Git-Repository initialisieren:**
    * Gehe im VS Code Terminal in deinen `Zufallsgenerator`-Ordner (wenn du es geschlossen hast, öffne ein neues Terminal in VS Code).
    * Gib ein und drücke Enter:
        ```bash
        git init
        ```
    * *(Dies initialisiert ein leeres Git-Repository in deinem Ordner.)*
2.  **`README.md` hinzufügen:**
    * Klicke im VS Code Explorer auf das **"New File" (Neue Datei)** Symbol im Explorer-Bereich (linker Seitenleiste) neben deinem `Zufallsgenerator`-Ordner.
    * Gib den Namen `README.md` ein und drücke Enter.
    * Füge diesen Markdown-Code, den ich dir gerade gebe, in diese Datei ein und speichere sie.
3.  **`.gitignore` erstellen:**
    * Klicke im VS Code Explorer auf das **"New File" (Neue Datei)** Symbol.
    * Gib den Namen `.gitignore` ein und drücke Enter.
    * Füge die folgenden Zeilen in die `.gitignore`-Datei ein und speichere sie. Diese Datei sagt Git, welche Dateien und Ordner es ignorieren soll (z.B. deine virtuelle Umgebung, da sie gross ist und lokal erzeugt wird):
        ```
        venv/
        __pycache__/
        *.pyc
        .env
        ```
4.  **Dateien zu Git hinzufügen und ersten Commit machen:**
    * Im VS Code Terminal:
        ```bash
        git add .
        ```
        *(Dieser Befehl fügt alle neuen und geänderten Dateien zum "Staging-Bereich" von Git hinzu.)*
        ```bash
        git commit -m "Initial commit: Setup basic Flask app and README"
        ```
        *(Dieser Befehl speichert den aktuellen Zustand deiner Dateien im lokalen Git-Verlauf.)*
5.  **GitHub-Repository erstellen:**
    * Gehe zu [https://github.com/](https://github.com/) und logge dich ein.
    * Klicke auf das **"+"** Zeichen oben rechts und wähle **"New repository" (Neues Repository)**.
    * **Repository name:** Gib `Zufallsgenerator` ein.
    * **Description (optional):** Gib eine kurze Beschreibung ein, z.B. "Ein vielseitiger Gruppen-Zufallsgenerator".
    * Wähle **"Public" (Öffentlich)**.
    * **WICHTIG:** Kreuze **NICHT** "Add a README file", "Add .gitignore", oder "Choose a license" an, da wir diese bereits lokal erstellt haben.
    * Klicke auf **"Create repository" (Repository erstellen)**.
6.  **Lokales Repository mit GitHub verbinden und pushen:**
    * Nachdem du das Repository auf GitHub erstellt hast, siehst du Anweisungen. Wir werden die "push an existing repository from the command line" Option verwenden.
    * Kopiere die beiden Zeilen, die dir GitHub vorschlägt, im Stil von:
        ```bash
        git remote add origin [https://github.com/DeinGitHubName/Zufallsgenerator.git](https://github.com/DeinGitHubName/Zufallsgenerator.git)
        git branch -M main
        git push -u origin main
        ```
        *(Ersetze `DeinGitHubName` durch deinen tatsächlichen GitHub-Benutzernamen.)*
    * Füge diese Befehle in dein **VS Code Terminal** ein und drücke nach jeder Zeile Enter.
    * Möglicherweise wirst du aufgefordert, deine GitHub-Anmeldeinformationen einzugeben.

---

## Beitrag leisten

Vorschläge und Verbesserungen sind willkommen! Bitte eröffne ein Issue oder sende einen Pull Request.

**Wichtiger Hinweis:** Dieses Repository ist öffentlich. Änderungen dürfen vorgeschlagen werden, aber der Code darf ohne meine Zustimmung ausserhalb der Weiterentwicklung nicht veröffentlicht oder kommerziell genutzt werden. Für die Weiterentwicklung darf der Code jedoch verwendet werden.

---

## Lizenz

Dieses Projekt steht unter der [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/). Dies bedeutet, dass der Code für die Weiterentwicklung verwendet werden darf, aber eine kommerzielle Nutzung oder Veröffentlichung ohne explizite Zustimmung nicht gestattet ist.

---

## Kontakt


Ich will eine Web-App für einen Gruppen-Zufallsgenerator erstellen und auf pythonanywhere veröffentlichen, Werbung schalten und Geld damit verdienen. Ich habe noch keinen Zufallsgenerator gesehen, der all diese Funktionen erfüllen kann:
1. (Optional) Wahl zwischen Modus: Projekt-Teams oder Sport-Teams, oder keine Angabe (hat vielleicht später Einfluss auf weitere Hilfsfunktionen, dies kommt dann aber später als Update dazu)
2. (Optional) Möglichkeit, aus verschiedenen Sportarten zu wählen oder einfach Standard-Modus
3. Eingabe von Namen und Teams und Möglichkeit, die Eingaben zu speichern. Dabei möchte ich, dass man auch ohne Login und ohne speichern die App benutzen kann, aber dass man auch die Möglichkeit hat, einen Login zu machen und die Teams und die Eingaben später jederzeit wieder abrufen kann. Man kann auch eine Namensliste als Datensatz speichern und auch jedes Gruppenkonstellations-Resultat unter dieser Namenslisten-Gruppe speichern und eine neue Konstellation starten, damit man jederzeit wieder damit arbeiten kann oder das Resultat wieder einsehen kann.
4. (Optional) Eingabe von Ratings pro Teilnehmer/Name. Die Rating-Spanne kann dabei komplett individuell gewählt werden und auch gespeichert werden (z.B. 1-5 oder 0-50 oder 4-16 oder -10-30, also auch negative Zahlen sind erlaubt, oder auch von 70-20, also auch die Möglichkeit, dass die niedrigere Zahl die "bessere" ist)
5. (optional) Eingabe von Rollenbezeichnungen/Tags, gewünschte Verteilung der Rollen in die verschiedenen Gruppen und dann zufällige Verteilung der Namen nach Rollen (also z.B. wie viele Verteidiger und wie viele Mittelfeldspieler ich in einer Gruppe haben möchte, oder beim Volleyball wie viele Zuspieler und wie viele Mittelblocker ich in einer Gruppe haben möchte und dann die Spieler zufällig in die Gruppen nach Rollen einteilen lassen), und das System gibt eine Warnung aus, wenn zu wenige oder zu viele Personen von einer Rolle vorhanden sind. Dann kann eine Lösung ausgewählt werden, z.B. Rolle von übrigen Spielern temporär oder permanent ändern oder Reservespieler für eine Gruppe zuordnen, z.B. wenn zu viele Verteidiger vorhanden sind, einen Verteidiger zu einem Angreifer machen, oder den übrigen Verteidiger als Reservespieler für die Verteidigung als Überzähliger Spieler zuordnen. Das System gibt auch automatisch Empfehlungs-Informationen
6. Gewünschte Gruppen-Grösse oder gewünschte Anzahl Gruppen auswählen.
7. (optional) Präferenz auswählen, welche Personen ich sicher in einer Gruppe zusammen haben möchte und welche sicher nicht zusammen in der Gruppe sein können. Dies kann ja nicht immer gewährleistet werden. Nach einer Warnung vom System, kann man entweder die Eingaben anpassen, oder einen Kompromiss-Vorschlag des Systems annehmen, bei dem dann trotzdem zwei Personen zusammen in der Gruppe sind, die nicht zusammen sein sollten, oder zwei nicht zusammen sind, die zusammen sein sollten.
8. (optional) die Möglichkeit, nach der Gruppeneinteilung für die Gruppen z.B. bei Spielen Punktestände (Pluspunkte oder Minuspunkte) einzutragen und dann die Möglichkeit bieten, mit den Punkten das Personenrating mit einem Klick automatisch proportional zu verändern. Teilnehmer einer Gruppe, die viele Punkte gesammelt hat, werden also mit einem individuellen Rating-Bonus belohnt und Teilnehmer einer Gruppe mit wenig gesammelten Punkten oder Minuspunkten bekommen Minuspunkte.
9. Alle optionalen Sachen kann man modular auswählen, sie sind also grundsätzlich beim Start zur Einfachheit ausgeblendet, können aber mit einem Klick hinzugefügt werden, wenn man sie wünscht
10. Nach der Gruppeneinteilung kann ich im Resultatfeld die Gruppen einfach per Drag&Drop ändern und die Änderungen mit einer "return" und "redo"-Taste rückgängig machen oder rückgängig gemachte Änderungen wieder herstellen.
11. Im Resultatfeld kann ich Personen-Ratings und berechnete Gruppen-Ratings ein- und ausblenden und die Gruppen auch teilen, z.B. mit einem Resultatfeld-Link oder einem automatisch generierten QR-Code.

Ich habe Python und VS Code installiert. Ich habe auch Git installiert und einen Github-Account, in dem ich das Projekt speichern kann und ich möchte damit ein sauberes Versions-Management mit verschiedenen branches betreiben. Ich möchte jederzeit Datenverlust vermeiden. Aber ich habe wirklich keine Ahnung, wie ich Schritt für Schritt von der Entwicklung bis zur Publikation und zur Monetarisierung vorgehen muss. Führe mich wirklich Schritt für Schritt, sehr einfach und genau durch den Prozess und sage mir jeden Klick.


Folgende Details möchte ich noch hinzufügen:
1. Ich möchte die Eingabefelder für die Namen auch löschen können, wenn ich z.B. aus Versehen auf "weiteren Namen hinzufügen" geklickt habe, will ich den Namen oder das leere Feld auch wieder löschen können.
2. Beim Hinzufügen eines neuen Namenfeldes möchte ich den Cursor direkt im neuen Textfeld haben, damit ich nicht immer klicken muss. Die Eingabe muss in der Praxis ja superschnell und intuitiv funktionieren.
3. auch die gespeicherten Listen möchte ich wieder löschen können.
4. Mit der Enter-Taste soll direkt ein neuer Name eingegeben werden können und nicht der Zufallsgenerator gestartet werden. Wenn der letzte Name eingetragen wurde und kein weiteres Textfeld vorhanden ist, wird mit Enter automatisch ein neues Textfeld erstellt und der Cursor befindet sich automatisch direkt in diesem neuen Textfeld. Wenn sich der Cursor in einem leeren Textfeld befindet wird mit Enter der Gruppengenerator automatisch gestartet, auch wenn noch leere Textfelder vorhanden sind. In diesem Fall werden die leeren Textfelder für die Berechnung gelöscht und nicht in die Gruppenbildung mit einbezogen.
5. Ich möchte die pure Namensliste von sogenannten Teams (später auch gegebenfalls mit den optionalen Daten) speichern können und innerhalb dieses "Teams" dann für die Berechnung einzelner Gruppenkonstellationen (genannt "Groups" zur Abgrenzung von "Teams") auswählen können, welche der gespeicherten Namen ich für die Gruppeneinteilung benutzen möchte. Und dann möchte ich die zufälligen Gruppenkonstellationen innerhalb der Team-Seite speichern können. Mein Ziel ist es, z.B. sowohl auf die komplette Namensliste einer Schulklasse oder einer Sport-Mannschaft zurückgreifen zu können (um sie nicht immer neu eingeben zu müssen) als auch auf die errechneten Gruppeneinteilungen zurückgreifen zu können (z.B. auf eine Konstellation am letzten Dienstag und auf eine Konstellation letzten Donnerstag, an dem nicht alle Schüler anwesend waren).
6. Wenn ich nicht eingeloggt oder registriert bin, aber meine eingegebenen Gruppendaten schon eingegeben habe, möchte ich diese momentanen Daten nicht durch den Anmelde- oder Registrierungsprozess verlieren, sondern möchte meine Eingaben direkt nach der Anmeldung oder Registrierung wieder sehen, damit ich den Generator fortsetzen kann.

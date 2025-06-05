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

Der Zufallsgenerator bietet die folgenden Hauptfunktionen:

### Basis-Gruppen-Generierung
* **Namen eingeben:** Einfache Eingabe von Namen mit automatischer Fokussierung auf neue Felder
* **Intelligente Enter-Taste:** 
  - Enter in nicht-leerem Feld: Neues Namensfeld erstellen
  - Enter in leerem Feld: Gruppen generieren (leere Felder werden ignoriert)
* **Gruppengrösse/-anzahl:** Auswahl der gewünschten Gruppengrösse oder der Anzahl der zu erstellenden Gruppen
* **Ergebnis-Darstellung:** Übersichtliche Anzeige der zufällig generierten Gruppen

### Datenmanagement
* **Gast-Nutzung:** Voll funktionsfähig ohne Login
* **Registrierung/Login:** Speichern von Namenslisten und Gruppeneinteilungen
* **Nahtlose Datenübergabe:** Eingaben bleiben nach Login/Registrierung erhalten
* **Teams verwalten:** 
  - Namenslisten speichern und laden
  - Gruppenkonstellationen speichern und abrufen
  - Einfaches Löschen von Listen und Gruppen

---

## Monetarisierung

Das Projekt ist darauf ausgelegt, über **PythonAnywhere** veröffentlicht und monetarisiert zu werden. Dies kann durch Werbeanzeigen auf der Plattform oder durch Premium-Funktionen für registrierte Benutzer (z.B. erweiterter Speicherplatz, detailliertere Statistiken, werbefreie Nutzung) geschehen.

---

## Technologien

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Python mit Flask
* **Datenbank:** SQLite
* **Versionskontrolle:** Git und GitHub

---

## Installation und Nutzung

### Lokale Entwicklung
1. Python, VS Code und Git installieren
2. Projektordner erstellen und in VS Code öffnen
3. Terminal öffnen und virtuelle Umgebung erstellen:
   ```bash
   python -m venv venv
4. Virtuelle Umgebung aktivieren:
- Windows: .\venv\Scripts\activate
- macOS/Linux: source venv/bin/activate
5. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```
6. App starten:
```bash
python app.py
```
7. Im Browser öffnen: `http://127.0.0.1:5000`

### PythonAnywhere Deployment
1. Konto auf pythonanywhere.com erstellen
2. Neue Web-App erstellen (Flask)
3. Git-Repository klonen
4. Virtuelle Umgebung einrichten
5. Abhängigkeiten installieren
6. Datenbank initialisieren
7. App konfigurieren und starten

## Beitrag leisten
Vorschläge und Verbesserungen sind willkommen! Bitte eröffne ein Issue oder sende einen Pull Request.

**Wichtiger Hinweis:** Dieses Repository ist öffentlich. Änderungen dürfen vorgeschlagen werden, aber der Code darf ohne meine Zustimmung ausserhalb der Weiterentwicklung nicht veröffentlicht oder kommerziell genutzt werden.

## Lizenz
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Kontakt
reneidou - [GitHub Profil](https://github.com/reneidou)
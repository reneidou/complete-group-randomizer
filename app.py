from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random
import os
import json
from functools import wraps
from datetime import datetime # Importiere datetime

app = Flask(__name__)

# --- Datenbank Konfiguration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Dein_wirklich_sehr_geheimer_schluessel_bitte_aendern_im_produktivbetrieb_123ABC'

db = SQLAlchemy(app)

# Erstelle den instance-Ordner, falls er nicht existiert
if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)

# Registriere den 'fromjson'-Filter für Jinja2 (falls noch nicht geschehen)
# Dies ermöglicht es, JSON-Strings direkt in den Templates zu parsen
app.jinja_env.filters['fromjson'] = json.loads

# --- Datenbank-Modelle definieren ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    player_lists = db.relationship('PlayerList', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class PlayerList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    players_json = db.Column(db.Text, nullable=False) # JSON-String der Spielernamen
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    generated_groups = db.relationship('GeneratedGroup', backref='player_list', lazy=True, cascade="all, delete-orphan")

class GeneratedGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_list_id = db.Column(db.Integer, db.ForeignKey('player_list.id'), nullable=False)
    name = db.Column(db.String(120), nullable=True) # Name der Gruppeneinteilung (optional)
    groups_json = db.Column(db.Text, nullable=False) # JSON-String der generierten Gruppen
    all_names_json = db.Column(db.Text, nullable=False) # JSON-String der Namen, die für diese Generierung verwendet wurden
    group_settings_json = db.Column(db.Text, nullable=False) # JSON-String der Einstellungen (num_groups, group_size, group_type)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# --- Datenbank initialisieren (nur einmal ausführen) ---
with app.app_context():
    db.create_all()

# --- Login-Handling ---
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Bitte melde dich an, um diese Funktion zu nutzen.', 'info')
            # RENATO - HIER IST DIE WICHTIGE ÄNDERUNG FÜR DATENÜBERNAHME!
            if request.method == 'POST':
                # Nur speichern, wenn die Anfrage eine Formular-Einreichung ist
                current_names = request.form.getlist('name[]')
                group_type = request.form.get('group_type')
                num_groups = request.form.get('num_groups')
                group_size = request.form.get('group_size')

                # Speichere die aktuellen Formular-Daten in der Session
                session['temp_form_data'] = {
                    'names': current_names,
                    'group_type': group_type,
                    'num_groups': num_groups,
                    'group_size': group_size
                }
            # Optional: Speichere auch den request.path um nach Login dorthin zurückzukehren
            session['next_url'] = request.url
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view


# --- Routen ---

@app.route('/')
def home():
    loaded_names = None
    group_type = 'num_groups' # Standardwert
    num_groups = ''
    group_size = ''
    selected_player_list_id = session.get('selected_player_list_id_for_save') # ID der aktuell geladenen Liste

    # RENATO - HIER IST DIE WICHTIGE ÄNDERUNG FÜR DATENÜBERNAHME NACH LOGIN/REGISTER!
    if 'temp_form_data' in session:
        temp_data = session.pop('temp_form_data') # Daten abrufen und aus Session löschen
        loaded_names = temp_data.get('names', [])
        group_type = temp_data.get('group_type', 'num_groups')
        num_groups = temp_data.get('num_groups', '')
        group_size = temp_data.get('group_size', '')
        flash('Deine vorherigen Eingaben wurden wiederhergestellt!', 'info')


    # Lade temporäre Namen und Einstellungen, wenn sie aus load_player_list oder load_generated_group kommen
    if 'temp_names' in session:
        loaded_names = session.pop('temp_names')
        # Überprüfe, ob es sich um eine Generierungs-Seite handelt, bevor Einstellungen geladen werden
        if 'temp_settings' in session:
            temp_settings = session.pop('temp_settings')
            group_type = temp_settings.get('group_type', 'num_groups')
            num_groups = temp_settings.get('num_groups', '')
            group_size = temp_settings.get('group_size', '')
        # Wenn eine player_list_id beim Laden einer generierten Gruppe mitgegeben wurde
        if 'temp_player_list_id' in session:
            selected_player_list_id = session.pop('temp_player_list_id')
            session['selected_player_list_id_for_save'] = selected_player_list_id


    return render_template('index.html',
                           loaded_names=loaded_names,
                           group_type=group_type,
                           num_groups=num_groups,
                           group_size=group_size,
                           selected_player_list_id=selected_player_list_id)


@app.route('/generate_groups', methods=['POST'])
def generate_groups():
    names = [name.strip() for name in request.form.getlist('name[]') if name.strip()] # Leere Namen ignorieren
    group_type = request.form.get('group_type')
    num_groups_str = request.form.get('num_groups')
    group_size_str = request.form.get('group_size')

    # Speichern der aktuellen PlayerList ID in der Session, falls eine geladen war
    # Dies ist wichtig, damit save_generated_group weiss, zu welcher PlayerList die Gruppe gehört
    if 'selected_player_list_id' in request.form:
        session['selected_player_list_id_for_save'] = request.form.get('selected_player_list_id')
    else:
        session.pop('selected_player_list_id_for_save', None) # Wenn keine ID übergeben wurde, Session-Variable löschen

    if not names:
        flash('Bitte gib mindestens einen Namen ein, um Gruppen zu generieren.', 'error')
        return redirect(url_for('home'))

    random.shuffle(names)
    groups = []
    error_message = None

    try:
        if group_type == 'num_groups':
            num_groups = int(num_groups_str)
            if num_groups <= 0:
                flash('Anzahl der Gruppen muss positiv sein.', 'error')
                return redirect(url_for('home'))
            if num_groups > len(names):
                flash(f'Du kannst nicht mehr Gruppen als Personen erstellen ({num_groups} Gruppen für {len(names)} Personen).', 'error')
                return redirect(url_for('home'))

            # Verteilung der Personen auf die Gruppen
            for i in range(num_groups):
                groups.append([])
            for i, name in enumerate(names):
                groups[i % num_groups].append(name)
        elif group_type == 'group_size':
            group_size = int(group_size_str)
            if group_size <= 0:
                flash('Größe der Gruppen muss positiv sein.', 'error')
                return redirect(url_for('home'))
            if group_size > len(names):
                flash(f'Gruppengrösse ({group_size}) kann nicht grösser sein als die Anzahl der Personen ({len(names)}).', 'error')
                return redirect(url_for('home'))

            current_group = []
            for name in names:
                current_group.append(name)
                if len(current_group) == group_size:
                    groups.append(current_group)
                    current_group = []
            if current_group: # Restliche Personen in eine Gruppe (oder zu den letzten hinzufügen)
                if groups:
                    # Füge die verbleibenden Personen zu den letzten Gruppen hinzu
                    # Dies verteilt die "ungeraden" Personen besser
                    for i, remaining_name in enumerate(current_group):
                        groups[i % len(groups)].append(remaining_name)
                else:
                    # Wenn nur eine Gruppe übrig bleibt (z.B. weniger als group_size Namen)
                    groups.append(current_group)

    except ValueError:
        flash('Bitte gib eine gültige Zahl für die Gruppenanzahl oder Gruppengrösse ein.', 'error')
        return redirect(url_for('home'))
    except Exception as e:
        flash(f'Ein Fehler ist aufgetreten: {e}', 'error')
        return redirect(url_for('home'))

    # Speichern der verwendeten Namen und Einstellungen in der Session für die results-Seite
    session['generated_names'] = names
    session['group_settings'] = {
        'group_type': group_type,
        'num_groups': num_groups_str,
        'group_size': group_size_str
    }

    # Rendere die Ergebnisseite
    return render_template('results.html', groups=groups, all_names_json=json.dumps(names),
                           group_settings_json=json.dumps(session['group_settings']))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Benutzername existiert bereits. Bitte wähle einen anderen.', 'error')
        else:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registrierung erfolgreich! Du kannst dich jetzt anmelden.', 'success')
            # RENATO - NACH ERFOLGREICHER REGISTRIERUNG DIE DATEN WIEDERHERSTELLEN
            session['user_id'] = new_user.id
            if 'next_url' in session:
                next_url = session.pop('next_url')
                return redirect(next_url)
            return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Erfolgreich angemeldet!', 'success')
            # RENATO - NACH ERFOLGREICHEM LOGIN DIE DATEN WIEDERHERSTELLEN
            if 'next_url' in session:
                next_url = session.pop('next_url')
                return redirect(next_url)
            return redirect(url_for('home'))
        else:
            flash('Ungültiger Benutzername oder Passwort.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('selected_player_list_id_for_save', None) # Auch diese ID leeren beim Logout
    # RENATO - Beim Logout auch die temporären Daten löschen, falls vorhanden
    session.pop('temp_form_data', None)
    session.pop('temp_names', None)
    session.pop('temp_settings', None)
    session.pop('temp_player_list_id', None)
    flash('Du wurdest abgemeldet.', 'info')
    return redirect(url_for('home'))


@app.route('/save_player_list', methods=['POST'])
@login_required # Schützt diese Route
def save_player_list():
    list_name = request.form['list_name'].strip()
    player_names_json = request.form['players_json'] # Kommt jetzt als JSON-String aus JS

    if not list_name:
        flash('Bitte gib einen Namen für die Namensliste ein.', 'error')
        return redirect(url_for('home'))

    if not player_names_json: # Hier prüfen wir, ob die JSON-Daten nicht leer sind
        flash('Kann keine leere Namensliste speichern. Bitte füge Namen hinzu.', 'error')
        return redirect(url_for('home'))

    # Versuche, die ID der zu aktualisierenden Liste zu erhalten
    selected_player_list_id_for_update = request.form.get('selected_player_list_id_for_update')

    if selected_player_list_id_for_update:
        # Aktualisiere eine bestehende Liste
        player_list = PlayerList.query.filter_by(id=selected_player_list_id_for_update, user_id=g.user.id).first()
        if player_list:
            player_list.name = list_name
            player_list.players_json = player_names_json
            player_list.timestamp = datetime.utcnow() # Aktualisiere den Zeitstempel bei Update
            db.session.commit()
            flash(f'Namensliste "{list_name}" erfolgreich aktualisiert!', 'success')
        else:
            flash('Namensliste zum Aktualisieren nicht gefunden oder keine Berechtigung.', 'error')
    else:
        # Erstelle eine neue Liste
        new_player_list = PlayerList(
            name=list_name,
            players_json=player_names_json,
            user=g.user
        )
        db.session.add(new_player_list)
        db.session.commit()
        flash(f'Namensliste "{list_name}" erfolgreich gespeichert!', 'success')
        # Speichere die ID der neuen Liste in der Session für zukünftiges Speichern von Gruppen
        session['selected_player_list_id_for_save'] = new_player_list.id

    return redirect(url_for('home'))


@app.route('/my_player_lists')
@login_required # Schützt diese Route
def my_player_lists():
    # Lade alle PlayerLists des aktuell eingeloggten Benutzers und ordne sie nach dem neuesten Zeitstempel
    user_player_lists = PlayerList.query.filter_by(user=g.user).order_by(PlayerList.timestamp.desc()).all()
    return render_template('my_player_lists.html', user_player_lists=user_player_lists)


@app.route('/load_player_list/<int:list_id>')
@login_required
def load_player_list(list_id):
    player_list = PlayerList.query.filter_by(id=list_id, user_id=g.user.id).first()
    if not player_list:
        flash('Namensliste nicht gefunden oder keine Berechtigung.', 'error')
        return redirect(url_for('my_player_lists'))

    loaded_names = json.loads(player_list.players_json)
    flash(f'Namensliste "{player_list.name}" erfolgreich geladen! Die Namen wurden auf die Startseite übertragen. Du kannst jetzt Gruppen generieren oder die Liste bearbeiten.', 'success')

    # Temporäre Speicherung in der Session, damit home() sie abrufen kann
    session['temp_names'] = loaded_names
    session['selected_player_list_id_for_save'] = player_list.id # Setze diese ID direkt hier
    session.pop('temp_settings', None) # Stelle sicher, dass alte Einstellungen gelöscht werden

    return redirect(url_for('home'))

@app.route('/delete_player_list/<int:list_id>', methods=['POST'])
@login_required
def delete_player_list(list_id):
    player_list = PlayerList.query.filter_by(id=list_id, user_id=g.user.id).first()
    if not player_list:
        flash('Namensliste nicht gefunden oder keine Berechtigung.', 'error')
        return redirect(url_for('my_player_lists'))

    # Lösche die PlayerList und alle zugehörigen GeneratedGroups (dank cascade="all, delete-orphan")
    db.session.delete(player_list)
    db.session.commit()

    # Wenn die gelöschte Liste die aktuell ausgewählte war, diese aus der Session entfernen
    if session.get('selected_player_list_id_for_save') == list_id:
        session.pop('selected_player_list_id_for_save', None)
        session.pop('temp_names', None) # Auch temporäre Namen löschen, falls sie von dieser Liste waren
        session.pop('temp_settings', None)


    flash(f'Namensliste "{player_list.name}" und alle zugehörigen Gruppeneinteilungen erfolgreich gelöscht.', 'success')
    return redirect(url_for('my_player_lists'))


@app.route('/save_generated_group', methods=['POST'])
@login_required
def save_generated_group():
    group_name = request.form['group_name'].strip()
    # groups_json und all_names_json kommen jetzt aus versteckten Feldern von results.html
    groups_json = request.form['groups_json']
    all_names_json = request.form['all_names_json']
    group_settings_json = request.form['group_settings_json']


    player_list_id = session.get('selected_player_list_id_for_save')

    if not player_list_id:
        flash('Keine aktive Namensliste ausgewählt. Bitte wähle oder speichere zuerst eine Namensliste.', 'error')
        return redirect(url_for('home'))

    player_list = PlayerList.query.filter_by(id=player_list_id, user_id=g.user.id).first()
    if not player_list:
        flash('Die zugehörige Namensliste wurde nicht gefunden oder du hast keine Berechtigung.', 'error')
        return redirect(url_for('home'))

    # Es wird immer eine neue GeneratedGroup erstellt, auch wenn der Name derselbe ist
    # Wenn der Benutzer die gleiche Konstellation unter einem neuen Namen speichern will, ist das erlaubt.
    new_generated_group = GeneratedGroup(
        name=group_name if group_name else None, # Erlaube leere Namen
        groups_json=groups_json,
        all_names_json=all_names_json,
        group_settings_json=group_settings_json,
        player_list=player_list
    )
    db.session.add(new_generated_group)
    db.session.commit()
    flash(f'Gruppeneinteilung "{group_name if group_name else "Ohne Namen"}" erfolgreich gespeichert!', 'success')
    return redirect(url_for('my_player_lists'))


@app.route('/load_generated_group/<int:group_id>')
@login_required
def load_generated_group(group_id):
    generated_group = GeneratedGroup.query.filter_by(id=group_id).first()

    if not generated_group:
        flash("Gruppeneinteilung nicht gefunden.", 'error')
        return redirect(url_for('my_player_lists'))

    # Stelle sicher, dass der Benutzer die übergeordnete PlayerList besitzt
    if generated_group.player_list.user_id != g.user.id:
        flash("Du hast keine Berechtigung, diese Gruppeneinteilung zu laden.", 'error')
        return redirect(url_for('my_player_lists'))

    loaded_names = json.loads(generated_group.all_names_json)
    loaded_settings = json.loads(generated_group.group_settings_json)

    flash(f'Gruppeneinteilung "{generated_group.name or "Ohne Namen"}" erfolgreich geladen! Die Namen und Einstellungen wurden auf die Startseite übertragen. Du kannst die Gruppen erneut generieren oder speichern.', 'success')

    # Temporäre Speicherung in der Session, damit home() sie abrufen kann
    session['temp_names'] = loaded_names
    session['temp_settings'] = loaded_settings
    session['temp_player_list_id'] = generated_group.player_list_id # Die ID der übergeordneten PlayerList

    return redirect(url_for('home'))


@app.route('/delete_generated_group/<int:group_id>', methods=['POST'])
@login_required
def delete_generated_group(group_id):
    generated_group = GeneratedGroup.query.filter_by(id=group_id).first()

    if not generated_group:
        flash("Gruppeneinteilung nicht gefunden.", 'error')
        return redirect(url_for('my_player_lists'))

    # Stelle sicher, dass der Benutzer die übergeordnete PlayerList besitzt
    if generated_group.player_list.user_id != g.user.id:
        flash("Du hast keine Berechtigung, diese Gruppeneinteilung zu löschen.", 'error')
        return redirect(url_for('my_player_lists'))

    db.session.delete(generated_group)
    db.session.commit()
    flash(f'Gruppeneinteilung "{generated_group.name or "Ohne Namen"}" erfolgreich gelöscht.', 'success')
    return redirect(url_for('my_player_lists'))


if __name__ == '__main__':
    app.run(debug=True)
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
    password_hash = db.Column(db.String(120), nullable=False)
    # Beziehung zu PlayerList: Ein User kann mehrere PlayerLists haben
    player_lists = db.relationship('PlayerList', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Neues Modell für gespeicherte Namenslisten
class PlayerList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    players_json = db.Column(db.Text, nullable=False) # Speichert die Liste der Namen als JSON-String
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # Beziehung zu GeneratedGroup: Eine PlayerList kann mehrere GeneratedGroups haben
    generated_groups = db.relationship('GeneratedGroup', backref='player_list', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<PlayerList {self.name}>'

# Neues Modell für gespeicherte, generierte Gruppenkonstellationen
class GeneratedGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_list_id = db.Column(db.Integer, db.ForeignKey('player_list.id'), nullable=False)
    name = db.Column(db.String(100), nullable=True) # Name der spezifischen Gruppeneinteilung
    selected_players_json = db.Column(db.Text, nullable=False) # Die Namen, die für diese Generierung verwendet wurden
    group_settings_json = db.Column(db.Text, nullable=False) # Die Einstellungen (num_groups/group_size)
    generated_groups_json = db.Column(db.Text, nullable=False) # Das eigentliche Gruppenergebnis
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<GeneratedGroup {self.name} for PlayerList {self.player_list_id}>'

# Erstelle die Datenbanktabellen (sollte einmalig ausgeführt werden)
with app.app_context():
    db.create_all()

# --- Login-Management ---
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
            flash('Du musst angemeldet sein, um diese Seite aufzurufen.', 'error')
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

# --- Routen ---
@app.route('/')
def home():
    loaded_names = session.pop('temp_names', None)
    loaded_settings = session.pop('temp_settings', None)
    selected_player_list_id = session.pop('temp_player_list_id', None)

    # Wenn wir von einer geladenen Liste kommen oder nach Login/Reg. Daten wiederherstellen
    if loaded_names is not None:
        return render_template('index.html', loaded_names=loaded_names, loaded_settings=loaded_settings, selected_player_list_id=selected_player_list_id)
    
    return render_template('index.html')

@app.route('/register', methods=('GET', 'POST'))
def register():
    if g.user:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Benutzername ist erforderlich.'
        elif not password:
            error = 'Passwort ist erforderlich.'
        elif User.query.filter_by(username=username).first() is not None:
            error = f"Benutzername {username} ist bereits registriert."

        if error is None:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            flash('Registrierung erfolgreich! Du bist jetzt angemeldet.', 'success')
            return redirect(url_for('home')) # Könnten hier auch zu einem 'welcome'-Screen leiten
        
        flash(error, 'error')

    return render_template('register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if g.user:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'Falscher Benutzername.'
        elif not user.check_password(password):
            error = 'Falsches Passwort.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            flash('Anmeldung erfolgreich!', 'success')
            return redirect(url_for('home'))
        
        flash(error, 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Du wurdest abgemeldet.', 'info')
    return redirect(url_for('home'))

@app.route('/generate', methods=['POST'])
def generate_groups():
    names = [name.strip() for name in request.form.getlist('name[]') if name.strip()]
    group_type = request.form['group_type']
    num_groups = request.form.get('num_groups', type=int)
    group_size = request.form.get('group_size', type=int)
    selected_player_list_id = request.form.get('selected_player_list_id', type=int)

    if not names:
        flash('Bitte gib Namen ein, um Gruppen zu generieren.', 'error')
        return redirect(url_for('home'))

    # Speichere die aktuellen Eingaben temporär in der Session, falls der User sich anmelden/registrieren möchte
    session['temp_names'] = names
    session['temp_group_type'] = group_type
    session['temp_num_groups'] = num_groups
    session['temp_group_size'] = group_size
    session['selected_player_list_id_for_save'] = selected_player_list_id # Speichere diese ID für das Speichern der GeneratedGroup

    random.shuffle(names)
    groups = []
    error_message = None

    if group_type == 'num_groups':
        if not num_groups or num_groups <= 0:
            error_message = "Bitte gib eine gültige Anzahl an Gruppen ein."
        elif num_groups > len(names):
            error_message = "Du kannst nicht mehr Gruppen als Personen erstellen."
        else:
            avg = len(names) // num_groups
            remainder = len(names) % num_groups
            start = 0
            for i in range(num_groups):
                end = start + avg + (1 if i < remainder else 0)
                groups.append(names[start:end])
                start = end
    elif group_type == 'group_size':
        if not group_size or group_size <= 0:
            error_message = "Bitte gib eine gültige Gruppengrösse ein."
        elif group_size > len(names):
            error_message = "Die Gruppengrösse kann nicht grösser sein als die Anzahl der Personen."
        else:
            current_names = list(names) # Erstelle eine Kopie, um Elemente zu entfernen
            while len(current_names) >= group_size:
                group = random.sample(current_names, group_size)
                for person in group:
                    current_names.remove(person)
                groups.append(group)
            if current_names: # Restliche Personen in bestehende Gruppen verteilen
                for i, person in enumerate(current_names):
                    groups[i % len(groups)].append(person)
    else:
        error_message = "Ungültiger Gruppentyp ausgewählt."

    if error_message:
        flash(error_message, 'error')
        return redirect(url_for('home'))
    
    # Speichere die generierten Gruppen und Einstellungen in der Session für die results.html
    # Wir speichern die ursprüngliche Liste der Namen, die für die Generierung verwendet wurde,
    # sowie die Einstellungen und die tatsächlich generierten Gruppen.
    session['last_generated_data'] = {
        'names': names, # Die Liste der Namen, die für diese Generierung verwendet wurde
        'group_settings': {'group_type': group_type, 'num_groups': num_groups, 'group_size': group_size},
        'groups': groups
    }

    return render_template('results.html', groups=groups, all_names_json=json.dumps(names), group_settings_json=json.dumps({'group_type': group_type, 'num_groups': num_groups, 'group_size': group_size}))

@app.route('/save_player_list', methods=['POST'])
@login_required
def save_player_list():
    list_name = request.form.get('list_name')
    names = request.form.getlist('name[]') # Kommt als Liste von Namen
    names = [name.strip() for name in names if name.strip()] # Bereinigen

    if not list_name or not list_name.strip():
        flash("Bitte gib einen Namen für die Namensliste ein.", 'error')
        return redirect(url_for('home'))
    
    if not names:
        flash("Die Namensliste kann nicht leer sein.", 'error')
        return redirect(url_for('home'))

    # Konvertiere die Liste der Namen in einen JSON-String
    names_json = json.dumps(names)

    # Überprüfen, ob eine existierende Liste aktualisiert werden soll (falls ID übergeben)
    # selected_player_list_id = request.form.get('selected_player_list_id', type=int) # Aktuell noch nicht im Formular
    # if selected_player_list_id:
    #     player_list = PlayerList.query.get(selected_player_list_id)
    #     if player_list and player_list.user_id == g.user.id:
    #         player_list.name = list_name.strip()
    #         player_list.players_json = names_json
    #         db.session.commit()
    #         flash(f'Namensliste "{list_name.strip()}" erfolgreich aktualisiert!', 'success')
    #         return redirect(url_for('my_player_lists'))

    new_player_list = PlayerList(
        user_id=g.user.id,
        name=list_name.strip(),
        players_json=names_json
    )
    db.session.add(new_player_list)
    db.session.commit()
    flash(f'Namensliste "{list_name.strip()}" erfolgreich gespeichert!', 'success')
    return redirect(url_for('my_player_lists'))

@app.route('/my_player_lists')
@login_required
def my_player_lists():
    user_player_lists = PlayerList.query.filter_by(user_id=g.user.id).order_by(PlayerList.timestamp.desc()).all()
    return render_template('my_player_lists.html', user_player_lists=user_player_lists)

@app.route('/load_player_list/<int:list_id>')
@login_required
def load_player_list(list_id):
    player_list = PlayerList.query.filter_by(id=list_id, user_id=g.user.id).first()
    if not player_list:
        flash("Namensliste nicht gefunden oder keine Berechtigung.", 'error')
        return redirect(url_for('my_player_lists'))

    loaded_names = json.loads(player_list.players_json) # Namen aus JSON string parsen
    
    flash(f'Namensliste "{player_list.name}" erfolgreich geladen!', 'success')
    # Leite zur Startseite um und übergebe die geladenen Namen und die ID der Liste
    return render_template('index.html', loaded_names=loaded_names, loaded_settings={}, selected_player_list_id=player_list.id)

@app.route('/delete_player_list/<int:list_id>', methods=['POST'])
@login_required
def delete_player_list(list_id):
    player_list = PlayerList.query.filter_by(id=list_id, user_id=g.user.id).first()
    if not player_list:
        flash("Namensliste nicht gefunden oder keine Berechtigung.", 'error')
        return redirect(url_for('my_player_lists'))

    db.session.delete(player_list)
    db.session.commit()
    flash(f'Namensliste "{player_list.name}" und zugehörige Gruppeneinteilungen erfolgreich gelöscht!', 'success')
    return redirect(url_for('my_player_lists'))

@app.route('/save_generated_group', methods=['POST'])
@login_required
def save_generated_group():
    group_name = request.form.get('group_name')
    player_list_id = request.form.get('player_list_id', type=int) # Die ID der Eltern-PlayerList
    all_names_json = request.form.get('all_names_json') # Die für diese Generierung verwendeten Namen
    group_settings_json = request.form.get('group_settings_json') # Die Einstellungen für diese Generierung

    if not group_name or not group_name.strip():
        flash("Bitte gib einen Namen für die Gruppeneinteilung ein.", 'error')
        # Versuche, die Daten in der Session zu erhalten und zurück zum results.html zu leiten
        last_generated_data = session.get('last_generated_data')
        if last_generated_data:
            return render_template('results.html', groups=last_generated_data['groups'], 
                                   all_names_json=json.dumps(last_generated_data['names']), 
                                   group_settings_json=json.dumps(last_generated_data['group_settings']))
        return redirect(url_for('home'))
    
    if not player_list_id:
        flash("Fehler: Eine Gruppeneinteilung kann nur gespeichert werden, wenn eine Namensliste aktiv ist. Bitte lade oder speichere zuerst eine Namensliste.", 'error')
        # Auch hier, versuchen die Daten zu erhalten
        last_generated_data = session.get('last_generated_data')
        if last_generated_data:
            return render_template('results.html', groups=last_generated_data['groups'], 
                                   all_names_json=json.dumps(last_generated_data['names']), 
                                   group_settings_json=json.dumps(last_generated_data['group_settings']))
        return redirect(url_for('home'))

    player_list = PlayerList.query.filter_by(id=player_list_id, user_id=g.user.id).first()
    if not player_list:
        flash("Fehler: Zugehörige Namensliste nicht gefunden oder keine Berechtigung.", 'error')
        # Auch hier, versuchen die Daten zu erhalten
        last_generated_data = session.get('last_generated_data')
        if last_generated_data:
            return render_template('results.html', groups=last_generated_data['groups'], 
                                   all_names_json=json.dumps(last_generated_data['names']), 
                                   group_settings_json=json.dumps(last_generated_data['group_settings']))
        return redirect(url_for('home'))
    
    # Hole die tatsächlich generierten Gruppen aus der Session
    generated_groups_result = session.get('last_generated_data', {}).get('groups')
    if not generated_groups_result:
        flash("Fehler: Keine Gruppen zum Speichern gefunden. Bitte generiere zuerst Gruppen.", 'error')
        return redirect(url_for('home'))
    
    generated_groups_json = json.dumps(generated_groups_result)

    new_generated_group = GeneratedGroup(
        player_list_id=player_list.id,
        name=group_name.strip(),
        selected_players_json=all_names_json,
        group_settings_json=group_settings_json,
        generated_groups_json=generated_groups_json
    )
    db.session.add(new_generated_group)
    db.session.commit()
    flash(f'Gruppeneinteilung "{group_name.strip()}" erfolgreich gespeichert!', 'success')
    return redirect(url_for('my_player_lists'))

# Route, um eine spezifische GeneratedGroup zu laden (z.B. für erneutes Generieren/Bearbeiten)
@app.route('/load_generated_group/<int:group_id>')
@login_required
def load_generated_group(group_id):
    generated_group = GeneratedGroup.query.filter_by(id=group_id).first()

    if not generated_group:
        flash("Gruppeneinteilung nicht gefunden.", 'error')
        return redirect(url_for('my_player_lists'))

    # Ensure the user owns the parent PlayerList before loading the group
    if generated_group.player_list.user_id != g.user.id:
        flash("Du hast keine Berechtigung, diese Gruppeneinteilung zu laden.", 'error')
        return redirect(url_for('my_player_lists'))

    loaded_names_data = json.loads(generated_group.selected_players_json)
    loaded_names = loaded_names_data # Hier sind die Namen bereits eine Liste von Strings

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
    flash(f'Gruppeneinteilung "{generated_group.name or "Ohne Namen"}" erfolgreich gelöscht!', 'success')
    return redirect(url_for('my_player_lists'))

if __name__ == '__main__':
    app.run(debug=True)
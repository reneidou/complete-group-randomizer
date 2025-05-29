from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random
import os
import json # Benötigen wir, um JSON-Daten zu speichern
from functools import wraps

app = Flask(__name__)

# --- Datenbank Konfiguration ---
# Pfad zur SQLite-Datenbankdatei
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Dein_wirklich_sehr_geheimer_schluessel_bitte_aendern_im_produktivbetrieb_123ABC' # WICHTIG: Ersetze dies!

db = SQLAlchemy(app)

# Erstelle den instance-Ordner, falls er nicht existiert
if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)

# Registriere den 'fromjson'-Filter für Jinja2
app.jinja_env.filters['fromjson'] = json.loads

# --- Datenbank-Modelle definieren ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    # Beziehung zu PlayerList: Ein User kann mehrere PlayerLists haben
    player_lists = db.relationship('PlayerList', backref='user', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.username}>'

class PlayerList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    players_json = db.Column(db.Text, nullable=False) # Speichert die Liste der Namen als JSON-String
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    # Beziehung zu GeneratedGroup: Eine PlayerList kann mehrere GeneratedGroups haben
    generated_groups = db.relationship('GeneratedGroup', backref='player_list', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<PlayerList {self.name}>'

class GeneratedGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_list_id = db.Column(db.Integer, db.ForeignKey('player_list.id'), nullable=False)
    name = db.Column(db.String(100), nullable=True) # Name der spezifischen Gruppeneinteilung
    selected_players_json = db.Column(db.Text, nullable=False) # Die für diese Generierung verwendeten Spieler (als JSON-String)
    group_settings_json = db.Column(db.Text, nullable=False) # Einstellungen (num_groups/group_size) als JSON-String
    generated_groups_json = db.Column(db.Text, nullable=False) # Die eigentlichen Gruppen als JSON-String
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<GeneratedGroup {self.name}>'


# --- Helper functions ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Bitte melde dich an, um diese Seite zu sehen.", 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Context Processor for current user ---
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

# --- Routes ---
@app.route('/')
def home():
    # Beim ersten Laden oder wenn keine Spielerliste ausgewählt ist, zeige leere Felder
    # oder Standard-Startwerte an.
    return render_template('index.html', loaded_names=[], loaded_settings={})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user:
        flash("Du bist bereits angemeldet.", 'info')
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        if not username or not password:
            flash("Benutzername und Passwort dürfen nicht leer sein.", 'error')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Benutzername existiert bereits. Bitte wähle einen anderen.", 'error')
            return redirect(url_for('register'))

        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registrierung erfolgreich! Bitte melde dich an.", 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        flash("Du bist bereits angemeldet.", 'info')
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            flash(f"Willkommen zurück, {user.username}!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Ungültiger Benutzername oder Passwort.", 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Du wurdest abgemeldet.", 'info')
    return redirect(url_for('home'))

@app.route('/generate', methods=['POST'])
def generate_groups():
    names = [name.strip() for name in request.form.getlist('name[]') if name.strip()]
    group_type = request.form['group_type']
    num_groups = request.form.get('num_groups', type=int)
    group_size = request.form.get('group_size', type=int)
    selected_player_list_id = request.form.get('selected_player_list_id', type=int)

    if not names:
        flash("Bitte gib Namen ein, um Gruppen zu generieren.", 'error')
        return redirect(url_for('home'))

    random.shuffle(names)
    groups = []

    if group_type == 'num_groups' and num_groups:
        if num_groups <= 0:
            flash("Anzahl der Gruppen muss mindestens 1 sein.", 'error')
            return redirect(url_for('home'))
        if num_groups > len(names):
            flash("Du kannst nicht mehr Gruppen als Personen erstellen.", 'error')
            return redirect(url_for('home'))

        # Initialisiere leere Gruppen
        groups = [[] for _ in range(num_groups)]
        # Verteile die Namen gleichmässig auf die Gruppen
        for i, name in enumerate(names):
            groups[i % num_groups].append(name)

    elif group_type == 'group_size' and group_size:
        if group_size <= 0:
            flash("Die Gruppengrösse muss mindestens 1 sein.", 'error')
            return redirect(url_for('home'))
        if group_size > len(names):
            flash("Die Gruppengrösse kann nicht grösser sein als die Anzahl der Personen.", 'error')
            return redirect(url_for('home'))

        # Erstelle Gruppen basierend auf der Gruppengrösse
        for i in range(0, len(names), group_size):
            groups.append(names[i:i + group_size])
    else:
        flash("Ungültige Gruppeneinstellungen.", 'error')
        return redirect(url_for('home'))

    # Speichern der Konfiguration in der Session, um sie nach dem Speichern anzuzeigen
    session['generated_groups'] = groups
    session['generated_names'] = names # Alle ursprünglich eingegebenen Namen
    session['generated_group_settings'] = {'group_type': group_type, 'num_groups': num_groups, 'group_size': group_size}
    session['selected_player_list_id_for_save'] = selected_player_list_id


    return render_template('results.html', groups=groups,
                           all_names_json=json.dumps(names), # Als JSON-String übergeben
                           group_settings_json=json.dumps({'group_type': group_type, 'num_groups': num_groups, 'group_size': group_size})) # Als JSON-String übergeben


@app.route('/save_generated_group', methods=['POST'])
@login_required
def save_generated_group():
    group_name = request.form.get('group_name')
    player_list_id = request.form.get('player_list_id', type=int)

    generated_groups_data = session.get('generated_groups')
    generated_names_data = session.get('generated_names')
    generated_group_settings_data = session.get('generated_group_settings')


    if not group_name or not generated_groups_data or not generated_names_data or not generated_group_settings_data:
        flash("Fehler: Gruppeneinteilung konnte nicht gespeichert werden. Daten fehlen.", 'error')
        return redirect(url_for('home'))

    # Stelle sicher, dass die zugehörige PlayerList dem angemeldeten Benutzer gehört
    player_list = PlayerList.query.filter_by(id=player_list_id, user_id=g.user.id).first()
    if not player_list:
        flash("Fehler: Zugehörige Namensliste nicht gefunden oder keine Berechtigung.", 'error')
        return redirect(url_for('home'))


    new_generated_group = GeneratedGroup(
        player_list_id=player_list.id,
        name=group_name.strip(),
        selected_players_json=json.dumps(generated_names_data), # Die Liste der Personen, die für DIESE Gruppengenerierung verwendet wurden
        group_settings_json=json.dumps(generated_group_settings_data),
        generated_groups_json=json.dumps(generated_groups_data)
    )
    db.session.add(new_generated_group)
    db.session.commit()

    # Nach dem Speichern die Session-Daten löschen
    session.pop('generated_groups', None)
    session.pop('generated_names', None)
    session.pop('generated_group_settings', None)
    session.pop('selected_player_list_id_for_save', None)


    flash(f'Gruppeneinteilung "{group_name.strip()}" erfolgreich gespeichert!', 'success')
    return redirect(url_for('my_player_lists', selected_list_id=player_list.id)) # Optional: Direkt zur PlayerList mit den neuen Gruppen

@app.route('/save_player_list', methods=['POST'])
@login_required
def save_player_list():
    names = [name.strip() for name in request.form.getlist('name[]') if name.strip()]
    list_name = request.form.get('list_name')
    player_list_id = request.form.get('player_list_id_for_update', type=int) # Für den Fall, dass eine bestehende Liste aktualisiert wird

    if not names:
        flash("Bitte gib Namen ein, um eine Namensliste zu speichern.", 'error')
        return redirect(url_for('home'))

    if not list_name.strip():
        flash("Bitte gib einen Namen für die Namensliste ein.", 'error')
        return redirect(url_for('home'))

    if player_list_id: # Aktualisieren einer bestehenden Liste
        player_list = PlayerList.query.filter_by(id=player_list_id, user_id=g.user.id).first()
        if player_list:
            player_list.name = list_name.strip()
            player_list.players_json = json.dumps(names)
            db.session.commit()
            flash(f'Namensliste "{list_name.strip()}" erfolgreich aktualisiert!', 'success')
        else:
            flash("Fehler: Namensliste nicht gefunden oder keine Berechtigung.", 'error')
    else: # Neue Liste speichern
        new_player_list = PlayerList(
            user_id=g.user.id,
            name=list_name.strip(),
            players_json=json.dumps(names)
        )
        db.session.add(new_player_list)
        db.session.commit()
        flash(f'Namensliste "{list_name.strip()}" erfolgreich gespeichert!', 'success')

    return redirect(url_for('my_player_lists'))

@app.route('/my_player_lists')
@login_required
def my_player_lists():
    user_player_lists = PlayerList.query.filter_by(user_id=g.user.id).order_by(PlayerList.timestamp.desc()).all()
    selected_list_id = request.args.get('selected_list_id', type=int)

    # Lade die GeneratedGroups für die ausgewählte PlayerList
    selected_player_list_groups = []
    if selected_list_id:
        selected_player_list = PlayerList.query.filter_by(id=selected_list_id, user_id=g.user.id).first()
        if selected_player_list:
            selected_player_list_groups = GeneratedGroup.query.filter_by(player_list_id=selected_list_id).order_by(GeneratedGroup.timestamp.desc()).all()


    return render_template('my_player_lists.html',
                           user_player_lists=user_player_lists,
                           selected_list_id=selected_list_id,
                           selected_player_list_groups=selected_player_list_groups)

@app.route('/delete_player_list/<int:list_id>', methods=['POST'])
@login_required
def delete_player_list(list_id):
    player_list = PlayerList.query.filter_by(id=list_id, user_id=g.user.id).first()
    if player_list:
        db.session.delete(player_list)
        db.session.commit()
        flash(f'Namensliste "{player_list.name}" und zugehörige Gruppeneinteilungen erfolgreich gelöscht!', 'success')
    else:
        flash("Fehler: Namensliste nicht gefunden oder keine Berechtigung zum Löschen.", 'error')
    return redirect(url_for('my_player_lists'))

@app.route('/delete_generated_group/<int:group_id>', methods=['POST'])
@login_required
def delete_generated_group(group_id):
    generated_group = GeneratedGroup.query.filter_by(id=group_id).first()

    if not generated_group:
        flash("Gruppeneinteilung nicht gefunden.", 'error')
        return redirect(url_for('my_player_lists'))

    # Sicherstellen, dass der Benutzer der Besitzer der übergeordneten PlayerList ist
    if generated_group.player_list.user_id != g.user.id:
        flash("Du hast keine Berechtigung, diese Gruppeneinteilung zu löschen.", 'error')
        return redirect(url_for('my_player_lists'))

    parent_player_list_id = generated_group.player_list_id # Speichern der ID vor dem Löschen
    group_name = generated_group.name

    db.session.delete(generated_group)
    db.session.commit()
    flash(f'Gruppeneinteilung "{group_name or "Ohne Namen"}" erfolgreich gelöscht!', 'success')

    # Nach dem Löschen zur PlayerList zurückkehren, zu der die Gruppe gehörte
    return redirect(url_for('my_player_lists', selected_list_id=parent_player_list_id))


@app.route('/load_player_list/<int:list_id>')
@login_required
def load_player_list(list_id):
    player_list = PlayerList.query.filter_by(id=list_id, user_id=g.user.id).first()
    if not player_list:
        flash("Namensliste nicht gefunden oder keine Berechtigung.", 'error')
        return redirect(url_for('my_player_lists'))

    loaded_names = json.loads(player_list.players_json)
    flash(f'Namensliste "{player_list.name}" erfolgreich geladen!', 'success')
    return render_template('index.html', loaded_names=loaded_names, loaded_settings={}, selected_player_list_id=player_list.id)


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
    loaded_names = [player['name'] for player in loaded_names_data] # Extract names only

    loaded_settings = json.loads(generated_group.group_settings_json)
    
    # We pass the ID of the parent player list
    flash(f'Gruppeneinteilung "{generated_group.name or "Ohne Namen"}" erfolgreich geladen!', 'success')
    return render_template('index.html', loaded_names=loaded_names, loaded_settings=loaded_settings, selected_player_list_id=generated_group.player_list_id)


# --- Initial database creation (run once) ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
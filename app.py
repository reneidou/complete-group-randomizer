from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random
import os
import json # Benötigen wir, um JSON-Daten zu speichern

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

# --- Datenbank-Modelle definieren ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    teams = db.relationship('SavedTeamConfig', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class SavedTeamConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # User kann NULL sein für Gäste
    name = db.Column(db.String(100), nullable=False) # Name der gespeicherten Konfiguration (z.B. "Meine Volleyball-Gruppe")
    players_json = db.Column(db.Text, nullable=False) # JSON-String der Spieler (mit optionalen Ratings/Rollen)
    group_settings_json = db.Column(db.Text, nullable=False) # JSON-String der Gruppeneinstellungen
    timestamp = db.Column(db.DateTime, default=db.func.now())
    results = db.relationship('SavedResult', backref='team_config', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<SavedTeamConfig {self.name}>'

class SavedResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    config_id = db.Column(db.Integer, db.ForeignKey('saved_team_config.id'), nullable=False)
    result_json = db.Column(db.Text, nullable=False) # JSON-String des Gruppeneinteilungs-Resultats
    timestamp = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<SavedResult {self.id}>'

# --- Jinja2 Custom Filters ---
# Filter zum Konvertieren eines JSON-Strings in ein Python-Objekt
def from_json_filter(value):
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return [] # Rückgabe einer leeren Liste oder eines geeigneten Standardwerts bei Fehler

app.jinja_env.filters['fromjson'] = from_json_filter

# --- Hooks und Helper-Funktionen ---
# Wird vor jeder Anfrage ausgeführt, um den angemeldeten Benutzer zu laden
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

# --- Routen der Anwendung ---

@app.route('/')
def home():
    # Beim ersten Laden der Seite oder bei der Rückkehr zur Home-Seite
    # werden keine vorgeladenen Daten übergeben
    return render_template('index.html')

# --- Registrierungs-Route ---
@app.route('/register', methods=('GET', 'POST'))
def register():
    if g.user: # Wenn der Benutzer bereits angemeldet ist, direkt zur Home-Seite umleiten
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
            error = f"Benutzername {username} ist bereits vergeben."

        if error is None:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registrierung erfolgreich! Du kannst dich jetzt anmelden.', 'success')
            return redirect(url_for('login'))
        flash(error, 'error')
    return render_template('register.html')

# --- Login-Route ---
@app.route('/login', methods=('GET', 'POST'))
def login():
    if g.user: # Wenn der Benutzer bereits angemeldet ist, direkt zur Home-Seite umleiten
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'Ungültiger Benutzername.'
        elif not user.check_password(password):
            error = 'Falsches Passwort.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            flash('Erfolgreich angemeldet!', 'success')
            return redirect(url_for('home')) # Oder zu einer Dashboard-Seite
        flash(error, 'error')
    return render_template('login.html')

# --- Logout-Route ---
@app.route('/logout')
def logout():
    session.clear()
    flash('Du wurdest abgemeldet.', 'info')
    return redirect(url_for('home'))

# --- Gruppen-Generierungs-Route ---
@app.route('/generate', methods=['POST'])
def generate_groups():
    names = [name.strip() for name in request.form.getlist('name[]') if name.strip()]
    group_type = request.form['group_type']

    if not names:
        flash("Bitte gib mindestens einen Namen ein, um Gruppen zu generieren.", 'error')
        return render_template('index.html')

    num_people = len(names)
    random.shuffle(names)

    groups = []

    if group_type == 'num_groups':
        try:
            num_groups = int(request.form['num_groups'])
            if num_groups <= 0:
                raise ValueError("Anzahl Gruppen muss positiv sein.")
            if num_groups > num_people:
                num_groups = num_people
                flash("Es wurden nicht mehr Gruppen als Personen erstellt.", 'info')
        except ValueError:
            flash("Ungültige Anzahl Gruppen eingegeben.", 'error')
            return render_template('index.html')

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
            flash("Ungültige Gruppengrösse eingegeben.", 'error')
            return render_template('index.html')

        if group_size == 0:
             flash("Gruppengrösse kann nicht Null sein.", 'error')
             return render_template('index.html')

        for i in range(0, num_people, group_size):
            group = names[i:i + group_size]
            groups.append(group)

    # Hier ist die Korrektur: JSON-Daten vorbereiten, bevor das Template gerendert wird
    all_names_flat = [name for group in groups for name in group] # Flache Liste aller Namen
    players_json_str = json.dumps(all_names_flat) # Konvertiere Liste zu JSON-String

    # Gruppeneinstellungen erfassen (kann je nach Bedarf detaillierter sein)
    group_settings_data = {
        'group_type': group_type,
        'num_groups': int(request.form.get('num_groups')) if group_type == 'num_groups' else None,
        'group_size': int(request.form.get('group_size')) if group_type == 'group_size' else None
    }
    group_settings_json_str = json.dumps(group_settings_data) # Konvertiere Dictionary zu JSON-String

    return render_template(
        'results.html',
        groups=groups,
        all_names_json=players_json_str,
        group_settings_json=group_settings_json_str
    )

@app.route('/save_config', methods=['POST'])
def save_config():
    if not g.user:
        flash("Bitte melde dich an, um Teamkonfigurationen zu speichern.", 'error')
        return redirect(url_for('login'))

    names_str = request.form.get('all_names_json')
    group_settings_str = request.form.get('group_settings_json')
    config_name = request.form.get('config_name')

    if not names_str or not group_settings_str or not config_name:
        flash("Fehler: Konfiguration konnte nicht gespeichert werden. Daten fehlen.", 'error')
        return redirect(url_for('home'))

    if not config_name.strip():
        flash("Bitte gib einen Namen für die Konfiguration ein.", 'error')
        return redirect(url_for('home'))

    new_config = SavedTeamConfig(
        user_id=g.user.id,
        name=config_name.strip(),
        players_json=names_str,
        group_settings_json=group_settings_str
    )
    db.session.add(new_config)
    db.session.commit()
    flash(f'Teamkonfiguration "{config_name.strip()}" erfolgreich gespeichert!', 'success')
    return redirect(url_for('my_teams'))

@app.route('/my_teams')
def my_teams():
    if not g.user:
        flash("Bitte melde dich an, um deine gespeicherten Teams zu sehen.", 'error')
        return redirect(url_for('login'))

    user_teams = SavedTeamConfig.query.filter_by(user_id=g.user.id).order_by(SavedTeamConfig.timestamp.desc()).all()
    return render_template('my_teams.html', user_teams=user_teams)

# --- NEUE ROUTE: Konfiguration laden ---
@app.route('/load_config/<int:config_id>')
def load_config(config_id):
    if not g.user:
        flash("Bitte melde dich an, um Konfigurationen zu laden.", 'error')
        return redirect(url_for('login'))

    config_to_load = SavedTeamConfig.query.filter_by(id=config_id, user_id=g.user.id).first()

    if not config_to_load:
        flash("Konfiguration nicht gefunden oder du hast keine Berechtigung, sie zu laden.", 'error')
        return redirect(url_for('my_teams'))

    # JSON-Strings in Python-Objekte umwandeln
    loaded_names = json.loads(config_to_load.players_json)
    loaded_settings = json.loads(config_to_load.group_settings_json)

    flash(f'Konfiguration "{config_to_load.name}" erfolgreich geladen! Du kannst sie jetzt anpassen und erneut generieren.', 'success')

    # Übergabe der geladenen Daten an das index.html-Template
    return render_template(
        'index.html',
        loaded_names=loaded_names,
        loaded_settings=loaded_settings
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
from flask import Flask, render_template, request # 'request' importiert

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST']) # Diese Route nimmt POST-Anfragen entgegen
def generate_groups():
    names = request.form.getlist('name[]') # Holt alle Namen
    group_type = request.form['group_type'] # Holt den ausgewählten Gruppentyp

    if group_type == 'num_groups':
        num_groups = request.form['num_groups']
        group_setting = f"Anzahl Gruppen: {num_groups}"
    else: # group_type == 'group_size'
        group_size = request.form['group_size']
        group_setting = f"Gruppengrösse: {group_size}"

    # Nur zum Testen: Gib die empfangenen Daten im Browser zurück
    return f"Empfangene Namen: {', '.join(names)}<br>Gruppeneinstellung: {group_setting}"

if __name__ == '__main__':
    app.run(debug=True)
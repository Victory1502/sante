from models import *



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/inscrire', methods=['GET', 'POST'])
def inscrire():
    if request.method == 'POST':
        name = request.form['name']
        firstname = request.form['firstname']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        
        # Créer un nouvel utilisateur
        new_user = User(name=name, Firstname=firstname, email=email, MDP=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Inscription réussie!', 'success')
        return redirect(url_for('login'))  # Redirige vers la page de connexion

    return render_template('inscription.html')

@app.route('/inscription')
def inscription():
    return render_template('inscription.html')


@app.route('/connexion')
def connexion():
    return render_template('connexion.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Rechercher l'utilisateur par son email
        user = User.query.filter_by(email=email).first()

        # Vérifier si l'utilisateur existe et si le mot de passe est correct
        if user and user.check_password(password):
            session['user_id'] = user.id  # Enregistrer l'ID utilisateur dans la session
            session['role'] = user.role  # Enregistrer le rôle de l'utilisateur (patient ou doctor)
            flash('Connexion réussie !', 'success')
            return redirect(url_for('dashboard'))  # Rediriger vers un tableau de bord ou page d'accueil après connexion
        else:
            flash('Email ou mot de passe incorrect', 'danger')
    
    return render_template('login.html')  # Affiche le formulaire de connexion


@app.route('/predict', methods=['POST'])
def predict():
    # Récupérer les données du formulaire
    gender = request.form.get('gender')
    age = request.form.get('age')
    smoking = request.form.get('smoking')
    yellow_eyes = request.form.get('yeux')
    anxiety = request.form.get('anxiete')
    peer_pressure = request.form.get('peer_pressure')
    chronic_disease = request.form.get('chronic_disease')
    fatigue = request.form.get('fatigue')
    allergies = request.form.get('allergies')
    wheezing = request.form.get('wheezing')
    alcohol_consumption = request.form.get('alcohol_consumption')
    coughing = request.form.get('coughing')
    shortness_of_breath = request.form.get('shortness_of_breath')
    swallowing_difficulty = request.form.get('swallowing_difficulty')
    chest_pain = request.form.get('chest_pain')

    # Optionnel: afficher les données récupérées dans la console
    print(f"Genre: {gender}, Âge: {age}, Fume: {smoking}")

    # Faire quelque chose avec les données récupérées
    # par exemple, les envoyer à un modèle de prédiction, les stocker, etc.

    # Renvoyer une réponse ou rediriger
    return render_template('login.html')  

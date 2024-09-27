import openai
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv  # Importa a biblioteca dotenv

load_dotenv()  # Carrega as variáveis de ambiente

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

openai.api_key = os.getenv('OPENAI_API_KEY')  # Usa a chave da API do ambiente

# Armazenamento do histórico da conversa com limite
conversation_history = []

# Define um limite de tokens para o histórico
MAX_TOKENS_HISTORY = 3000

def trim_history(conversation_history):
    total_tokens = sum([len(h["content"].split()) for h in conversation_history])
    while total_tokens > MAX_TOKENS_HISTORY:
        conversation_history.pop(0)
        total_tokens = sum([len(h["content"].split()) for h in conversation_history])

def create_context_from_dataframe(df):
    context = ""
    summary = df.describe(include='all').to_string()
    context += f"Resumo dos dados:\n{summary}\n\n"
    
    for col in df.columns:
        col_data = ', '.join(map(str, df[col].dropna().tolist()[:10]))  # Apenas os 10 primeiros valores
        context += f"Coluna '{col}' tem os seguintes valores: {col_data}\n"
    
    context += "Use essas informações para responder às perguntas do usuário de forma detalhada e inteligente."
    return context

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('As senhas não coincidem.')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(name=name, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça o login.')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Erro ao cadastrar. Talvez o e-mail já esteja em uso.')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('E-mail ou senha incorretos.')
            return redirect(url_for('login'))

        session['user_id'] = user.id
        session['user_name'] = user.name
        flash('Login realizado com sucesso!')
        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('Você saiu da sua conta.')
    return redirect(url_for('home'))

@app.route('/chat')
def chat():
    # Verifica se o usuário está logado
    if 'user_id' not in session:
        flash('Por favor, faça login para acessar o chat.')
        return redirect(url_for('login'))
    
    return render_template('index.html')  # Carrega a página do chat se o usuário estiver logado

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/send_message_with_file', methods=['POST'])
def send_message_with_file():
    global conversation_history
    
    message = request.form.get('message')
    file = request.files.get('file')
    
    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
            context = create_context_from_dataframe(df)

            conversation_history.append({"role": "user", "content": f"Contexto da planilha:\n{context}"})
            conversation_history.append({"role": "user", "content": message})
            
            trim_history(conversation_history)
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=conversation_history
            )
            bot_response = response['choices'][0]['message']['content'].strip()

            conversation_history.append({"role": "assistant", "content": bot_response})

            return bot_response
        except Exception as e:
            return f"Ocorreu um erro ao processar a planilha: {str(e)}"
    else:
        conversation_history.append({"role": "user", "content": message})
        
        trim_history(conversation_history)
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=conversation_history
        )
        bot_response = response['choices'][0]['message']['content'].strip()

        conversation_history.append({"role": "assistant", "content": bot_response})

        return bot_response

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

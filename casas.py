import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, static_folder="static", template_folder="static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scores.db'
db = SQLAlchemy(app)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professor = db.Column(db.String(100), nullable=False)
    aluno = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    motivo = db.Column(db.String(200), nullable=False)
    turma = db.Column(db.String(50), nullable=False)
    equipe = db.Column(db.String(50), nullable=False)
    pontos = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    scores = Score.query.all()
    return render_template('index.html', scores=scores)

@app.route('/add', methods=['POST'])
def add_score():
    professor = request.form['professor']
    aluno = request.form['aluno']
    data = request.form['data']
    motivo = request.form['motivo']
    turma = request.form['turma']
    equipe = request.form['equipe']
    pontos = int(request.form['pontos'])
    
    new_score = Score(professor=professor, aluno=aluno, data=data, motivo=motivo, turma=turma, equipe=equipe, pontos=pontos)
    db.session.add(new_score)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/placar')
def placar():
    placar = db.session.query(Score.equipe, db.func.sum(Score.pontos)).group_by(Score.equipe).all()
    return render_template('placar.html', placar=placar)

@app.route('/api/placar')
def api_placar():
    placar = db.session.query(Score.equipe, db.func.sum(Score.pontos)).group_by(Score.equipe).all()
    return jsonify(placar)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

    # blablabla teste
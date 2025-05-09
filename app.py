
#* FLASK = FRAMEWORK WEB
#* RENDER TEMPLATE = CARREGA OS O HTML
#* REQUEST = ACESSA DADOS ENVIADO PELO FORM
#* REDIRECT E URL_FOR REDIRECIONA PRA OUTRA ROTA
#* IMPORTAÇÃO E CONFIGURAÇÃO SQLALCHEMY = BIBLIOTECA PRA USAR BANCO DE DADOS DE FORMA SIMPLES

#! IMPORTAÇÃO E CONFIGURAÇÃO
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  #!CRIA O APP 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuario.db' #!CONFIGURA O BANCO DE DADOS
db = SQLAlchemy(app) #!CRIA O OBJETO DO BANCO DE DADOS PARA MANIPULAR O BANCO


#!MODELO (TABELA DO BANCO)
#!CRIA A CLASSE DO BANCO DE DADOS || DEFINE O ID/NOME/EMAIL EM 3 COLUNAS NA TABELA || db.model indica que a classe representea uma tabela
class usuario(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  nome = db.Column(db.String(100))
  email = db.Column(db.String(100))


#!ROTA PRINCIPAL | LISTA DE USUARIO 
#! / ACESSA E BUSCA TODO OS USUARIOS NO BANCO

@app.route('/') 
def index():
  usuario = usuario.query.all()
  return render_template('index.html', usuario=usuario) #!ENVIA OS DADOS PARA O HTML

@app.route('/novo', methods=['GET', 'POST'])  #!SE FOR "POST" PEGA OS DADOS DO FORMULARIO CRIA E SALVA NO BANCO DE DADOS || SE FOR "GET" APENAS MOSTRA O FORMULARIO VAZIO
def novo (): #!CRIANDO UM USUARIO NOVO
  if request.method == 'POST':
    nome = request.form['nome']
    email = request.form['email']
    novo_usuario = usuario(nome = nome, email=email)
    db.session.add(novo_usuario)
    db.session.commit()
    return redirect(url_for('index'))
  return render_template('form.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST']) 
def editar(id):#!BUSCA O USUARIO PELO ID || SE FOR 'POST' ATUALIZA OS DADOS NO BANCO || SE FOR 'GET' MOSTRA OS DADOS PREENCHIDOS COM OS DADOS ATUAIS
  usuario=usuario.query.get_or_404(id)
  if request.method == 'POST':
    usuario.nome = request.form['nome']
    usuario.email = request.form['email']
    db.session.commit()
    return redirect(url_for('index'))
  return render_template('form.html' , usuario=usuario)

@app.route('/deletar/<int:id>')#!BUSCA O USUARIO PELO ID 
def deletar (id): #!BUSCA PELO ID E REMOVE O BANCO DO DADO
  usuario=usuario.query.get_or_404(id)
  db.session.delete(usuario)
  db.session.commit()
  return redirect(url_for('index'))
  
  if __name__ == '__main__':
    with app.app_context():
      db.create_all()
    app.run(debug=True)
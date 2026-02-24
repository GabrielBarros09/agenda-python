from flask import Flask, render_template, request, redirect, url_for
from models.tarefa import Tarefa
from models.database import Database

app = Flask(__name__) # aplicação flask

@app.route('/') # renderiza pagina inicial 
def home():
    return render_template('home.html', titulo='Home')

@app.route('/agenda', methods=['GET', 'POST']) # get: pedindo dados (mostra lista tarefas)
def agenda():                                  # post: enviando dados (cria nova tarefa)
    if request.method == 'POST':
        titulo_tarefa = request.form.get('titulo-tarefa')
        data_conclusao = request.form.get('data-conclusao')
        if titulo_tarefa and data_conclusao:
            tarefa = Tarefa(titulo_tarefa=titulo_tarefa, data_conclusao=data_conclusao)
            tarefa.salvar_tarefa()

    tarefas = Tarefa.obter_tarefas() # busca tarefas e envia para agenda.html
    return render_template('agenda.html', titulo='Agenda', tarefas=tarefas)

@app.route('/delete/<int:idTarefa>')
def delete(idTarefa):
    tarefa = Tarefa.id(idTarefa)
    tarefa.excluir_tarefa()
    return redirect(url_for('agenda'))

@app.route('/toggle/<int:idTarefa>') # alterna status: concluida ou aberta
def toggle(idTarefa):
    tarefa = Tarefa.id(idTarefa)
    tarefa.toggle_concluir()
    return redirect(url_for('agenda'))

@app.route('/update/<int:idTarefa>', methods=['GET', 'POST']) # get: mostra formulario preenchido / post: atualiza tarefa no banco
def update(idTarefa):
    if request.method == 'POST':
        titulo = request.form.get('titulo-tarefa')
        data = request.form.get('data-conclusao')
        if titulo and data:
            tarefa = Tarefa(titulo_tarefa=titulo, data_conclusao=data, id_tarefa=idTarefa)
            tarefa.atualizar_tarefa()
        return redirect(url_for('agenda'))

    tarefas = Tarefa.obter_tarefas()
    tarefa_selecionada = Tarefa.id(idTarefa)
    return render_template('agenda.html', 
                           titulo=f'Editando a tarefa ID: {idTarefa}', 
                           tarefas=tarefas, 
                           tarefa_selecionada=tarefa_selecionada)

def init_db(): # cria tabela, se não existir 
    from models.database import Database
    with Database() as db:
        db.executar("""
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo_tarefa TEXT NOT NULL,
                data_conclusao TEXT NOT NULL,
                concluida INTEGER DEFAULT 0,
                data_conclusao_real TEXT
            )
        """)
        print("Banco e tabela 'tarefas' verificados/criados com sucesso!")

init_db()

if __name__ == '__main__':
    print("Servidor Flask iniciado! Acesse http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

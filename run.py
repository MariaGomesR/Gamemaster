import uuid
import os
from flask import Flask, render_template, request, redirect 

app = Flask(__name__)

UPLOAD = 'static/assets'
app.config['UPLOAD'] = UPLOAD


@app.route('/')
def index():
    return render_template ("index.html")


#@app.route('/cadastro_plataformas')

@app.route('/cadastro_plataformas', methods=['GET', 'POST'])
def cadastro_plataformas():
    if request.method == 'POST':
        nome = request.form['nome']
        fabricante = request.form['fabricante']

        imagem = request.files['imagem']

        if imagem:
            extensao = imagem.filename.split('.')[-1]
            nome_imagem = f"{nome.strip().lower().replace(" ", "_")}.{extensao}"
            caminho_imagem = os.path.join(app.config['UPLOAD'], nome_imagem)  # Cria o caminho completo para salvar a imagem.
            imagem.save(caminho_imagem)  # Salva a imagem no diretório especificado.

        cod_plataforma = str(uuid.uuid4())

        caminho_arquivo = 'models/plataforma.txt'


        with open (caminho_arquivo, 'a') as arquivo:
            arquivo.write(f"{cod_plataforma};{nome}; {fabricante}; {caminho_imagem}\n")

        return redirect("/cadastro_plataformas")
    

    return render_template ("cadastro_plataformas.html")

# Consulta de dados da página: consulta_plataformas.html
@app.route('/consulta_plataformas')
def consulta_plataformas():
    plataformas = []
    linha_controle = 0 #controle numerico
    caminho_plataformas = 'models/plataforma.txt'

    with open (caminho_plataformas, 'r') as arquivo:
        for linha in arquivo:
            dados = linha
            #comando strip() elimina os espaços em branco
            #comando split() divide infomação baseado nos caracteres 
            dados = linha.strip().split(';')
            plataformas.append({  #alimentar a lista com um dicionário
                'linha':linha_controle,
                'cod_plataforma':dados[0],
                'nome':dados[1],
                'fabricante': dados [2],
                'imagem': dados [3]
            })

            linha_controle += 1 #incremento da variavel linha 

        return render_template ('consulta_plataformas.html', dados_lista=plataformas)


#Exclusão de dados do arquivo plataforma.txt
@app.route('/excluir_plataforma', methods=['GET', 'POST'])
def excluir_plataforma():
    #linha_para_excluir = request.args.get('linha') o nome da variável está apos o ponto de interrogação
    linha_para_excluir = int( request.args.get('linha'))
    caminho_plataformas = 'models/plataforma.txt'

    with open (caminho_plataformas, 'r') as arquivo:
        linhas = arquivo.readlines() #criado a variavel linhas que recebe todo o contexto
    linha_excluida = linhas[linha_para_excluir]

    del linhas[linha_para_excluir]

    with open (caminho_plataformas, 'w') as arquivo:
        arquivo.writelines (linhas)

    return redirect ('/consulta_plataformas')



@app.route('/cadastro_jogo', methods=['GET', 'POST'])
def cadastro_jogo():
    if request.method == 'POST':
        nomej = request.form['nomej']
        genero = request.form['genero']
        data = request.form['data']

        cod_jogo = str(uuid.uuid4())

        caminho_arquivo = 'models/jogos.txt'


        with open (caminho_arquivo, 'a') as arquivo:
            arquivo.write(f"{cod_jogo}; {nomej}; {genero}; {data}; \n")

        return redirect("/cadastro_jogo")
    

    return render_template ("cadastro_jogo.html")

app.run(host='0.0.0.0', port=5000, debug=True)

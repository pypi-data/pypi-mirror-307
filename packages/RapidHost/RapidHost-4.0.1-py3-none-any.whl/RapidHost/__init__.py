from flask import Flask, render_template, request, jsonify, redirect
import time  # Para usar o sleep

app = Flask(__name__)
host_ip = '127.0.0.1'  # IP padrão
host_port = 5000  # Porta padrão
template_path = 'templates'  # Caminho padrão dos templates
routes_data = {}  # Armazena os dados das rotas

def hostSite(*pages, information):
    app.template_folder = template_path  # Define o caminho dos templates
    for page in pages:
        route = '/' + page.split('.')[0] if page != 'index.html' else '/'

        # Definindo uma função única para cada rota
        def render_specific_page(page=page):
            return render_template(page, info=information)

        # Adicionando a rota com um nome de endpoint único
        app.add_url_rule(route, endpoint=route, view_func=render_specific_page)

    app.run(host=host_ip, port=host_port, debug=False)

def hostIP(ip):
    global host_ip
    host_ip = ip

def hostPort(port):
    global host_port
    host_port = port

def setTemplatePath(path):
    global template_path
    template_path = path

# Função para criar rota com informações associadas
def create_route(route_name, returnMessage):
    @app.route(f'/{route_name}', methods=['GET', 'POST'])
    def route_function():
        if request.method == 'POST':
            # Recebe dados do HTML e armazena na rota
            data = request.form.to_dict()
            routes_data[route_name] = data
            
            # Pausa por 0,5 segundos antes de retornar a resposta
            time.sleep(0.5)
            
            # Verifica se returnMessage é um link
            if returnMessage.startswith("http://") or returnMessage.startswith("https://"):
                return redirect(returnMessage, code=302)
            
            return returnMessage, 200

        # Retorna os dados armazenados na rota (para GET)
        return jsonify(routes_data.get(route_name, {}))

# Função para obter informações de uma rota no código Python
def GetfromRoute(route_name, info=""):
    data = routes_data.get(route_name, {})
    
    if info == "":
        return data  # Retorna todas as informações da rota
    return data.get(info, None)  # Retorna apenas a informação solicitada

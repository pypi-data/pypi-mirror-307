from flask import Flask, render_template

app = Flask(__name__)
host_ip = '127.0.0.1'  # IP padrão
host_port = 5000  # Porta padrão
template_path = 'templates'  # Caminho padrão dos templates

def hostSite(*pages):
    app.template_folder = template_path  # Define o caminho dos templates
    for page in pages:
        route = '/' + page.split('.')[0] if page != 'index.html' else '/'

        # Definindo uma função única para cada rota
        def render_specific_page(page=page):
            return render_template(page)

        # Adicionando a rota com um nome de endpoint único
        app.add_url_rule(route, endpoint=route, view_func=render_specific_page)

    app.run(host=host_ip, port=host_port, debug=True)

def hostIP(ip):
    global host_ip
    host_ip = ip

def hostPort(port):
    global host_port
    host_port = port

def setTemplatePath(path):
    global template_path
    template_path = path

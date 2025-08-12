# scanner-de-servicos-RTSP-HTTP-E-HTTPS-e-brute-force-de-credenciais-padrao.
Testa a acessibilidade dos serviços RTSP, HTTP e HTTPS em um IP informado pelo usuário e realiza tentativas de login usando uma lista de combinações de usuários e senhas básicas/padrão para cada serviço.
# Scanner de Serviços RTSP, HTTP e HTTPS com Brute Force de Credenciais

Este projeto realiza testes automáticos em serviços **RTSP**, **HTTP** e **HTTPS** para identificar vulnerabilidades de login, utilizando uma lista de credenciais padrão.  
Também permite o envio automático de um relatório por e-mail com as credenciais encontradas.

⚠ **Aviso**: Use este script apenas em redes e dispositivos que você tenha permissão para testar. O uso indevido pode ser ilegal.

---

## Funcionalidades

- **Varredura de portas** para serviços RTSP, HTTP e HTTPS.
- **Teste de credenciais padrão** (brute force leve).
- **Envio de relatório por e-mail** com as vulnerabilidades encontradas.
- **Registro em arquivo (`vulnerabilidades.txt`)** para consulta posterior.

---

## Pré-requisitos

- **Python 3.7 ou superior**
- Ter o **FFmpeg** instalado no sistema (necessário para teste RTSP).
- Conta de e-mail para envio do relatório (o script está configurado para Gmail).

---

## Instalação das dependências

Instale as bibliotecas necessárias com:

```bash
pip install requests

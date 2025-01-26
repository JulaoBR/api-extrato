class Middleware:
    def __init__(self, app, ips_permitidos):
        self.app = app
        self.ips_permitidos = ips_permitidos

    def __call__(self, environ, start_response):
        try:
            # Exemplo: validação simples antes de processar a requisição
            path = environ['PATH_INFO']
            if "/processar-extrato-cartao" in path:  # Exemplo de rota protegida
                # Tenta capturar o IP do cabeçalho X-Forwarded-For
                ip_cliente = environ.get('HTTP_X_FORWARDED_FOR')
                if ip_cliente:
                    # O X-Forwarded-For pode conter uma lista de IPs; pega o primeiro
                    ip_cliente = ip_cliente.split(',')[0].strip()
                else:
                    # Usa o IP direto se não estiver atrás de um proxy
                    ip_cliente = environ.get('REMOTE_ADDR', '0.0.0.0')

                if ip_cliente not in self.ips_permitidos:
                    print(f"Acesso negado para o IP: {ip_cliente}")
                    start_response('403 Forbidden', [('Content-Type', 'text/plain')])
                    return [b"Acesso negado"]

                # Caso o IP seja permitido, passa a requisição para o Flask
                return self.app(environ, start_response)

        except Exception as e:
            print(f"Erro no middleware: {e}")
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [b"Internal Server Error"]
        
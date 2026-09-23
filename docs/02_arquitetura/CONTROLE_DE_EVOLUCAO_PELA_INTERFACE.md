# Controle de Evolução pela Interface

A interface V1 agora possui um plano de controle explícito para a evolução do ABS.

Endpoints:
- GET /update/status
- POST /update/apply
- POST /update/rollback

Aplicar e rollback exigem o campo approved=true. Sem autorização explícita, o ABS recusa a operação.

O update manager continua responsável por:
- verificar mudanças;
- aplicar o commit remoto;
- reiniciar o serviço;
- aguardar health check;
- registrar o estado;
- realizar rollback quando a atualização falhar.

Isso conecta a interface ao mecanismo de continuidade e atualização sem transformar atualização em execução autônoma irrestrita.

Fluxo:
Imperador → Interface → autorização → Update Manager → serviço → health check → continuidade.

O mesmo mecanismo pode ser usado como fundação para futuras missões de construção do próprio ABS, desde que cada etapa preserve autorização, teste, evidência e rollback.
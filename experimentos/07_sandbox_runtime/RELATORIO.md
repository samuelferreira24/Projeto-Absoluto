# Experimento 07 — Resultado esperado

O experimento valida a fronteira:

MOLDE ≠ CAPACIDADE ≠ RECURSO ≠ EXECUTOR

A camada de molde decide o modo. O CapabilityRegistry fornece a capacidade correspondente. O ResourceRouter escolhe o caminho de recurso. O executor sandbox produz o resultado.

Ataques:
- todos os seis modos;
- ausência total de recurso;
- recurso explicitamente diferente no contexto;
- recursos com capacidades assimétricas.

A ausência de recurso deve produzir RESOURCE_UNAVAILABLE, não uma mudança silenciosa de molde.

Se este contrato passar, a integração futura pode ser feita como camada acima do runtime existente.

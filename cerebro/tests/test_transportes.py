from cerebro.transportes import Transporte, selecionar_transporte


def test_seleciona_transporte_sem_exigir_internet():
    opcoes = [
        Transporte("internet", "internet", "longo", custo=10, energia=3, internet_necessaria=True),
        Transporte("wifi", "wifi_direct", "curto", custo=1, energia=1, internet_necessaria=False),
    ]
    escolhido = selecionar_transporte(opcoes)
    assert escolhido is not None
    assert escolhido.id == "wifi"


def test_pode_exigir_internet():
    opcoes = [
        Transporte("wifi", "wifi_direct", "curto", internet_necessaria=False),
        Transporte("net", "internet", "longo", internet_necessaria=True),
    ]
    escolhido = selecionar_transporte(opcoes, exigir_internet=True)
    assert escolhido is not None
    assert escolhido.id == "net"


def test_retorna_none_sem_meio_viavel():
    opcoes = [Transporte("nfc", "nfc", "proximidade", conectado=False)]
    assert selecionar_transporte(opcoes) is None

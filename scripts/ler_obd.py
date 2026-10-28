"""Leitura simples de OBD2 via ELM327, para aprender o que o OBDium faz por baixo.

Instalar dependência:
    pip install obd

Uso:
    python ler_obd.py                  # detecta a porta automaticamente
    python ler_obd.py COM3             # Windows
    python ler_obd.py /dev/ttyUSB0     # Linux
    python ler_obd.py /dev/ttyUSB0 --ao-vivo
"""

import sys
import time

import obd

# PIDs do modo 01 que valem a pena olhar num TSI
COMANDOS_AO_VIVO = [
    obd.commands.RPM,
    obd.commands.SPEED,
    obd.commands.COOLANT_TEMP,
    obd.commands.INTAKE_TEMP,
    obd.commands.INTAKE_PRESSURE,  # MAP: acima de ~100 kPa = turbo soprando
    obd.commands.THROTTLE_POS,
    obd.commands.ENGINE_LOAD,
    obd.commands.CONTROL_MODULE_VOLTAGE,
]


def conectar(porta):
    # Jetta 2018/19: CAN 11-bit 500 kbps = protocolo "6" do ELM327
    conexao = obd.OBD(porta, protocol="6", fast=False)
    if not conexao.is_connected():
        print(f"Não conectou. Status: {conexao.status()}")
        print("Confira: adaptador plugado, ignição ligada, porta correta.")
        sys.exit(1)
    print(f"Conectado em {conexao.port_name()} | protocolo: {conexao.protocol_name()}")
    return conexao


def mostrar_resumo(conexao):
    vin = conexao.query(obd.commands.VIN)
    if not vin.is_null():
        print(f"VIN: {vin.value}")

    codigos = conexao.query(obd.commands.GET_DTC)
    if codigos.is_null() or not codigos.value:
        print("Nenhum código de falha armazenado.")
    else:
        print("Códigos de falha:")
        for codigo, descricao in codigos.value:
            print(f"  {codigo}: {descricao or 'sem descrição'}")

    print()
    for comando in COMANDOS_AO_VIVO:
        resposta = conexao.query(comando)
        valor = "não suportado" if resposta.is_null() else resposta.value
        print(f"{comando.desc:<35} {valor}")


def ao_vivo(conexao):
    print("Lendo ao vivo (Ctrl+C para sair)...")
    try:
        while True:
            linha = []
            for comando in (obd.commands.RPM, obd.commands.SPEED,
                            obd.commands.COOLANT_TEMP, obd.commands.INTAKE_PRESSURE):
                resposta = conexao.query(comando)
                linha.append("--" if resposta.is_null() else f"{resposta.value.magnitude:.0f}")
            print("RPM {:>5} | km/h {:>3} | motor °C {:>3} | MAP kPa {:>3}".format(*linha))
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass


def main():
    argumentos = [a for a in sys.argv[1:] if not a.startswith("--")]
    porta = argumentos[0] if argumentos else None
    conexao = conectar(porta)
    try:
        if "--ao-vivo" in sys.argv:
            ao_vivo(conexao)
        else:
            mostrar_resumo(conexao)
    finally:
        conexao.close()


if __name__ == "__main__":
    main()

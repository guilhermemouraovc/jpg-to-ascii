# 3. Usando o OBDium

[OBDium](https://github.com/provrb/obdium) é um app de diagnóstico open source
(GPL-3.0), feito em Rust com interface Tauri. Roda em Windows 10/11, macOS e Linux.

O que ele faz:

- Lê códigos de falha (P, B, C, U) com descrição
- Mostra dados ao vivo dos PIDs padrão OBD2 (PIDs específicos de montadora ainda estão nos planos)
- Decodifica o VIN offline (base vPIC da NHTSA)
- Testes de prontidão (I/M readiness) do motor
- Modo demo: grava as respostas do carro num `requests.json` e reproduz depois sem o carro

## Instalar (jeito fácil)

Baixe o instalador do seu sistema na página de
[Releases](https://github.com/provrb/obdium/releases) e instale normalmente.

## Compilar do código-fonte (para estudar o código)

```bash
# 1. Instalar Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 2. Instalar o Tauri CLI v2
cargo install tauri-cli --version "^2.0.0"

# 3. Baixar o projeto
git clone https://github.com/provrb/obdium
cd obdium

# 4a. Rodar em modo desenvolvedor
cargo tauri dev --no-watch

# 4b. Ou gerar o executável final
cargo tauri build
```

No Linux, o Tauri precisa de algumas bibliotecas do sistema (webkit2gtk etc.);
veja os [pré-requisitos do Tauri](https://tauri.app/start/prerequisites/).

## Conectar no Jetta

1. Plugue o adaptador e ligue a ignição/motor (ver [guia de conexão](02-adaptador-e-conexao.md)).
2. Abra o OBDium e vá no painel **Connection**.
3. Escolha a porta serial do adaptador (clique em atualizar se a lista estiver vazia).
4. Protocolo e baud rate: deixe no padrão. Se falhar, escolha **ISO 15765-4 CAN (11 bit, 500 kbaud)**.
5. Clique em **Connect** e espere a notificação de sucesso.

## Roteiro de aprendizado no carro

1. **VIN**: confira se o VIN decodificado bate com o documento do carro.
2. **Códigos de falha**: leia mesmo sem luz acesa; anote se tiver algum.
3. **Prontidão (readiness)**: veja quais monitores estão "completos".
4. **Dados ao vivo com motor frio → quente**: acompanhe a temperatura do
   líquido subir até ~90 °C e a marcha lenta cair de ~1000 para ~750 rpm.
5. **Turbo**: com alguém dirigindo, observe a pressão do coletor (MAP) passar de
   ~100 kPa (pressão atmosférica) em acelerações — isso é o turbo do TSI soprando.
6. **Modo demo**: grave uma sessão e depois estude em casa sem o carro.

## Problemas comuns

| Sintoma | O que tentar |
|---------|--------------|
| Nenhuma porta na lista | Driver do adaptador (FTDI/CH340); no Linux, grupo `dialout` |
| Conecta no adaptador mas "no data" / "unable to connect" | Ignição ligada? Force protocolo CAN 11-bit 500k |
| Respostas estranhas / travando | Adaptador clone ruim; teste outro baud (38400, 115200) ou outro adaptador |
| Alguns PIDs não aparecem | Normal: cada ECU suporta só parte dos PIDs (veja resposta do `0100`) |

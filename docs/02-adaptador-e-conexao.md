# 2. Adaptador e conexão no Jetta TSI 2018/19

## Qual é o meu Jetta

- **2018**: geração MK6 (reestilizado), 1.4 TSI (EA211) ou 2.0 TSI no GLI/Highline.
- **2019**: geração MK7 (plataforma MQB), 250 TSI 1.4 ou GLI 350 TSI 2.0.

Para OBD2 genérico os dois funcionam igual: rede **CAN 11-bit, 500 kbps
(ISO 15765-4)** — no ELM327 é o **protocolo 6** (`ATSP6`).
Nesses anos o VW ainda não tem o "gateway de segurança" que bloqueia acesso,
então leitura genérica funciona sem problema.

## Onde fica a tomada

Embaixo do painel, **lado do motorista**, à esquerda da coluna de direção, acima
dos pedais. Às vezes fica atrás de uma tampinha plástica. Olhe deitado no banco
com uma lanterna — o conector é trapezoidal e fica virado para baixo.

## Qual adaptador comprar

O OBDium conecta por **porta serial** (você escolhe a porta na lista). Isso define o tipo:

| Tipo | Funciona no OBDium? | Observação |
|------|---------------------|------------|
| **ELM327 USB** | ✅ Melhor opção | Aparece como `COMx` (Windows) ou `/dev/ttyUSB0` (Linux) |
| **OBDLink SX / EX (USB)** | ✅ Excelente | Mais caro, chip original, bem mais rápido e confiável |
| ELM327 Bluetooth clássico | ⚠️ Geralmente sim | Depois de parear, vira uma porta COM (Windows) / `/dev/rfcomm0` (Linux) |
| ELM327 Bluetooth LE (BLE) | ❌ Em geral não | BLE não cria porta serial; serve para apps de celular |
| ELM327 Wi-Fi | ❌ Em geral não | Usa TCP (192.168.0.10:35000), não porta serial |

**Cuidado com clones baratos**: muitos ELM327 "v2.1" de site chinês são
cópias ruins que não respondem a todos os comandos. Prefira os anunciados com
chip **PIC18F25K80** ("v1.5") ou um OBDLink. Para o celular, o app
**Car Scanner** com um adaptador BLE (ex.: Vgate iCar Pro) é uma boa dupla.

## Drivers

- **Windows**: adaptadores USB costumam usar chip FTDI ou CH340. Se não aparecer
  porta COM no Gerenciador de Dispositivos, instale o driver do chip.
- **Linux**: aparece como `/dev/ttyUSB0`. Dê permissão ao seu usuário:
  `sudo usermod -aG dialout $USER` (depois saia e entre de novo).
- **macOS**: aparece como `/dev/tty.usbserial-*` (CH340 pode precisar de driver).

## Passo a passo da primeira conexão

1. Carro desligado: plugue o adaptador na tomada OBD2 (a luz dele deve acender).
2. Ligue a ignição (posição 2, painel aceso) ou, melhor, ligue o motor para ver dados ao vivo.
   Se for ficar muito tempo só com ignição, cuidado com a bateria.
3. Conecte o adaptador ao notebook (cabo USB ou pareamento Bluetooth, PIN costuma ser `1234` ou `0000`).
4. Abra o software e escolha a porta.

## Teste manual (opcional, para aprender)

Num terminal serial (PuTTY no Windows, `screen /dev/ttyUSB0 38400` no Linux),
com baud 38400 (ou 9600/115200 dependendo do adaptador), digite:

```
ATZ        -> reinicia o ELM327 (responde "ELM327 v1.5")
ATE0       -> desliga o eco
ATSP6      -> força CAN 11-bit 500k (o protocolo do Jetta)
0100       -> pergunta quais PIDs o carro suporta
010C       -> RPM
0105       -> temperatura do motor
03         -> códigos de falha
ATRV       -> tensão da bateria lida pelo adaptador
```

## Segurança

- Não mexa no notebook dirigindo. Para testar andando, leve alguém junto.
- Não deixe o adaptador plugado por dias: alguns drenam a bateria.
- Modo `04` (apagar códigos) também zera os monitores de prontidão; o carro
  pode reprovar em inspeção até rodar alguns ciclos.

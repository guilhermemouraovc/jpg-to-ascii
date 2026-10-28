# 1. O que é OBD2

OBD2 (On-Board Diagnostics II) é um padrão que todo carro a combustão vendido
nos EUA desde 1996 (e no Brasil, como OBDBr-2, desde ~2010) precisa ter. Ele dá
acesso padronizado aos dados da **central do motor (ECU)**: sensores, falhas e
testes de emissões.

## As peças

```
[ECU do motor] <--rede CAN--> [tomada OBD2] <--> [adaptador ELM327] <--USB/BT--> [notebook + OBDium]
```

- **Tomada OBD2 (DLC)**: conector trapezoidal de 16 pinos. Pinos importantes:
  4/5 = terra, 6/14 = CAN High/Low, 16 = +12 V da bateria.
- **Adaptador ELM327**: traduz a rede CAN do carro para uma porta serial no
  computador. Você manda texto (comandos AT e pedidos OBD) e recebe texto em hexadecimal.
- **Software** (OBDium, Car Scanner, Torque…): manda os pedidos e interpreta as respostas.

## Modos (serviços)

Cada pedido OBD2 é `MODO + PID`, em hexadecimal.

| Modo | Para que serve |
|------|----------------|
| `01` | Dados ao vivo (RPM, velocidade, temperatura…) |
| `02` | "Freeze frame": foto dos sensores no momento em que uma falha ocorreu |
| `03` | Ler códigos de falha (DTCs) confirmados |
| `04` | **Apagar** códigos de falha e apagar a luz de injeção |
| `07` | Códigos pendentes (ainda não confirmados) |
| `09` | Informações do veículo (VIN, calibração) |

## PIDs: exemplos do modo 01

| Pedido | O que é | Como calcular a resposta (A, B = bytes) |
|--------|---------|------------------------------------------|
| `01 0C` | RPM | `(256·A + B) / 4` |
| `01 0D` | Velocidade | `A` km/h |
| `01 05` | Temperatura do líquido de arrefecimento | `A − 40` °C |
| `01 0F` | Temperatura do ar admitido | `A − 40` °C |
| `01 11` | Posição da borboleta | `A · 100 / 255` % |
| `01 0B` | Pressão no coletor (MAP) | `A` kPa (útil para ver o turbo do TSI) |
| `01 42` | Tensão do módulo | `(256·A + B) / 1000` V |

Exemplo real: você manda `010C` e o carro responde `41 0C 0B B8`.
`41` = resposta ao modo 01, `0C` = PID, `A=0x0B=11`, `B=0xB8=184` →
`(256·11 + 184)/4 = 750 rpm` (marcha lenta).

## Códigos de falha (DTCs)

Formato `P0301`:

- 1ª letra: **P** = motor/câmbio (Powertrain), **B** = carroceria, **C** = chassi, **U** = rede
- 1º dígito: `0` = genérico (igual em qualquer carro), `1` = específico da montadora
- Restante: subsistema e falha. Ex.: `P0301` = falha de ignição no cilindro 1.

> Dica: anote o código e o freeze frame **antes** de apagar. Apagar não conserta
> nada, e a luz volta se o problema persistir.

## O que o OBD2 genérico NÃO mostra

O OBD2 padrão conversa basicamente com a central do motor (e às vezes do câmbio).
Módulos de ABS, airbag, painel, ar-condicionado, ajustes de conforto etc. no VW
usam protocolos próprios (UDS/KWP da VAG). Para isso existem ferramentas
específicas: **VCDS** (Ross-Tech), **OBDeleven** ou **Car Scanner** com perfil VAG.

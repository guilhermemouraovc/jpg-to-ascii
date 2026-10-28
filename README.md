# OBD2 no Jetta TSI 2018/19

Guia prático para aprender OBD2 do zero e ler dados do meu Jetta TSI com o
[OBDium](https://github.com/provrb/obdium) (open source, em Rust) e com um
script Python simples para entender o que acontece "por baixo".

- [`docs/01-o-que-e-obd2.md`](docs/01-o-que-e-obd2.md): conceitos (modos, PIDs, códigos de erro)
- [`docs/02-adaptador-e-conexao.md`](docs/02-adaptador-e-conexao.md): qual adaptador comprar e como conectar no Jetta
- [`docs/03-obdium.md`](docs/03-obdium.md): instalar e usar o OBDium
- [`scripts/ler_obd.py`](scripts/ler_obd.py): script Python para ler RPM, temperatura, códigos etc.

## Resumo rápido

1. Compre um adaptador **ELM327 USB** (ou um OBDLink SX/EX) — é o que funciona melhor no OBDium.
2. A tomada OBD2 do Jetta fica **embaixo do painel, do lado do motorista**, acima dos pedais.
3. Plugue o adaptador, ligue a ignição (ou o motor) e conecte no notebook.
4. Abra o OBDium, escolha a porta serial, deixe protocolo/baud no padrão e clique em **Connect**.
5. O Jetta usa **CAN 11-bit 500 kbps (ISO 15765-4, protocolo 6 do ELM327)** — se a detecção automática falhar, force esse protocolo.

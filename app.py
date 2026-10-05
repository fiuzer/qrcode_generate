"""
Gerador de Pix estático: cria o "copia e cola" e o QR Code a partir de
chave, nome, cidade e valor.

Como rodar:
    pip install -r requirements.txt
    python app.py
    abra http://127.0.0.1:5000 no navegador

O formato do código é o BR Code, do Manual de Padrões para Iniciação do Pix
(Banco Central). Cada campo é: ID (2 dígitos) + tamanho (2 dígitos) + valor.
"""
import re
import unicodedata
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from pathlib import Path

import segno
from flask import Flask, jsonify, request, send_from_directory

PASTA = Path(__file__).resolve().parent
app = Flask(__name__)


# ---------------------------------------------------------------------------
# Montagem do código Pix
# ---------------------------------------------------------------------------

def campo(id_campo: str, valor: str) -> str:
    """Monta um campo: ID + tamanho com 2 dígitos + valor."""
    if len(valor) > 99:
        raise ValueError(
            f"O campo {id_campo} ficou grande demais ({len(valor)} caracteres, máximo 99)."
        )
    return f"{id_campo}{len(valor):02d}{valor}"


def normalizar(texto: str, limite: int) -> str:
    """Tira acentos, deixa em maiúsculas e corta no limite do campo."""
    sem_acento = (
        unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    )
    limpo = re.sub(r"\s+", " ", sem_acento).strip().upper()
    return limpo[:limite].strip()


def formatar_valor(texto: str) -> str:
    """Converte '25,90', '1.234,56' ou '25.9' em '25.90' (ponto, 2 casas)."""
    texto = texto.strip().replace("R$", "").replace(" ", "")
    if "," in texto:  # formato brasileiro: ponto separa milhar, vírgula separa centavos
        texto = texto.replace(".", "").replace(",", ".")
    try:
        valor = Decimal(texto)
    except InvalidOperation:
        raise ValueError("Valor inválido. Use apenas números, por exemplo 25,90.")
    if not valor.is_finite() or valor <= 0:
        raise ValueError("O valor precisa ser um número maior que zero.")
    valor = valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if valor > Decimal("9999999.99"):
        raise ValueError("Valor alto demais para um Pix.")
    return f"{valor:.2f}"


def crc16(texto: str) -> str:
    """CRC16-CCITT-FALSE (polinômio 0x1021, início 0xFFFF), em hexadecimal maiúsculo."""
    crc = 0xFFFF
    for byte in texto.encode("ascii"):
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return f"{crc:04X}"


def gerar_payload(chave: str, nome: str, cidade: str, valor: str | None = None) -> str:
    """Devolve o texto do Pix copia e cola."""
    chave = chave.strip()
    if not chave:
        raise ValueError("Informe a chave Pix.")
    if re.fullmatch(r"[\d.\-/]+", chave):  # CPF/CNPJ com pontuação -> só números
        chave = re.sub(r"\D", "", chave)
    if not chave.isascii() or " " in chave:
        raise ValueError("A chave Pix não pode ter espaços nem acentos.")

    nome = normalizar(nome, 25)
    cidade = normalizar(cidade, 15)
    if not nome:
        raise ValueError("Informe o nome do recebedor.")
    if not cidade:
        raise ValueError("Informe a cidade.")

    # Campo 26: dados da conta, com subcampos (00 = identificador do Pix, 01 = chave)
    conta = campo("00", "br.gov.bcb.pix") + campo("01", chave)

    partes = [
        campo("00", "01"),    # versão do formato
        campo("01", "11"),    # 11 = QR estático (pode ser pago mais de uma vez)
        campo("26", conta),
        campo("52", "0000"),  # categoria do comerciante (não informada)
        campo("53", "986"),   # moeda: real
    ]
    if valor:
        partes.append(campo("54", formatar_valor(valor)))
    partes += [
        campo("58", "BR"),
        campo("59", nome),
        campo("60", cidade),
        campo("62", campo("05", "***")),  # identificador da transação (não informado)
    ]

    sem_crc = "".join(partes) + "6304"  # o CRC cobre o texto inteiro, incluindo "6304"
    return sem_crc + crc16(sem_crc)


def autoteste() -> None:
    """Confere os dois exemplos conhecidos (chave fictícia). Falha se algo estiver errado."""
    chave = "123e4567-e89b-12d3-a456-426614174000"
    esperados = {"25,90": "A7B3", "255,00": "B755"}
    for valor, crc in esperados.items():
        codigo = gerar_payload(chave, "Loja Exemplo", "Sao Paulo", valor)
        assert codigo.endswith("6304" + crc), f"Autoteste falhou para {valor}: {codigo}"


# ---------------------------------------------------------------------------
# Rotas web
# ---------------------------------------------------------------------------

@app.get("/")
def pagina():
    return send_from_directory(PASTA, "index.html")


@app.post("/api/gerar")
def api_gerar():
    dados = request.get_json(silent=True) or {}
    chave = str(dados.get("chave") or "")
    nome = str(dados.get("nome") or "")
    cidade = str(dados.get("cidade") or "")
    valor = str(dados.get("valor") or "").strip() or None

    try:
        codigo = gerar_payload(chave, nome, cidade, valor)
    except ValueError as erro:
        return jsonify(erro=str(erro)), 400

    qr = segno.make(codigo, error="m", micro=False)
    return jsonify(
        codigo=codigo,
        qr=qr.png_data_uri(scale=10, border=4),
        valor=formatar_valor(valor) if valor else None,
    )


if __name__ == "__main__":
    autoteste()
    print("Autoteste do Pix: OK")
    # 127.0.0.1 = só este computador acessa. Para abrir pelo celular na mesma rede,
    # troque por host="0.0.0.0" (só faça isso em rede de confiança).
    app.run(host="127.0.0.1", port=5000, debug=False)

import pytest
import bot
import io
from unittest.mock import *
from PIL import Image


@pytest.mark.parametrize(
    "code",[
        "https://example.com",  # URL simples
        "12345",                # Apenas números
        "Hello, World!",        # Texto com pontuação
        "",                     # String vazia
        "🧡💻🌟"                # Emojis
],)

def test_generate_qr_valid_bytes(code):
    qr_bytes = bot.makeQRimage(code)
    assert isinstance(qr_bytes, bytes), "A saída deve ser do tipo bytes"
    assert len(qr_bytes) > 0, "A saída em bytes não pode estar vazia"


@pytest.mark.parametrize(
    "code",
    [
        "https://example.com",  # URL
        "test_data",            # Texto simples
        "abcdef",               # Letras minúsculas
        "0123456789",           # Apenas números
        "SPECIAL*&^%$#"         # Caracteres especiais
    ],)
def test_generate_qr_valid_image(code):
    qr_bytes = bot.makeQRimage(code)
    with io.BytesIO(qr_bytes) as buffer:
        img = Image.open(buffer)
        img.verify()  # Verifica se é uma imagem válida
    assert img.format == "PNG", "A imagem gerada deve estar no formato PNG"


@pytest.mark.parametrize(
    "code",
    [
        "https://example.com",  # URL
        "test",                 # Texto curto
        "another_test_123",     # Texto misto
        "☀️🌈✨",                # Emojis
        "A" * 1000              # String muito longa
    ],)
def test_generate_qr_contains_correct_data(code):
    from pyzbar.pyzbar import decode

    qr_bytes = bot.makeQRimage(code)
    buffer = io.BytesIO(qr_bytes) 
    img = Image.open(buffer)
    decoded_data = decode(img)

    assert len(decoded_data) > 0, "O QR Code não foi decodificado corretamente"
    assert decoded_data[0].data.decode() == code, "Os dados no QR Code não correspondem ao código original"


@pytest.mark.parametrize(
    "invalid_code",
    [
        None,                   # Código inválido (None)
        12345,                  # Número (não string)
        {"key": "value"},       # Dicionário
        ["item1", "item2"],     # Lista
        b"bytes_data"           # Bytes
    ],)
def test_generate_qr_invalid_input(invalid_code):
    with pytest.raises((TypeError, ValueError)):
        bot.makeQRimage(invalid_code)


@pytest.mark.parametrize(
    "code",
    [
        "Test Short",           # Texto curto
        "A" * 100,              # Texto longo
        "https://example.com",  # URL
        "",                     # String vazia
        "Data with spaces"      # Texto com espaços
    ],)
def test_generate_qr_different_inputs(code):
    qr_bytes = bot.makeQRimage(code)
    with io.BytesIO(qr_bytes) as buffer:
        img = Image.open(buffer)
    assert img.size[0] > 0 and img.size[1] > 0, "As dimensões da imagem devem ser maiores que zero"

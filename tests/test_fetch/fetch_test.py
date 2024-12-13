import pytest
from unittest.mock import MagicMock, patch
from mercadopago.config import RequestOptions
from fetch import fetch
from classes import Usertest


@patch("mercadopago.SDK")
def test_fetch_payment_approved(mock_sdk):
    mock_payment = MagicMock()
    mock_payment.create.return_value = {
        "status": "201",
        "response": {
            "point_of_interaction": {
                "transaction_data": {
                    "qr_code": "mock_qr_code",
                    "ticket_url": "mock_ticket_url",
                }
            }
        },
    }
    mock_sdk.return_value.payment.return_value = mock_payment

    user = Usertest()

    result = fetch(mock_sdk.return_value, user, "pix")
    assert result == {
        "QRCode": "mock_qr_code",
        "link": "mock_ticket_url",
        "status": "aproved",
    }

    mock_payment.create.assert_called_once()
    args, kwargs = mock_payment.create.call_args
    payment_data = args[0]
    request_options = args[1]
    assert payment_data["transaction_amount"] == 1
    assert payment_data["payer"]["email"] == user.email
    assert request_options.custom_headers["x-idempotency-key"] == str(user.id)


@patch("mercadopago.SDK")
def test_fetch_payment_denied(mock_sdk):
    mock_payment = MagicMock()
    mock_payment.create.return_value = {
        "status": "400",
        "response": {"message": "Invalid request"},
    }
    mock_sdk.return_value.payment.return_value = mock_payment

    user = Usertest()

    result = fetch(mock_sdk.return_value, user, "pix")

    print("Mock SDK payment.create call:", mock_payment.create.call_args)
    print("Resultado da função fetch:", result)
    mock_payment.create.assert_called_once()
    assert result == {"status": "denied", "msg": "Invalid request"}


@patch("mercadopago.SDK")
def test_fetch_payment_with_invalid_paymentMode(mock_sdk):
    user = Usertest()
    result = fetch(mock_sdk, user, "pinto grosso 8====D")
    assert result == {"status": "denied", "msg": "An unexpected error occurred."}
    print(result)
    # with pytest.raises(ValueError):
    #     fetch(mock_sdk.return_value, user, "pinto grosso 8====D")


@patch("mercadopago.SDK")
def test_fetch_sdk_unexpected_error(mock_sdk):
    mock_payment = MagicMock()
    mock_payment.create.side_effect = Exception("Unexpected error")
    mock_sdk.return_value.payment.return_value = mock_payment

    user = Usertest()

    result = fetch(mock_sdk.return_value, user, "pix")

    assert result == {"status": "denied", "msg": "An unexpected error occurred."}
    mock_payment.create.assert_called_once()


@patch("mercadopago.SDK")
def test_fetch_connection_error(mock_sdk):
    mock_payment = MagicMock()
    mock_payment.create.side_effect = ConnectionError("Connection failed")
    mock_sdk.return_value.payment.return_value = mock_payment

    user = Usertest()

    result = fetch(mock_sdk.return_value, user, "pix")

    assert result == {
        "status": "denied",
        "msg": "Network error occurred, please try again.",
    }


@patch("mercadopago.SDK")
def test_fetch_key_error(mock_sdk):
    mock_payment = MagicMock()
    mock_payment.create.return_value = {
        "status": 201,  # Resposta válida
        "response": {},  # Dados incompletos
    }
    mock_sdk.return_value.payment.return_value = mock_payment

    user = Usertest()

    result = fetch(mock_sdk.return_value, user, "pix")

    assert result == {
        "status": "denied",
        "msg": "Invalid response structure: 'point_of_interaction'",
    }

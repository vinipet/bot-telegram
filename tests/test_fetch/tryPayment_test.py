from unittest.mock import patch
import pytest
import classes
import fetch
import bot
from unittest.mock import patch


@pytest.fixture
def mock_fetch():
    with patch("fetch.fetch") as mock:
        yield mock


def test_try_payment_valid_user(mock_fetch):
    mock_fetch.return_value = {
        "status": 1,
        "response": {"msg": "Pagamento realizado com sucesso!"},
    }
    user = classes.Usertest()
    userInfos = []
    result = fetch.tryPayment(user, userInfos)
    assert result == {
        "status": 1,
        "response": {"msg": "Pagamento realizado com sucesso!"},
    }
    mock_fetch.assert_called_once_with(user)


def test_try_payment_invalid_user(mock_fetch):
    user = None  
    userInfos = ["id", "name"]
    result = fetch.tryPayment(user, userInfos)
    assert result == {
        "status": 0,
        "response": {"msg": "o usuario não possui um cadastro completo, ou valido"},
    }
    mock_fetch.assert_not_called()


def test_try_payment_none_user(mock_fetch):
    mock_fetch.return_value = {
        "status": 1,
        "response": {
            "msg": "Pagamento realizado com sucesso!"
        }
    }

    user = None
    userInfos = []
    result = fetch.tryPayment(user, userInfos)
    assert result == {
        "status": 0,
        "response": {
            "msg": "o usuario não possui um cadastro completo, ou valido"
        }
    }
    mock_fetch.assert_not_called()

def test_try_payment_no_complete_user(mock_fetch):
    userInfos = ["id", "firstName"]
    user = classes.Usertest(3434, userInfos, firstName=None)  
    result = fetch.tryPayment(user, userInfos)
    assert result == {
        "status": 0,
        "response": {"msg": "o usuario não possui um cadastro completo, ou valido"},
    }
    mock_fetch.assert_not_called()

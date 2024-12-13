from unittest.mock import *

import pytest

import bot
import classes


def compare_objects(obj1, obj2):
    """
    Compara dois objetos para verificar se possuem os mesmos valores nos atributos especificados.

    Parâmetros:
        obj1: O primeiro objeto a ser comparado.
        obj2: O segundo objeto a ser comparado.

    Retorna:
        bool: True se os objetos têm os mesmos valores nos atributos especificados, False caso contrário.
    """
    obj1_attrs = vars(obj1)
    obj2_attrs = vars(obj2)
    return obj1_attrs == obj2_attrs


@pytest.fixture
def mockBank():
    with patch(
        "bot.bancoDdados", {"1": classes.Usertest(), "2": {"name": "Bob"}}
    ), patch(
        "bot.userData",
        {
            "3": {"name": "Charlie"},
            "4": classes.Usertest(),
            "5": classes.User(123, infos="1"),
            "6": classes.User(9090, ["quero boquete parafuso", "name", "email"]),
        },
    ):
        yield bot


def test_try_register_dict_user(mockBank):
    with pytest.raises(TypeError):
        bot.tryRegisterUser("3")


def test_try_register_object_user(mockBank):
    preObj = bot.userData["4"]
    bot.tryRegisterUser("4")
    assert compare_objects(bot.bancoDdados["4"], preObj) == True


def test_try_register_user_without_steps(mockBank):
    with pytest.raises(TypeError):
        bot.tryRegisterUser("5")


def test_try_register_user_with_somuch_steps(mockBank):
    bot.tryRegisterUser("6")
    assert "6" in bot.userData
    assert "6" not in bot.bancoDdados

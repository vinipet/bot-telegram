from unittest.mock import *

import pytest

import bot
import classes


@patch("bot.bot.get_my_commands")
def test_add_command(mock_get_my_commands):
    mock_get_my_commands.return_value = [
        bot.types.BotCommand("start", "Iniciar bot"),
        bot.types.BotCommand("help", "Mostrar ajuda"),
    ]

    expected_commands = [
        bot.types.BotCommand("start", "Iniciar bot"),
        bot.types.BotCommand("help", "Mostrar ajuda"),
        bot.types.BotCommand("settings", "Configurar bot"),
    ]

    bot.add_command(bot.bot, "settings", "Configurar bot")

    result_commands = bot.bot.get_my_commands()

    assert len(result_commands) == len(expected_commands)
    for i in range(len(expected_commands)):
        assert result_commands[i].command == expected_commands[i].command
        assert result_commands[i].description == expected_commands[i].description

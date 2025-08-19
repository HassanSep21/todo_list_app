import pytest
from unittest.mock import MagicMock
from project import register, login, todo


@pytest.fixture
def mock_window(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("PySimpleGUI.PySimpleGUI.Window", mock)
    return mock


def test_register():
    window_mock = {
        "-USER-": {"update": lambda x: None},
        "-PASS-": {"update": lambda x: None},
    }

    result = register("valid_user", "valid_password", window_mock)
    assert result is True

    result = register("", "", window_mock)
    assert result is False


def test_login():
    window_mock = {
        "-USER-": {"update": lambda x: None},
        "-PASS-": {"update": lambda x: None},
        "_closed": False,
    }

    result = login("valid_user", "valid_password", window_mock, close_window=False)
    assert result is True

    assert not window_mock["_closed"]

    result = login("invalid_user", "invalid_password", window_mock, close_window=False)
    assert result is False

    assert not window_mock["_closed"]


def test_todo():
    mock_window_instance = mock_window.return_value
    mock_window_instance.read.side_effect = [
        ("Add", {"-DATE-": "2023-11-30", "-TASK-": "Test Task"}),
        ("Exit", None),
    ]

    todo()

    mock_window.assert_called_once()
    mock_window_instance["-TABLE-"].update.assert_called_once_with(
        [["2023-11-30", "Test Task"]]
    )

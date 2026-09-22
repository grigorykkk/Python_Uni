import main as application


def test_main_menu_covers_all_actions(monkeypatch, sample_events, capsys):
    data = {
        "events": sample_events[:1],
        "organizations": [{"id": 1, "name": "Фонд", "contact": "a@b.ru"}],
        "users": [],
        "registrations": [],
    }
    user = {"id": 1, "name": "Анна", "age": 20, "email": "a@b.ru"}
    answers = iter([
        "1", "2", "животные", "", "Москва", "3", "название",
        "4", "1", "5", "1", "6", "7", "0",
    ])
    monkeypatch.setattr(application, "load_data", lambda: data)
    monkeypatch.setattr(application, "get_current_user", lambda _: user)
    monkeypatch.setattr(application, "save_data", lambda _: None)
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    application.main()

    output = capsys.readouterr().out
    assert "Помощь животным" in output
    assert "Регистрация выполнена" in output
    assert "Регистрация отменена" in output
    assert "=== Статистика ===" in output
    assert "До свидания!" in output

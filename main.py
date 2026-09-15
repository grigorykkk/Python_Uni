from datetime import date


def can_participate(user_age, event_min_age):
    """Проверяет, подходит ли пользователь по возрасту."""
    return user_age >= event_min_age


def register_user(user_name, event_name):
    """Выполняет регистрацию пользователя на мероприятие."""
    answer = input("\nХотите зарегистрироваться? (да/нет): ")

    if answer.lower() == "да":
        registration_date = date.today()
        registration_status = "Зарегистрирован"

        print("\n=== Регистрация ===")
        print("Пользователь:", user_name)
        print("Мероприятие:", event_name)
        print("Дата регистрации:", registration_date)
        print("Статус:", registration_status)
    else:
        print("Регистрация отменена.")


def search_event(user_name, user_age, user_category):
    """Ищет благотворительное мероприятие по направлению помощи."""

    category = user_category.lower()

    if category == "животные":
        event_name = "Благотворительная ярмарка помощи животным"
        event_city = "Москва"
        event_date = date(2026, 9, 20)
        event_min_age = 14

        organization_name = "Фонд помощи животным"
        organization_contact = "animals@example.ru"

    elif category == "дети":
        event_name = "Благотворительный праздник для детей"
        event_city = "Екатеринбург"
        event_date = date(2026, 9, 28)
        event_min_age = 14

        organization_name = "Фонд помощи детям"
        organization_contact = "children@example.ru"

    elif category == "экология":
        event_name = "Уборка городского парка"
        event_city = "Москва"
        event_date = date(2026, 9, 21)
        event_min_age = 14

        organization_name = "ЭкоВолонтер"
        organization_contact = "eco@example.ru"

    else:
        print("\nТакое направление не найдено.")
        print("Выберите: животные, дети или экология.")
        return

    print("\n=== Результат поиска ===")
    print("Найдено мероприятие:")
    print("Название:", event_name)
    print("Город:", event_city)
    print("Дата:", event_date)
    print("Минимальный возраст:", event_min_age)

    print("\nОрганизация:")
    print("Название:", organization_name)
    print("Контакты:", organization_contact)

    if can_participate(user_age, event_min_age):
        print("\nВы можете участвовать в этом мероприятии.")
        register_user(user_name, event_name)
    else:
        print("\nВы не можете участвовать в этом мероприятии.")
        print(
            "Для участия необходимо достичь возраста",
            event_min_age,
            "лет."
        )


print("=== Сервис поиска благотворительных мероприятий ===")

user_name = input("Введите ваше имя: ")
user_age = int(input("Введите ваш возраст: "))
user_category = input(
    "Введите направление помощи (животные, дети, экология): "
)

search_event(user_name, user_age, user_category)
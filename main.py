from datetime import date

print("=== Сервис поиска благотворительных мероприятий ===")

user_name = input("Введите ваше имя: ")
user_age = int(input("Введите ваш возраст: "))
user_category = input(
    "Введите направление помощи (животные, дети, экология): "
)

print("\n=== Результат поиска ===")

event_found = True


if user_category.lower() == "животные":
    event_name = "Благотворительная ярмарка помощи животным"
    event_city = "Москва"
    event_date = date(2026, 9, 20)
    event_min_age = 14

    organization_name = "Фонд помощи животным"
    organization_contact = "animals@example.ru"

elif user_category.lower() == "дети":
    event_name = "Благотворительный праздник для детей"
    event_city = "Екатеринбург"
    event_date = date(2026, 9, 28)
    event_min_age = 14

    organization_name = "Фонд помощи детям"
    organization_contact = "children@example.ru"

elif user_category.lower() == "экология":
    event_name = "Уборка городского парка"
    event_city = "Москва"
    event_date = date(2026, 9, 21)
    event_min_age = 14

    organization_name = "ЭкоВолонтер"
    organization_contact = "eco@example.ru"

else:
    event_found = False
    print("Такое направление не найдено.")
    print("Выберите: животные, дети или экология.")


if event_found:
    print("\nНайдено мероприятие:")
    print("Название:", event_name)
    print("Город:", event_city)
    print("Дата:", event_date)
    print("Минимальный возраст:", event_min_age)

    print("\nОрганизация:")
    print("Название:", organization_name)
    print("Контакты:", organization_contact)

    if user_age >= event_min_age:
        print("\nВы можете участвовать в этом мероприятии.")

        answer = input("Хотите зарегистрироваться? (да/нет): ")

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

    else:
        print("\nВы не можете участвовать в этом мероприятии.")
        print(
            "Для участия необходимо достичь возраста",
            event_min_age,
            "лет."
        )
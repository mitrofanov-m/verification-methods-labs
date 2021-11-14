# ЛР №3. Модульное тестирование. Тестовые дублёры. unittest.mock
# Цель
Получение практических навыков разработки модульных тестов с применением тестовых дублёров, а также определения их эффективности путём замера покрытия тестируемого кода.

Для более эффективного выполнения лабораторной работы рекомендуется почитать статью [об объектах Mock в python](https://realpython.com/python-mock-library/).

# Требуемые PyBuilder-зависимости
Начиная с версии языка >= Python 3.3 модуль unittest.mock является встроенным и не требует введения дополнительных зависимостей.

# Описание объекта исследований
Дан прототип проекта BankOnline. На начальном этапе разработки в нём созданы наброски небольшого функционального модуля, предназначенного для регистрации и логина пользователей в систему (реализация методов Register и Login в учебных целях значительно упрощена, в частности, отсутствует валидация формата адреса электронной почты и др.). Проект сделан с использованием системы сборки и управления зависимостями PyBuilder.

Определение класса AuthService (файл `./src/main/python/services.py`)
```python
from dao import UserDaoInterface
from model import User
from utils import PasswordHasherInterface
from typing import Optional


class AuthService:
    """Служба идентификации, аутентификации и авторизации.
    
    Attributes:
        userDao (UserDao): объект постоянного хранения информации о пользователях.
        passwordHasher (PasswordHasher): объект, выполняющий хэширование паролей в процессе
            регистрации/логина пользователей.

    """

    def __init__(self, userDao: UserDaoInterface, passwordHasher: PasswordHasherInterface) -> None:
        self.userDao = userDao
        self.passwordHasher = passwordHasher

    def register(self, email: str, password:str) -> Optional[User]:
        """Регистрация новой учетной записи пользователя в системе банка.
        
        Args:
            email (str): имя нового пользователя.
            password (str): пароль нового пользователя.
                Должен удовлетворять определенным требованиям (см.ТЗ)

        Returns:
            объект нового пользователя, если регистарация прошла устешно,
            None если пользователь с таким email уже есть в хранилище.
        
        """
        if email is None:
            raise ValueError("email is None")
        
        if email.strip() == '':
            raise ValueError("email is empty")

        if not password:
            raise ValueError("password is None")

        if len(password) < 12:
            raise ValueError("password too short")

        passwordHash: str = self.passwordHasher.computeHash(password)
        return self.userDao.create(email, passwordHash)

    def login(self, email: str, password: str) -> Optional[User]:
        """Идентификация и аутентификация пользователя в системе.

        Note:
            Вход в систему возможен только для ранее зарегестрированного пользователя

        Args:
            email (str): адрес электронной почты пользователя.
            password (str): пароль пользователя.

        Returns:
            объект существующего пользователя, если логин выполнен устешно,
            None если пользователя с таким email нет в хранилище или
            введён неправильный пароль.

        """
        user: User = self.userDao.findByEmail(email)
        if not user:
            return None

        passwordHash: str = self.passwordHasher.computeHash(password)
        if passwordHash != user.getPasswordHash():
            return None

        return user
```
Данный класс через конструктор принимает 2 параметра:
1. userDao типа UserDaoInterface
2. passwordHasher типа PasswordHasherInterface

Интерфейс **UserDaoInterface** (User Data Access Object) объявляет методы доступа к данным о пользователе. Т.е. он не определяет никакой конкретной реалзиации подсистемы хранения, а только задаёт контракт взаимодействия с ней. Конкретные механизмы хранения определятся в производных классах. Например, это может быть класс для хранения информации в СУБД postgres или класс для хранения информации в обычном тестовом файле и т.д.

Интерфейс **PasswordHasherInterface** объявляет методы хэширования паролей пользователей. Предназначен для решения проблемы хранения информации о паролях в БД. (Здесь не затрагивается вопрос "солёных" паролей, которые применяются для исключения атаки с использованием радужных таблиц). Так же как и в UserDao конкретный механизм хэширования определяется в подклассах (например, это может быть sha1, Стрибог и др.).

Какие реализации **UserDaoInterface** и **PasswordHasherInterface** будут использованы в процессе работы определяется конфигурационным файлом (в настоящее время не реализовано).

В качестве модели пользователя выступает простой класс **User** (файл `./src/main/python/model.py`), объекты которого возвращаются из методов Register и Login в случае успешного их выполнения:
```python
class User:
    def __init__(self, email: str, name: str, passwordHash: str, role: str) -> None:
        self.email = email
        self.name = name
        self.passwordHash = passwordHash
        self.role = role

    def getEmail(self) -> str:
        return self.email

    def getPasswordHash(self) -> str:
        return self.passwordHash
```
Определение интерфейса **UserDaoInterface** (файл `./src/main/python/dao.py`)
```python
from typing import Optional
from model import User


class UserDaoInterface:
    """Хранилише информации пользователей."""

    def create(self, email: str, passwordHash: str) -> Optional[User]:
        """Создание нового пользователя в хранилище.
        
        Note:
            Успешное создание нового пользователя возможно, только если в
            хранилище отсутсвует учётная запись с адресом email.

        Args:
            email (str): адрес электронной почты нового пользователя.
            passwordHash (str): хэш от пароля создаваемого пользователя.
        
        Returns:
            объект нового пользователя.
            None, если такой пользователь уже есть в хранилище.

        """
        pass

    def findByEmail(email: str) -> Optional[User]:
        """Поиск пользователя по email.
        
        Args:
            email (str): адрес электронной почты пользователя.
        
        Returns:
            объект пользователя с адресом email.
            None если пользователь с адресом email не найден.
        """
        pass

    def update(self, user: User) -> None:
        """Обновление информации о пользователе.

        Args:
            user (str): объект пользователя с новыми данными.

        """
        pass

    def delete(self, user: User) -> None:
        """Удаление информации о пользователе user.

        Args:
            user (str): объкт удаляемого пользователя.

        """
        pass
```
Определение интерфейса **PasswordHasherInterface** (файл `./src/main/python/utils.py`)
```python
class PasswordHasherInterface:
    """Вычисление хэш-значения от пароля"""
    
    def computeHash(self, password: str) -> str:
        """Вычисление значения хэш-функции от пароля
    
        Args:
            password (str): строковое представление пароля

        Returns:
            Возвращает хэш от пароля в виде строки шестрадцатеричных цифр

        """
        pass
```

# Требования к методу Register [Auth][Reg]
Успешная регистрация выполняется при соблюдении всех следующих условий:
1. email пользователя не должен быть пустым
2. пароль не должен быть пустым
3. пароль не должен быть короче 12 символов
4. учётная запись с email регистрируемого пользователя должна отсутствовать в хранилище пользоватлей

# Требования к методу Login [Auth][Login]
Успешный вход в систему выполняется при соблюдении всех следующих условий:
1. учётная запись с именем входящего пользователя должна существовать в хранилище
2. Хэш от переданного пароля должен совпадать с хэшем, соответствующим учетной записи пользователя из хранилища.

# Постановка задачи
Разработать модульные тесты, проверяющие корректность реализации методов Register и Login на соответствие требованиям, указанным в пунктах выше:
1. [Auth][Reg]
2. [Auth][Login]

# Проблема
Предположим, что в настоящий момент разработка конкретных реализаций классов-наследников для PasswordHasherInterface и UserDaoInterface ведётся в другом отделе и ещё далека от завершения, а тестировать надо начать как можно раньше.

Плюс ко всему, развертывание инфраструктуры реальных хранилищ достаточно трудоёмкая операция, которая требует дополнительных затрат, в виде постоянного поддержания актуальности тестовых наборов данных, установки и настройки реальных СУБД, а также сложности модификации тестовых наборов данных.

# Решение
С целью изоляции объекта тестирования от окружения предлагается применить mock-классы.
Более подробную информацию можно найти в задании "Модульное тестирование. Тестовые дублёры. unittest.mock".

# Разработка тестов
Как правило, разработка тестов начинается с позитивных сценариев, а затем переходят к негативным.

В процессе разработки тестов возникнет необходимость в создании объекта класса **AuthService**, которому в конструктор необходимо передать 2 зависимости: ссылку на объект, реализующий интерфейс **UserDaoInterface**, и ссылку на объект, реализующий интерфейс **PasswordHasherInterface**.

Как было сказано ранее, конкретных реализаций этих классов у нас нет, поэтому сделаем для них Mock-объекты, которые сконфигурируем на трубуемое для выполнения тестов поведение.

## Позитивный тест процедуры регистрации в системе
Из требований следует, что успешная регистарация в системе выполняется, когда email не пустой, пароль не пустой, пароль не менее 12 символов, пользователь с указанным email отсутствует в хранилище учетных записей.

Для тестирования этого сценария необходимо создать объект класса **AuthService**, вызывать у него метод register, передав в него какие-нибудь тестовые значения email (`student@email.ru`) и пароля (`pa$$w0rd1111`), а затем проверить вернувшийся из метода объект **User**.
При этом тестовые дублёры конфигурируются следующим образом:
1. Объект, реализующий интерфейс **UserDaoInterface**, при вызове метода create с указанными параметрами должен вернуть объект **User**, содержащий информацю о новом пользователе. Таким образом моделируется ситуация, при которой пользователя с указанным email в хранилище ещё нет.
2. Объект, реализующий интерфейс **PasswordHasherInterface**, при вызове метода computeHash с параметром `pa$$w0rd1111` должен вернуть значение хэш-функции от данной строки. Предположим, что используется какая-то произвольная функция, которая для строки `pa$$w0rd1111` возвращает хэш-значение `12345678` (очень плохая функция, надо заметить).

## Негативный тест процедуры регистрации в системе
Негативный сценарий возможен в случае невыполнения одного из условий требований [Auth][Reg]:
- либо email пустой, либо пароль пустой, либо пароль меньше 12 символов, либо пользователя с заданным именем уже существует в хранилище.
Для примера реализуем тест на проверку пустого email, в случае которого будет сгенерировано исключение `IllegalArgumentException` с сообщением `"email is empty"`.
В этом сценарии не потребуется конфигурирование Mock-объектов, т.к. выполнение функции Register не дойдёт до мест обращения к методам computeHash и create .

Исходный текст тестирующего класса `AuthServiceTest` с тестовыми примерами (файл `./src/unittest/python/services_tests.py`)
```python
import unittest
from unittest.mock import call, patch
from services import AuthService
from dao import UserDaoInterface
from utils import PasswordHasherInterface
from model import User

class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.userDao = UserDaoInterface()
        self.passwordHasher = PasswordHasherInterface()
        self.authService = AuthService(self.userDao, self.passwordHasher)

    def test_register_new_user_should_success(self):
        # сконфигурируем mock-объектам поведение, требуемое для выполнения позитивного теста.
        # Т.е. метод create объекта UserDao должен быть вызыван с параметром email, равным student@email.ru,
        # а параметру password после вызова должно быть присвоено значение хэш-функции от пароля pa$$w0rd1111.
        # Предположим, используется произвольная хэш-функция, которая для строки pa$$w0rd1111 дает значение
        # "12345678"
        side_effect_computeHash = lambda password: "12345678" if password == "pa$$w0rd1111" else None
        side_effect_create = lambda *args: User("student@email.ru", "petrov", "12345678", "USER") \
                                if args == ("student@email.ru", "12345678") else None

        with patch.object(PasswordHasherInterface, "computeHash", side_effect=side_effect_computeHash), \
             patch.object(UserDaoInterface, "create", side_effect=side_effect_create):

            newUser = self.authService.register("student@email.ru", "pa$$w0rd1111")
            # Проверка утверждений теста
            self.assertEqual("student@email.ru", newUser.getEmail())
            # Проверка поведения мокированного объекта
            self.passwordHasher.computeHash.assert_called_once_with('pa$$w0rd1111')
            self.userDao.create.assert_called_once_with("student@email.ru", "12345678")

    def test_register_with_empty_email_should_throw_exception(self):
        with self.assertRaisesRegex(ValueError, "email is empty"):
            self.authService.register("", "pa$$w0rd1111")
```
# Задание
Дополнить класс `TestAuthService` тестами для покрытия всех позитивных и негативных сценариев методов Register и Login.

Выполнить тестирование с записью результатов выполнения тестов в отдельный файл: `mvn test | tee report.txt`

С использованием библиотеки coverage измерить покрытие разработанного набора тестов.
Загузить в `gitlab.studware.ru` полученные файлы проекта `BankOnline`.
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
    
    # positive tests

    def test_register_new_user_should_success(self):
        # сконфигурируем mock-объектам поведение, требуемое для выполнения позитивного теста.
        # Т.е. метод create объекта UserDao должен быть вызыван с параметром email, равным student@email.ru,
        # а параметру password после вызова должно быть присвоено значение хэш-функции от пароля pa$$w0rd1111.
        # Предположим, используется произвольная хэш-функция, которая для строки pa$$w0rd1111 дает значение
        # "12345678"
        side_effect_computeHash = lambda password: "12345678" if password == "pa$$w0rd1111" else None
        side_effect_create = lambda *args: User("student@email.ru", "petrov", "12345678", "USER") if args == ("student@email.ru", "12345678") else None

        with patch.object(PasswordHasherInterface, "computeHash", side_effect=side_effect_computeHash), \
             patch.object(UserDaoInterface, "create", side_effect=side_effect_create):

            newUser = self.authService.register("student@email.ru", "pa$$w0rd1111")
            # Проверка утверждений теста
            self.assertEqual("student@email.ru", newUser.getEmail())
            # Проверка поведения мокированного объекта
            self.passwordHasher.computeHash.assert_called_once_with('pa$$w0rd1111')
            self.userDao.create.assert_called_once_with("student@email.ru", "12345678")

    def test_login_existed_user_shoud_success(self):
        side_effect_findByEmail = lambda email: User("student@email.ru", "petrov", "12345678", "USER") if email == "student@email.ru" else None
        side_effect_computeHash = lambda password: "12345678" if password == "pa$$w0rd1111" else None

        with patch.object(PasswordHasherInterface, "computeHash", side_effect=side_effect_computeHash), \
             patch.object(UserDaoInterface, "findByEmail", side_effect=side_effect_findByEmail):
            
            user = self.authService.login("student@email.ru", "pa$$w0rd1111")
            # Проверка утверждений теста
            self.assertEqual("student@email.ru", user.getEmail())
            # Проверка поведения мокированного объекта
            self.passwordHasher.computeHash.assert_called_once_with('pa$$w0rd1111')
            self.userDao.findByEmail.assert_called_once_with("student@email.ru")

    # negative tests

    def test_register_with_empty_email_should_throw_exception(self):
        with self.assertRaisesRegex(ValueError, "email is empty"):
            self.authService.register("", "pa$$w0rd1111")
    
    def test_register_with_None_email_should_throw_exception(self):
        with self.assertRaisesRegex(ValueError, "email is None"):
            self.authService.register(None, "pa$$w0rd1111")

    def test_register_with_None_password_should_throw_exception(self):
        with self.assertRaisesRegex(ValueError, "password is None"):
            self.authService.register("student@email.ru", None)

    def test_register_with_password_lenth_less_than_12_should_throw_exception(self):
        with self.assertRaisesRegex(ValueError, "password too short"):
            self.authService.register("student@email.ru", "pa$$w0rd")

    def test_register_with_already_registered_email_shoud_return_None(self):
        side_effect_computeHash = lambda password: "12345678" if password == "pa$$w0rd1111" else "87654321"
        # имитируем поведение UserDaoInterface.create, который согласно описанию:
        # > Returns:
        # >    объект нового пользователя.
        # >    None, если такой пользователь уже есть в хранилище.
        side_effect_create = [User("student@email.ru", "petrov", "12345678", "USER"), None]

        with patch.object(PasswordHasherInterface, "computeHash", side_effect=side_effect_computeHash), \
             patch.object(UserDaoInterface, "create", side_effect=side_effect_create):

            newUser = self.authService.register("student@email.ru", "pa$$w0rd1111")
            self.assertEqual("student@email.ru", newUser.getEmail())
            # попытка повторной регистрации должна вернуть None
            newUserAgain = self.authService.register("student@email.ru", "AnotherPa$$w0rd1111")
            self.assertIsNone(newUserAgain)
            # Проверка поведения мокированного объекта
            computeHash_calls = [call("pa$$w0rd1111"), call("AnotherPa$$w0rd1111")]
            self.passwordHasher.computeHash.assert_has_calls(computeHash_calls)
            create_calls = [call("student@email.ru", "12345678"), call("student@email.ru", "87654321")]
            self.userDao.create.assert_has_calls(create_calls)

    def test_login_with_incorrect_password_should_return_None(self):
        side_effect_findByEmail = lambda email: User("student@email.ru", "petrov", "12345678", "USER") if email == "student@email.ru" else None
        side_effect_computeHash = lambda password: "87654321" if password == "incorrectPa$$w0rd1111" else None

        with patch.object(PasswordHasherInterface, "computeHash", side_effect=side_effect_computeHash), \
             patch.object(UserDaoInterface, "findByEmail", side_effect=side_effect_findByEmail):
            
            user = self.authService.login("student@email.ru", "incorrectPa$$w0rd1111")
            # Проверка утверждений теста
            self.assertIsNone(user)
            # Проверка поведения мокированного объекта
            self.passwordHasher.computeHash.assert_called_once_with('incorrectPa$$w0rd1111')
            self.userDao.findByEmail.assert_called_once_with("student@email.ru")

    def test_login_with_incorrect_email_should_return_None(self):
        side_effect_findByEmail = lambda email: User("student@email.ru", "petrov", "12345678", "USER") if email == "student@email.ru" else None

        with patch.object(UserDaoInterface, "findByEmail", side_effect=side_effect_findByEmail):
            unregistredUser = self.authService.login("teacher@email.ru", "Pa$$w0rd1111")
            # Проверка утверждений теста
            self.assertIsNone(unregistredUser)
            # Проверка поведения мокированного объекта)
            self.userDao.findByEmail.assert_called_once_with("teacher@email.ru")
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
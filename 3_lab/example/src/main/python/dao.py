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
    
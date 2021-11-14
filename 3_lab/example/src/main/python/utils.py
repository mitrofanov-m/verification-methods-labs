
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
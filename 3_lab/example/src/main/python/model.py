
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


def checkPassword(password: str) -> str:
    uppercase: bool = False
    lowercase: bool = False
    specialcharacters: bool = False
    digits: bool = False
    strength: str = ""

    for i in range(len(password)):
        if password[i].isupper():
            uppercase = True
        if password[i].islower():
            lowercase = True
        if password[i].isdigit():
            digits = True

    if ("~" in password) or ("!" in password) or ("@" in password) or \
            ("#" in password) or ("$" in password) or ("%" in password) or \
            ("^" in password) or ("&" in password) or ("*" in password):
        specialcharacters = True

    if len(password) < 8:
        strength = "TooShort"
    else:
        if (uppercase and lowercase) or digits or specialcharacters:
            strength = "Weak"

        if ((uppercase and lowercase) and digits) or \
                ((uppercase and lowercase) and specialcharacters) or \
                (digits and specialcharacters):
            strength = "Medium"

        if uppercase and lowercase and digits and specialcharacters:
            strength = "Strong"

    return strength

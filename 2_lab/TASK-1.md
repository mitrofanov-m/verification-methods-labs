# ЛР №2-1. Модульное тестирование. Unittest

# Общие сведения
Целью данной лабораторной работы является практическое освоение основ разработки модульных тестов на языке программирования Python с использованием фреймворка тестирования Unittest, а также измерения метрик тестового покрытия разработанной системы тестов.

В качестве объектов тестирования будут выступать:
1. метод простейшей классификации сложности пароля;
2. реализация операции зашифрования/расшифрования в соответствии с алгоритмом "Магма";
3. реализация вычисления хэш-функции "Стрибог".


# Требуемое ПО
Для запуска разработанных приложений необходимо установить Python версии 3.7 и выше.

Сборка проекта и управление библиотеками-зависимостями будет осуществляться с использованием утилиты Pybuilder.

Разработка, компоновка и запуск модульных тестов будет выполняться с использованием фреймворка тестирования Unittest.

Для определение покрытия кода применяется библиотека Coverage.

В качестве редактора кода предлагается использовать одно из следующих решений:
- Atom
- Microsoft Visual Studio Code
- Sublime Text

Обращаю внимание, что данные инструменты будут использоваться только как редакторы кода, а не полноценные среды разработки со всеми их возможностями по поддержке проектов, отладке и др. Компиляция и запуск проектов будет выполняться из командного интерпретатора.


# Python
## Скачивание
В этой и последующих лабораторных работах при использовании Python будет применяться Python 3.7.
Скачать данный дистрибутив можно по следующей [ссылке](https://www.python.org/downloads/).

## Настройка окружения
При создании проетка на языке Python хорошим тоном является конфигурация нового виртуального окружения для проекта. Это позволит избежать конфликтов при скачивании пакетов, а так же даст возможность получить список зависимостей для Вашего проекта.
``` bash
$ python3 -m venv lab_env
$ source lab_env/bin/activate
(lab_env)$
```

## Проверка работоспособности
Проверим версию используемого компилятора:
```bash
(lab_env)$ python --version
```
Вывод команды должен иметь вид:
```
Python 3.7.6
```


# PyBuilder
Чтобы скачать данный пакет, введите следующую команду
``` bash
(lab_env)$ pip install pybuilder
```
Вывод команды должен иметь вид:
```
Using cached https://files.pythonhosted.org/packages/94/2f/ea044bb5b7aeb18f710842b6bac3527f7342e9e64e05f88f254fe14343bf/pybuilder-0.13.3-py3-none-any.whl
Installing collected packages: pybuilder
Successfully installed pybuilder-0.13.3
```
Вы так же можете подробнее познакомиться с проектом через [документацию](https://pybuilder.io/documentation/).

# Unittest, Coverage
Данные библиотеки будут скачаны, установлены и настроены с использованием возможностей PyBuilder.

# Создание PyBuilder-проекта
Создадим папку проекта
``` bash
(lab_env)$ mkdir psv
(lab_env)$ cd psv
``` 
Введите следующую команду:
``` bash
$ pyb --start-project
Project name (default: 'helloworld') : ru.bk252.kkso17
Source directory (default: 'src/main/python') : 
Docs directory (default: 'docs') : 
Unittest directory (default: 'src/unittest/python') : 
Scripts directory (default: 'src/main/scripts') : 
Use plugin python.flake8 (Y/n)? (default: 'y') : n
Use plugin python.coverage (Y/n)? (default: 'y') : n
Use plugin python.distutils (Y/n)? (default: 'y') : n
```
Назовем проект `ru.bk252.kkso17`, настройки директорий оставим без изменений, откажемся от установки дополнительных модулей. В результате выполнения команды в текущей директории должна быть создана минимально-необходимая структура каталогов.


# Создание объекта тестирования
Необходимо создать файл `psv/src/main/python/app.py` с кодом, представленным ниже.
Данный код взят из реально заданного на stackoverflow [вопроса](https://stackoverflow.com/questions/54869952/password-strength-validation-java) и преобразован под решение задания на Python:

``` python
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
```

# Требования к объекту тестирования
Автор кода описал следующие условия классификации:
1. Password should be 8 characters long
2. it should contain at least one uppercase and one lowercase letter
3. it should contain one or more of these special characters: ~, !, @, #, $, %, ^, &, *
4. it should contain one or more digits in it

The output is defined as:
1. if first condition fails, then output = "Too short"
2. if only two conditions including first one is met, then output = "Weak"
3. if only three conditions including first one is met, then output = "Medium"
4. if all four conditions are met, then output = "Strong"

# Классы эквивалентности
По заданным условиям можно выделить следующие классы эквивалентности паролей:
1. Все пароли менее 8 символов. Относятся к классу "Too Short"
2. Все пароли не менее 8 символов, состоящие из символов верхнего и нижнего регистров. 3. Относятся к классу "Weak".
4. Все пароли не менее 8 символов, состоящие из специальных символов. Относятся к классу "Weak" .
5. Все пароли не менее 8 символов, состоящие из цифр. Относятся к классу "Weak" .
6. Все пароли не менее 8 символов, состоящие из не менее одного символа нижнего и верхнего регистров и не менее одного специального символа. Относятся к классу "Medium" .
7. Все пароли не менее 8 символов, состоящие из не менее одного символа нижнего и верхнего регистров и не менее одной цифры. Относятся к классу "Medium" .
8. Все пароли не менее 8 символов, состоящие из не менее одного специального символа и не менее одной цифры. Относятся к классу "Medium" .
9. Все пароли не менее 8 символов, состоящие из не менее одного символа нижнего и верхнего регистров и не менее одного специального символа и не менее одной цифры. Относятся к классу "Strong" .

# Разработка модульного теста
Для PyBuilder проектов принято следующее соглашение:
Тестирующий код для метода `checkPassword`, который расположен в файле `/psv/src/main/python/app.py`,
размещается в классе `TestCheckPassword`, который располагается в файле с суффиксом *_tests `/psv/src/unittest/python/app_tests.py`

```python
import unittest
from app import checkPassword


class TestCheckPassword(unittest.TestCase):
    def test_length_less_than_8_is_TooShort(self):
        expectedResult: str = "TooShort"
        result: str = checkPassword("Pass")
        self.assertEqual(expectedResult, result)

```
Запуск тестов на выполнение (ключ -v позволяет увидеть ошибки, в случае, если тест закончился с флагом failure)
```
(lab_env)$ pyb -v
```

# Задание
## Базовое
1. Создать в директории проекта git репозиторий
2. Дополнить систему тестов для паролей классов "Weak", "Medium", "Strong" с учётом всех возможных классов эквивалентности. Т.е. должны быть разработаны следующие тестовые методы:
    1. lengthEquals8ContainsUpperLowerIsWeak
    2. lengthGreater8ContainsOnlyUpperLowerIsWeak
    3. lengthGreater8ContainsOnlySpecialIsWeak
    4. lengthGreater8ContainsOnlyDigitIsWeak
    5. lengthGreater8ContainsUpperLowerSpecialIsMedium
    6. lengthGreater8ContainsUpperLowerDigitIsMedium
    7. lengthGreater8ContainsSpecialDigitIsMedium
    8. lengthGreater8ContainsUpperLowerSpecialDigitIsStrong
3. Провести тестирование, сохранив отчёт о тестировании: `pyb -v | tee -a report.txt`
4. Выполнить коммит текущего состояния
5. ~~Определить причину, по которой тесты, выделенные жирным шрифтом, завершаются статусом "Failure".~~
6. ~~Исправить ошибку.~~
7. ~~Выполнить тесты. Убедиться, что тесты проходят успешно: `pyb -v | tee -a report.txt`~~
8. ~~Выполнить коммит исправлнной версии.~~
9. Создать в gitlab.studware.ru проект с именем psv и загрузить в него полученный репозиторий с отчётом о выполнеии тестов.

## Дополнительное
1. Создать в локальном репозитории новую ветку parametrized
2. Заменить все тесты из базового задания одним параметризированным тестом
3. Выполнить тест, получив отчёт о тестировании
4. Выполнить коммит состояния в новой ветке
5. Загрузить новую ветку (включая отчёт о тестировании) в созданный в рамках базового задания репозиторий.

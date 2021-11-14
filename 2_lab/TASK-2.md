# ЛР №2-2. Дополнение. Coverage

# Описание

Целью данного дополнения к Лабораторной работе №2 является получение практических навыков определения тестового покрытия структурных элементов кода с использованием метрик на основе инструкций и ветвей.

Подключение Coverage
Подключить библиотеку Coverage к проекту на основе системы сборки PyBuilder можно с использованием её системы плагинов, добавив в файл `build.py` вызов метода , содержащий соответсвующий плагин:
```python
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.coverage") # <--



name = "ru.bk252.kkso17"
default_task = "publish"


@init
def set_properties(project):
    pass
```
Указанная конфигурация плагина позволяет запустить сбор метрик покрытия на этапе выполнения тестов.
Таким образом после выполнения команды mvn test в директрории проекта должна быть создана директория `target/reports/ru.bk252.kkso17_coverage_html`, содержащий файл с отчётом о поктырии `index.html`.

# Задание
1. Полчить отчёт о тестовом покрытии разработанной системы тестов.
2. Зафиксировать в репозитории полученный отчёт (и для ветки `master` и для ветки `parametrized`)
3. Выполнить `git push`, обновив удалённый репозиторий в gitlab.studware.ru
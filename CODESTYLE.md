# Code Style
## Используемые либы

_[black](https://github.com/psf/black)_

_[isort](https://pycqa.github.io/isort)_ — сортирует импорты

_[darker](https://github.com/akaihola/darker)_ — нажимает black на измененные с последнего коммита строки (+ (опционально) isort, mypy, etc).

_[pre-commit](https://pre-commit.com/)_ — Управляет пре-коммит хуками гита. Пре-коммит хуки проверяют файлы со стейджа на соответствие заданным в конфиг-файле требованиям.

## Установка

### Установка либ
pip install darker[isort] pre-commit --upgrade
pre-commit install --install-hooks

### Конфигурация 
_black_, _isort_, _darker_ используют конфигурацию из *pyproject.toml*, лежащего в руте репозитория.

_pre-commit_ пользуется *.pre-commit-config.yaml*, лежащим в руте репозитория. После изменений в конфиг файле может потребоваться

    pre-commit install --install-hooks

## Использование
### Если помним про красоту
Делаем изменения, наводим красоту.

    darker .

Добавляем изменения на стейдж.

    git add .

Коммитим успешно.

    git commit -m 'samplemessage'

### Если забываем про красоту
Делаем изменения, добавляем изменения на стейдж.

    git add .

Пытаемся коммитнуть и фейлимся.

    git commit -m 'samplemessage'
    darker...................................................................Failed
    - hook id: darker
    - files were modified by this hook

_darker_ модифицирует несоответствующие требованиям файлы, добавляем их.

    git add .

Коммитим успешно.

    git commit -m 'samplemessage'

#### NB
Если в застейджнутых файлах есть также незастейджнутые изменения _darker_ не сможет их автоматически привести в порядок. В таком случае:

    git stash -k
    darker .
    git add .
    git commit -m 'samplemessage'
    git stash pop

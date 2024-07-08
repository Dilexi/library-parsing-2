# Парсирование библиотеки
## Описание
Проект создан для парсирования онлайн-библиотеки. Загружает содержание книг и обложки в разные папки, а также собирает всю информацю о книгах в файл.


## Установка
Скачайте необходимые файлы, затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей и установить зависимости. Зависимости можно установить командой, представленной ниже.


Установите зависимости командой:

```python
  pip install -r requirements.txt
```

## Пример запуска скрипта
Для запуска скрипта у вас уже должен быть установлен Python3.

Для запуска программы укажите страницу каталога с научной фантастикой, с которой нужно начать скачивать, после аргумента `--start_page` и страницу каталога с научной фантастикой, до которой нужно скачивать, после аргумента `--end_page`. Укажите аргумент `--skip_txt`, если не хотите скачивать текст книг, и аргумент `--skip_imgs`, если не хотите скачивать обложки к книгам. Укажите путь для скачивания книг и обложек после аргумента `--dest_folder` и путь к JSON файлу с информацией о книгах после аргумента `--json_path`. Пример:

```python
python main.py --start_page <страница> --end_page <страница> --skip_txt --skip_imgs --dest_folder <путь> --json_path <путь_к_json>
```


## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/modules/).
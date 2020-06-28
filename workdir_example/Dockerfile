FROM alpine
# Зададим рабочую директорию
WORKDIR /dir_1/dir_2
# Создадим файл file_of_dir_2
RUN touch file_of_dir_2
# Перейдём на вышележащий каталог и создадим файл file_of_dir_1
RUN cd .. && touch file_of_dir_1
# Создадим файл another_file
RUN touch another_file

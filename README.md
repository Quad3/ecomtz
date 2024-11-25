### Цель:
#### Разработать скрипт, который собирает открытые данные с сайта и сохраняет их.

#### Источники:
1.	https://www.wildberries.ru/
2.	https://www.ozon.ru/
3.	https://www.auchan.ru/

#### Задача:
1. -[x] Из сайтов источников требуется собрать данные из любой категории:
    * Ссылка на товар
    * Название товара
    * Цена со скидкой
    * Цена без скидки
    * Остатки
2. -[x] Количество страниц в категории ограничить до 3.
3. -[x] Обработать возможные ошибки и блокировки.
4. -[x] Реализовать асинхронный подход как к постраничной пагинации, так и к итерации по ссылкам товаров, так же ограничить число одновременных сетевых запросов.
5. -[x] Данные сохранить в таблицу PostgreSQL.
6. -[x] Docker compose.

Допускается использовать эмуляторы для получения параметров, которые могут потребоваться в запросах к ресурсу.

#### Необязательные задачи:
1. -[ ] Написать скрипт для сбора данных с мобильной версии на один из источников на выбор.

### Как запустить:
Скачайте проект
```bash
git clone https://github.com/Quad3/ecomtz.git ecomtz
```

Переместитесь в папку с проектом
```bash
cd ecomtz
```

Запустите docker-compose.
```bash
docker-compose up
```

### Использованные технологии:
* Python (Многопоточность)
* Selenium (Undetected Chrome Driver)
* BeautifulSoup
* SQLAlchemy, PostgreSQL

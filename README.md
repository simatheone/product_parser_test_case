# Тестовое задание

## Оглавление
- [Тестовое задание](#тестовое-задание)
  - [Оглавление](#оглавление)
  - [Задание](#задание)
  - [Запуск проекта](#запуск-проекта)
    - [Unix systems](#unix-systems)
    - [Windows](#windows)
  - [Описание ендпоинтов](#описание-ендпоинтов)

## Задание
<details>
    <summary>Описание задания</summary><br />

**Цель задания:** создать сервис на FastAPI, который будет взаимодействовать с сайтом https://www.wildberries.ru/.

Необходимо реализовать 4 конечные точки для работы с номенклатурой.

**Требования:**
1. Используйте FastAPI для разработки сервиса.
2. Используйте парсинг данных с сайта https://www.wildberries.ru/ с использованием библиотеки `requests`.
3. Реализуйте 4 конечные точки:
   - Добавить номенклатуру: пользователь указывает nm_id, сервис парсит данные с сайта www.wildberries.ru и сохраняет их в базу данных `PostgreSQL`
   - Получить товар по номенклатуре
   - Получить все товары
   - Удалить товар по номенклатуре

4. Товар должен содержать следующие поля:
    - nm_id
    - name
    - brand
    - brand_id
    - site_brand_id
    - supplier_id
    - sale
    - price
    - sale_price
    - rating
    - feedbacks
    - colors
5. Используйте `Docker` для развертывания сервиса.
6. Используйте `SQLAlchemy` для работы с базой данных `PostgreSQL`.

**Дополнительное задание:**

1. Реализуйте задачу в `Celery` для обновления карточек товаров, которые хранятся в базе данных.
2. Настройте подключение `CORS` для сервиса.
3. Дополнительное поле в таблице (`quantity` - количество товара в наличии). Обновление остатков.

**Результат:**

Ссылка на **github**, **Dockerfile** для развертывания сервиса, и инструкцию по его
развертыванию и использованию.

**Подсказка:**

Пример страницы товара: https://www.wildberries.ru/catalog/139760729/detail.aspx

**В случае использования технологий, не указанных в требованиях задание будет считаться нерешенным.**
</details>

#
## Запуск проекта

1. Клонировать репозиторий
```shell
HTTPS
git clone https://github.com/simatheone/product_parser_test_case.git

SSH
git clone git@github.com:simatheone/product_parser_test_case.git
```
2. Перейти в директорию с проектом:
```shell
cd product_parser_test_case/
```


### Unix systems
3. Выполнить команду по созданию и запуску контейнеров:
```shell
make up
```
4. Выполнить миграции:
```shell
make migrate
```
Документация к API доступна по ссылке: http://localhost:8000/docs/
> либо выполнить команду `make view-docs`

Для получения полного списка доступных комманд выполните:
```shell
make help
```


### Windows
3. Перейти в директорию `docker`, запустить создание и запуск контейнеров:
```shell
cd docker/

docker-compose up -d --build
```
4. Выполнить миграции:
```shell
docker-compose exec backend alembic upgrade head
```
Документация к API доступна по ссылке: http://localhost:8000/docs/

5. Для остановки и удаления контейнеров выполните:
```shell
docker-compose down
```

[:top: Вернуться к оглавлению](#оглавление)

#
## Описание ендпоинтов

В проекте доступно 4 ендпоинта:
- `/products/all?page=1&size=10` - получение списка всех продуктов, добавленных в базу данных;
- `/products/{product_id}/` - получение продукта по его **id**;
- `/products/{product_id}/` - удаление продукта по его **id**;
- `/products/` - создание нового продукта.

---
`GET /products/all?page=1&size=10`

Данный ендпоинт принимает query параметры `page` и `size` для пагинации запроса. 
Возвращает список всех продуктов, с учетом параметров `page` и `size`. 

**Пример запроса:**
```curl
curl -X 'GET' \
  'http://localhost:8000/products/all?page=1&size=10' \
  -H 'accept: application/json'
```

**Пример ответа:**
```json
{
  "items": [
    {
      "nm_id": 134386495,
      "name": "Футболка мужская набор 3 шт однотонные хлопок",
      "brand": "OKO-group",
      "brand_id": 93472,
      "site_brand_id": 103472,
      "supplier_id": 409934,
      "sale": 42,
      "price": 231100,
      "sale_price": 134000,
      "rating": 5,
      "feedbacks": 2199,
      "quantity": 1168,
      "colors": [
        {
          "color_id": 4,
          "name": "черный"
        },
     ]
    },
    {
      "nm_id": 143422254,
      "name": "Футболка мужская набор 3 шт однотонные хлопок",
      "brand": "OKO-group",
      "brand_id": 93472,
      "site_brand_id": 103472,
      "supplier_id": 409934,
      "sale": 40,
      "price": 231100,
      "sale_price": 138600,
      "rating": 5,
      "feedbacks": 2199,
      "quantity": 654,
      "colors": [
        {
          "color_id": 4,
          "name": "черный"
        }
      ]
    }
  ],
  "total": 6,
  "page": 1,
  "size": 3,
  "pages": 2
}
```

Если в базе нет продуктов, вернется пустой список.

**Пример ответа:**
```json
{
  "items": [],
  "total": 0,
  "page": 1,
  "size": 10,
  "pages": 0
}
```

[:top: Вернуться к оглавлению](#оглавление)

---
`GET /products/{product_id}/` - получение продукта по его **id**;

Данный ендпоинт принимает `id` продукта в качестве параметра пути (**path parameter**) и возвращает информацию из базы о данном продукте.

**Пример запроса:**
```curl
curl -X 'GET' \
  'http://localhost:8000/products/111' \
  -H 'accept: application/json'
```

**Пример ответа:**
```json
{
  "nm_id": 111,
  "name": "Пуловер",
  "brand": "Y.O.U",
  "brand_id": 987,
  "site_brand_id": 439,
  "supplier_id": 458,
  "sale": 0,
  "price": 105000,
  "sale_price": 105000,
  "rating": 0,
  "feedbacks": 0,
  "quantity": 0,
  "colors": [
    {
      "color_id": 2,
      "name": "коричневый"
    }
  ]
}
```

При попытке получить продукт, который не был сохранен в базе, вернется ошибка со статус кодом 404 и сообщением:
```shell
{
  "detail": "Product does not exist."
}
```

[:top: Вернуться к оглавлению](#оглавление)

---
`DELETE /products/{product_id}/` - удаление продукта по его **id**;

Данный ендпоинт принимает `id` продукта в качестве параметра пути (**path parameter**) и возвращает статус код 204, если продукт был удален из базы.

```curl
curl -X 'DELETE' \
  'http://localhost:8000/products/111' \
  -H 'accept: */*'
```

При попытке повторно удалить продукт из базы, вернется ошибка со статус кодом 404 и сообщением:
```json
{
  "detail": "Product does not exist."
}
```

[:top: Вернуться к оглавлению](#оглавление)

---
`POST /products/`
Данный ендпоинт принимает в теле запроса `id` продукта, который должен быть сохранен в базу.

**Пример запроса:**
```curl
curl -X 'POST' \
  'http://localhost:8000/products/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "nm_id": 139760619
}'
```

**Request body (JSON):**

```json
{
    "nm_id": 139760619
}
```

**Пример ответа:**
```json
{
  "nm_id": 139760619,
  "name": "iPhone 14 Pro Max 1TB (США)",
  "brand": "Apple",
  "brand_id": 6049,
  "site_brand_id": 16049,
  "supplier_id": 887491,
  "sale": 23,
  "price": 19999000,
  "sale_price": 15399200,
  "rating": 4,
  "feedbacks": 7,
  "quantity": 18,
  "colors": [
    {
      "color_id": 1,
      "name": "серый"
    }
  ]
}
```

При попытке повторно добавить продукт в базу, вернется ошибка со статус кодом 400 и сообщением:
```json
{
  "detail": "Product with this id already exists."
}
```

Если по указанному в запросе `id` не удается найти продукт, вернется ошибка со статус кодом 404 и сообщением:
```shell
{
  "detail": "Unable to find a product with the provided ID. Check the ID of the product you are entering."
}
```

В случае, если по каким-то причинам не удалось получить информацию о продукте от сайта **wildberries**, вернется ошибка со статус кодом 500 и сообщением:
```shell
{
  "detail": "Something went wrong on requesting data from the website."
}
```

[:top: Вернуться к оглавлению](#оглавление)

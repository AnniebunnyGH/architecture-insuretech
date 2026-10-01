# Задание 5: Проектирование GraphQL API для сервиса client-info

## 1. Проблема исходного REST API и цель перехода
* **Исходная проблема**: Карточка клиента в сервисе `client-info` содержит до 500 атрибутов. Разделение данных на отдельные REST-ресурсы (`/clients/{id}`, `/documents`, `/relatives`) привело к лавинообразному росту RPS: для типового сценария клиент вынужден делать 2–3 последовательных или параллельных HTTP-запроса (Roundtrips / Under-fetching). Передача же всех 500 атрибутов единым объектом привела бы к Over-fetching и замедлению веб-клиента.
* **Цель**: Предоставить единый гибкий GraphQL API, позволяющий вызывающим сервисам (`web-app`, `core-app`) запрашивать **ровно те поля и связи, которые необходимы в текущем сценарии**, в рамках одного сетевого запроса.

---

## 2. Маппинг операций REST $\rightarrow$ GraphQL

| Операция REST API | GraphQL эквивалент | Преимущество GraphQL |
|---|---|---|
| `GET /clients/{id}` | `client(id: ID!) { id name age }` | Клиент запрашивает только нужные поля карточки (защита от Over-fetching). |
| `GET /clients/{id}/documents` | `client(id: ID!) { documents { ... } }`<br>или `documents(clientId: ID!) { ... }` | Возможность выбрать только нужные атрибуты документов (например, без `expiryDate`). |
| `GET /clients/{id}/relatives` | `client(id: ID!) { relatives { ... } }`<br>или `relatives(clientId: ID!) { ... }` | Выборка родственников напрямую или через клиента. |
| **Композитный сценарий**<br>(Клиент + Документы + Родственники) | `client(id: ID!) { name documents { ... } relatives { ... } }` | **1 сетевой запрос вместо 3.** Сервис `client-info` снижает нагрузку по RPS в 3 раза. |

---

## 3. Схема GraphQL (SDL)

Схема сохранена в файле [`schema.graphql`](./schema.graphql):

```graphql
schema {
  query: Query
}

type Query {
  """Получить клиента по ID с гибким составом полей и связанных сущностей"""
  client(id: ID!): Client

  """Получить список документов клиента напрямую (эквивалент GET /clients/{id}/documents)"""
  documents(clientId: ID!): [Document!]!

  """Получить список родственников клиента напрямую (эквивалент GET /clients/{id}/relatives)"""
  relatives(clientId: ID!): [Relative!]!
}

type Client {
  id: ID!
  name: String!
  age: Int
  documents: [Document!]!
  relatives: [Relative!]!
}

type Document {
  id: ID!
  type: String!
  number: String!
  issueDate: String!
  expiryDate: String
}

type Relative {
  id: ID!
  relationType: String!
  name: String!
  age: Int
}
```

---

## 4. Примеры запросов под различные сценарии

### Сценарий А. Оформление полиса ОСАГО (Клиент + Документы)
В REST требовалось 2 вызова (`GET /clients/{id}` и `GET /clients/{id}/documents`). В GraphQL — один запрос без родственников:
```graphql
query GetClientForOsago($clientId: ID!) {
  client(id: $clientId) {
    id
    name
    documents {
      type
      number
      issueDate
    }
  }
}
```

### Сценарий Б. Семейная страховка / ДМС (Клиент + Родственники)
```graphql
query GetClientFamily($clientId: ID!) {
  client(id: $clientId) {
    name
    relatives {
      relationType
      name
      age
    }
  }
}
```

### Сценарий В. Прямой запрос только документов (аналог эндпоинта документов)
```graphql
query GetDocumentsOnly($clientId: ID!) {
  documents(clientId: $clientId) {
    id
    type
    number
  }
}
```

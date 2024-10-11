# Cart Service:
Håndterer brugernes indkøbskurve.
Tilbyder funktioner til at tilføje, fjerne og opdatere varer i kurven.

## Installation

1. Clone dette repository:

```
   git clone https://github.com/DetGrey/cart_service
   cd cart_service
   docker build -t cart_service .
   docker run -it --rm -p 5000:5000 -v ${PWD}:/home/data cart_service
```

## API Endpoints

### See all cart items

- **URL:** `/cart`
- **Method:** `GET`

- **Response:**

  - **200 OK:** Returns cart data
  - **204 No contet:** Cart is empty
  - **500:** Some error happened

### Add new item to cart

- **URL:** `/cart`
- **Method:** `POST`
- **Request Body:** JSON

  ```json
  {
      "product_id": 4321,
      "amount": 1
  }
  ```

- **Response:**

  - **201 Created:** Item added to cart successfully
  - **500:** Some error happened

### Delete item from cart

- **URL:** `/cart/<id>`
- **Method:** `DELETE`

- **Response:**

  - **204 No content:** Item deleted from cart successfully
  - **404 Not Found:** Item not found
  - **500:** Some error happened

*(Bemærk: Dette endpoint opdaterer i øjeblikket ikke nogen data og returnerer et pladsholderrespons.)*

### Update product amount

- **URL:** `/cart/<id>`
- **Method:** `PATCH`
- **Request Body:** JSON

  ```json
  {
      "amount": 2
  }
  ```

- **Response:**

  - **200 OK:** Product amount updated successfully
  - **400:** Specifying amount is required
  - **500:** Some error happened

   
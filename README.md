# 🛒 Shopping-Cart-Assignment

This project is a **web-based e-commerce application** built using **HTML, CSS (Bootstrap) and Python (Flask)**.  
The application allows users to browse products, add them to a shopping cart, and complete an order through a checkout form.

---

##  Key Features Implemented

### 🏠 Front Page / Product Showcase
- Products are dynamically rendered using **Python** and **Jinja2** templates.  
- Each product includes an **“Add to Cart”** button.  
- Individual product pages are available as an extra feature for more detailed views.

### 🛒 Shopping Cart
- View selected products, adjust quantities, remove items, and see total pricing.  
- For the **vacation shop concept**, users can select the desired period for their vacation trips.  

### 💖 Wishlist
- Authenticated users can add products to a **wishlist**, accessible only after login.  

### 📝 Checkout Page
- Fully functional checkout form collecting:
  - `full_name`
  - `email`
  - `phone`
  - `address`
  - `payment_method` (card, bank_transfer, cash)
- Submitted orders are printed in the **server console** and saved in a structured format for record-keeping.

### 📞 Contact Page

A dedicated **Contact Page** allows users to get in touch easily. Features include:

- A responsive form collecting:
  - Full Name
  - Email
  - Message

### 🔐 User Authentication
- Simple login functionality with predefined users:

```python
ALLOWED_USERS = {
    "test": "test123",
    "admin": "n0h4x0rz-plz",
}
```
### 🐳 Containerization

The application is fully **containerized using Docker**, enabling:

- ✅ Easy setup and deployment
- ✅ Consistent environment across machines
- ✅ Execution on **Flask’s default port 5000**

#### How to run:

```bash
# Build the Docker image
docker build -t tema_ia1 .

# Run the container
docker run -p 5000:5000 -it tema_ia1
```

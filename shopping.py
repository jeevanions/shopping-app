import json
import uuid

# Load JSON data from a file
def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Load users, admins, and product catalog data from JSON files
users = load_json('users.json')
product_catalog = load_json('product_catalog.json')

# Dummy data for payment options
payment_options = ['Net Banking', 'PayPal', 'UPI']

class User:
    def __init__(self, username, password, is_admin):
        self.username = username
        self.password = password
        self.session_id = None
        self.cart = []
        self.is_admin = is_admin

    def login(self, password):
        if self.password == password:
            self.session_id = str(uuid.uuid4())
            return self.session_id
        return None

    def logout(self):
        self.session_id = None

    def add_to_cart(self, product_id, quantity):
        for category, products in product_catalog.items():
            for product in products:
                if product['product_id'] == product_id:
                    if product['stock'] == 0:
                        return "Product out of stock"
                    if product['stock'] < quantity:
                        return "Not enough stock available"
                    self.cart.append({'product_id': product_id, 'name': product['name'], 'quantity': quantity, 'price': product['price']})
                    return f"Added {quantity} of {product['name']} to cart"
        return "Product not found"

    def remove_from_cart(self, product_id):
        for item in self.cart:
            if item['product_id'] == product_id:
                self.cart.remove(item)
                return f"Removed {product_id} from cart"
        return "Product not in cart"

    def clear_cart(self):
        self.cart = []
        return "Cart cleared"

    def checkout(self, payment_option):
        if payment_option in payment_options:
            for item in self.cart:
                for category, products in product_catalog.items():
                    for product in products:
                        if product['product_id'] == item['product_id']:
                            product['stock'] -= item['quantity']
            total_amount = sum(item['quantity'] * item['price'] for item in self.cart)
            self.cart = []
            return f"Your order is successfully placed using {payment_option} for a total of Rs. {total_amount}"
        return "Invalid payment option"

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, is_admin=True)

    def add_product(self, category, product_id, name, stock, price):
        if category not in product_catalog:
            product_catalog[category] = []
        product_catalog[category].append({'product_id': product_id, 'name': name, 'stock': stock, 'price': price})
        return f"Product {name} added to {category}"

    def remove_product(self, category, product_id):
        if category in product_catalog:
            for product in product_catalog[category]:
                if product['product_id'] == product_id:
                    product_catalog[category].remove(product)
                    return f"Product {product_id} removed from {category}"
        return "Product not found in category"

    def add_category(self, category):
        if category not in product_catalog:
            product_catalog[category] = []
            return f"Category {category} added"
        return "Category already exists"

    def remove_category(self, category):
        if category in product_catalog:
            del product_catalog[category]
            return f"Category {category} removed"
        return "Category not found"

def load_users():
    user_objects = {}
    for username, data in users.items():
        if data['is_admin']:
            user_objects[username] = Admin(username, data['password'])
        else:
            user_objects[username] = User(username, data['password'], data['is_admin'])
    return user_objects

user_objects = load_users()

def user_menu(user):
    while True:
        print("\nUser Menu:")
        print("1. View Catalog")
        print("2. Add Item to Cart")
        print("3. Remove Item from Cart")
        print("4. Clear Cart")
        print("5. View Cart")
        print("6. Checkout")
        print("7. Exit")

        choice = input("Choose an option: ")
        if choice == '1':
            catalog = product_catalog
            for category, products in catalog.items():
                print(f"\nCategory: {category}")
                for product in products:
                    print(f"Product ID: {product['product_id']}, Name: {product['name']}, Stock: {product['stock']}, Price: {product['price']}")
        elif choice == '2':
            product_id = input("Enter Product ID to add: ")
            quantity = int(input("Enter quantity: "))
            print(user.add_to_cart(product_id, quantity))
        elif choice == '3':
            product_id = input("Enter Product ID to remove: ")
            print(user.remove_from_cart(product_id))
        elif choice == '4':
            print(user.clear_cart())
        elif choice == '5':
            if user.cart:
                for item in user.cart:
                    print(f"Product ID: {item['product_id']}, Name: {item['name']}, Quantity: {item['quantity']}, Price: {item['price']}")
            else:
                print("Your cart is empty")
        elif choice == '6':
            print("Payment options: Net Banking, PayPal, UPI")
            payment_option = input("Choose a payment option: ")
            print(user.checkout(payment_option))
        elif choice == '7':
            user.logout()
            break
        else:
            print("Invalid choice. Please try again.")

def admin_menu(admin):
    while True:
        print("\nAdmin Menu:")
        print("1. View Catalog")
        print("2. Add Product")
        print("3. Remove Product")
        print("4. Add Category")
        print("5. Remove Category")
        print("6. Exit")

        choice = input("Choose an option: ")
        if choice == '1':
            catalog = product_catalog
            for category, products in catalog.items():
                print(f"\nCategory: {category}")
                for product in products:
                    print(f"Product ID: {product['product_id']}, Name: {product['name']}, Stock: {product['stock']}, Price: {product['price']}")
        elif choice == '2':
            category = input("Enter category: ")
            product_id = input("Enter product ID: ")
            name = input("Enter product name: ")
            stock = int(input("Enter product stock: "))
            price = float(input("Enter product price: "))
            print(admin.add_product(category, product_id, name, stock, price))
        elif choice == '3':
            category = input("Enter category: ")
            product_id = input("Enter product ID to remove: ")
            print(admin.remove_product(category, product_id))
        elif choice == '4':
            category = input("Enter new category: ")
            print(admin.add_category(category))
        elif choice == '5':
            category = input("Enter category to remove: ")
            print(admin.remove_category(category))
        elif choice == '6':
            admin.logout()
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    username = input("Enter username: ")
    password = input("Enter password: ")

    user = user_objects.get(username)
    if user and user.login(password):
        print(f"Login successful! Session ID: {user.session_id}")
        if user.is_admin:
            admin_menu(user)
        else:
            user_menu(user)
    else:
        print("Invalid credentials. Please try again.")

if __name__ == "__main__":
    main()

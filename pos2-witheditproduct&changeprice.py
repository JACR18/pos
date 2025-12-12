import os
import json
import uuid
import datetime
import time

# ==========================
# TERMINAL COLORS
# ==========================
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"

# ==========================
# UTILITY FUNCTIONS
# ==========================
def clear():
    os.system("cls" if os.name=="nt" else "clear")

def header(text):
    print(CYAN + "╔" + "═"*60 + "╗")
    print(f"        {text.upper():^60}")
    print("╚" + "═"*60 + "╝" + RESET)

def success(msg):
    print(f"{GREEN}✔ {msg}{RESET}")

def error(msg):
    print(f"{RED}✘ {msg}{RESET}")

def option(num, text):
    print(f"{YELLOW}{num}.{WHITE} {text}{RESET}")

# ==========================
# DATA
# ==========================
users = {
    "admin": "1234",
    "cashier": "1234"
}

products = [
    {"name": "ID Lace", "price": 75},
    {"name": "Logo", "price": 50},
    {"name": "Cartolina", "price": 20},
    {"name": "Bond Paper", "price": 1}
]

def load_transactions():
    data = []
    if not os.path.exists("transactions.json"):
        open("transactions.json","w").close()
    with open("transactions.json", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data

def save_transaction(cart, total, method, cash, change):
    receipt_id = str(uuid.uuid4())
    trans = {
        "receipt_id": receipt_id,
        "datetime": str(datetime.datetime.now()),
        "items": cart,
        "total": total,
        "method": method,
        "cash": cash,
        "change": change
    }
    with open("transactions.json", "a") as f:
        f.write(json.dumps(trans)+"\n")
    success(f"Transaction saved! Receipt ID: {receipt_id}")

def save_all_transactions(data):
    with open("transactions.json", "w") as f:
        for entry in data:
            f.write(json.dumps(entry) + "\n")

# ==========================
# NEW FUNCTION: EDIT PRODUCT
# ==========================
def edit_product():
    while True:
        clear()
        header("Edit Product & Price")

        print("Products:")
        for idx, p in enumerate(products, start=1):
            print(f"{idx}. {p['name']} - ₱{p['price']}")

        print("\nB. Back")
        choice = input("\nSelect product number: ").lower()

        if choice == "b":
            break

        if not choice.isdigit() or not (1 <= int(choice) <= len(products)):
            error("Invalid product number!")
            time.sleep(1)
            continue

        selected = products[int(choice)-1]

        print(f"\nSelected: {selected['name']} - ₱{selected['price']}")
        print("1. Change Name")
        print("2. Change Price")
        print("3. Back")
        sub = input("Choose: ")

        # Change Name
        if sub == "1":
            new_name = input("Enter new name: ").strip()
            if new_name == "":
                error("Name cannot be empty!")
                time.sleep(1)
                continue
            selected["name"] = new_name
            success("Product name updated!")
            time.sleep(1)

        # Change Price
        elif sub == "2":
            new_price = input("Enter new price: ")
            if not new_price.isdigit():
                error("Invalid price!")
                time.sleep(1)
                continue
            selected["price"] = int(new_price)
            success("Product price updated!")
            time.sleep(1)

        elif sub == "3":
            continue
        else:
            error("Invalid option!")
            time.sleep(1)

# ==========================
# LOGIN
# ==========================
def login():
    clear()
    header("Login Page")
    print(f"{YELLOW}Hint: admin/1234 or cashier/1234{RESET}\n")
    user = input("Username: ").lower()
    password = input("Password: ")
    if user in users and password == users[user]:
        success("Login successful!")
        time.sleep(1)
        return user
    else:
        error("Invalid username/password")
        input("Press Enter to try again...")
        return None

# ==========================
# ADMIN DASHBOARD
# ==========================
def admin_dashboard():
    while True:
        clear()
        header("Admin Dashboard")
        print("Options:")
        option(1, "View Transaction History")
        option(2, "Logout")
        option(3, "Edit Product & Price")   # <== ADDED HERE

        choice = input("\nChoose option: ").lower()
        if choice == "1":
            # Show list
            transactions = load_transactions()
            clear()
            header("Transaction List")
            if not transactions:
                print(YELLOW + "No transactions found." + RESET)
                input("Press Enter to return...")
                continue

            for idx, t in enumerate(transactions, start=1):
                print(f"{idx}. {t['receipt_id']} - {t['datetime']}")

            sel = input("\nSelect transaction number: ")
            if not sel.isdigit() or not (1 <= int(sel) <= len(transactions)):
                error("Invalid selection!")
                time.sleep(1)
                continue

            selected = transactions[int(sel) - 1]

            # Display details
            while True:
                clear()
                header("Transaction Details")
                print(f"Receipt ID: {selected['receipt_id']}")
                print(f"Date: {selected['datetime']}")
                print("Items:")
                for item in selected["items"]:
                    print(f" - {item['name']} x{item['qty']} = ₱{item['total']}")
                print(f"Total: ₱{selected['total']}")
                print(f"Payment: {selected['method']}")
                print(f"Cash: ₱{selected['cash']}  Change: ₱{selected['change']}\n")

                print("1. Delete this transaction")
                print("2. Back")
                sub = input("Choose: ")

                if sub == "1":
                    confirm = input("Are you sure? (y/n): ").lower()
                    if confirm == "y":
                        transactions.remove(selected)
                        save_all_transactions(transactions)
                        success("Transaction deleted!")
                        time.sleep(1)
                        break
                elif sub == "2":
                    break
                else:
                    error("Invalid input!")
                    time.sleep(1)

        elif choice == "2":
            break

        elif choice == "3":
            edit_product()   # <<< CALL ADDED FUNCTION

        else:
            error("Invalid input!")
            time.sleep(1)

# ==========================
# CASHIER DASHBOARD
# ==========================
def cashier_dashboard():
    cart = []
    total = 0

    while True:
        clear()
        header("Cashier Dashboard")
        print("Options:")
        option(1, "Add Item to Cart")
        option(2, "Checkout")
        option(3, "Logout")

        print("\n" + CYAN + "=== Products ===" + RESET)
        for idx, p in enumerate(products, start=1):
            print(f"{idx}. {p['name']} - ₱{p['price']}")

        print("\n" + MAGENTA + "=== Cart ===" + RESET)
        if cart:
            for i in cart:
                print(f"{i['name']} x{i['qty']} = ₱{i['total']}")
            print(f"Total: ₱{total}")
        else:
            print(YELLOW + "Cart is empty." + RESET)

        choice = input("\nChoose option: ").lower()

        if choice == "1":
            while True:
                clear()
                header("Cashier Dashboard")
                print("Options:")
                option(1, "Add Item to Cart")
                option(2, "Checkout")
                option(3, "Logout")

                print("\n=== Products ===")
                for idx, p in enumerate(products, start=1):
                    print(f"{idx}. {p['name']} - ₱{p['price']}")

                print("\n=== Cart ===")
                if cart:
                    for i in cart:
                        print(f"{i['name']} x{i['qty']} = ₱{i['total']}")
                    print(f"Total: ₱{total}")
                else:
                    print("Cart is empty.")

                product_num = input("\nSelect product number or B to go back: ").lower()
                if product_num == "b":
                    break
                if product_num.isdigit() and 1 <= int(product_num) <= len(products):
                    product = products[int(product_num)-1]
                    qty = input(f"Quantity for {product['name']}: ")
                    if qty.isdigit() and int(qty)>0:
                        qty = int(qty)
                        cost = qty*product['price']
                        cart.append({"name":product['name'], "qty":qty, "price":product['price'], "total":cost})
                        total += cost
                        success(f"Added {qty} x {product['name']} = ₱{cost}")
                        time.sleep(0.5)
                    else:
                        error("Invalid quantity!")
                else:
                    error("Invalid product number!")

        elif choice == "2":
            if not cart:
                error("Cart is empty!")
                time.sleep(0.5)
                continue

            method = input("Payment method (cash/card): ").lower()
            if method not in ["cash","card"]:
                error("Invalid method!")
                time.sleep(0.5)
                continue

            if method=="cash":
                cash = input("Enter cash amount: ")
                if not cash.isdigit() or int(cash)<total:
                    error("Insufficient cash!")
                    time.sleep(0.5)
                    continue
                cash = int(cash)
                change = cash-total
            else:
                cash = total
                change = 0

            save_transaction(cart, total, method, cash, change)
            cart.clear()
            total = 0
            time.sleep(1)

        elif choice == "3":
            break
        else:
            error("Invalid input!")

# ==========================
# MAIN LOOP
# ==========================
while True:
    user = login()
    if user=="admin":
        admin_dashboard()
    elif user=="cashier":
        cashier_dashboard()

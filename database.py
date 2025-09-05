# # import sqlite3
# # from datetime import datetime

# # class Database:
# #     def __init__(self):
# #         try:
# #             self.conn = sqlite3.connect("restaurant.db", check_same_thread=False)
# #             self.cursor = self.conn.cursor()
# #             self.create_tables()
# #         except sqlite3.Error as e:
# #             print(f"Database connection error: {e}")
# #             raise

# #     def create_tables(self):
# #         try:
# #             # Create menu table
# #             self.cursor.execute('''
# #                 CREATE TABLE IF NOT EXISTS menu (
# #                     id INTEGER PRIMARY KEY AUTOINCREMENT,
# #                     name TEXT NOT NULL UNIQUE,
# #                     price REAL NOT NULL
# #                 )
# #             ''')
# #             # Create orders table with waiter
# #             self.cursor.execute('''
# #                 CREATE TABLE IF NOT EXISTS orders (
# #                     order_id TEXT PRIMARY KEY,
# #                     order_type TEXT NOT NULL,
# #                     order_date TEXT NOT NULL,
# #                     waiter TEXT NOT NULL
# #                 )
# #             ''')
# #             # Create order_items table
# #             self.cursor.execute('''
# #                 CREATE TABLE IF NOT EXISTS order_items (
# #                     id INTEGER PRIMARY KEY AUTOINCREMENT,
# #                     order_id TEXT NOT NULL,
# #                     item_name TEXT NOT NULL,
# #                     quantity INTEGER NOT NULL,
# #                     price REAL NOT NULL,
# #                     total REAL NOT NULL,
# #                     FOREIGN KEY (order_id) REFERENCES orders(order_id)
# #                 )
# #             ''')
# #             # Create expenses table
# #             self.cursor.execute('''
# #                 CREATE TABLE IF NOT EXISTS expenses (
# #                     expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
# #                     category TEXT NOT NULL,
# #                     amount REAL NOT NULL,
# #                     date TEXT NOT NULL
# #                 )
# #             ''')
# #             self.conn.commit()
# #             print("Tables created successfully")
# #         except sqlite3.Error as e:
# #             print(f"Error creating tables: {e}")
# #             raise

# #     def initialize_menu(self, menu_items):
# #         try:
# #             self.cursor.executemany('''
# #                 INSERT OR REPLACE INTO menu (name, price)
# #                 VALUES (?, ?)
# #             ''', [(item["name"], item["price"]) for item in menu_items])
# #             self.conn.commit()
# #             print(f"Initialized menu with {len(menu_items)} items")
# #         except sqlite3.Error as e:
# #             print(f"Error initializing menu: {e}")
# #             raise

# #     def get_menu(self):
# #         try:
# #             self.cursor.execute("SELECT name, price FROM menu")
# #             return [{"name": row[0], "price": row[1]} for row in self.cursor.fetchall()]
# #         except sqlite3.Error as e:
# #             print(f"Error retrieving menu: {e}")
# #             return []

# #     def edit_product(self, old_name, new_name, price):
# #         try:
# #             self.cursor.execute('''
# #                 UPDATE menu
# #                 SET name = ?, price = ?
# #                 WHERE name = ?
# #             ''', (new_name, price, old_name))
# #             self.conn.commit()
# #             print(f"Edited product: {old_name} -> {new_name}, Price={price}")
# #         except sqlite3.Error as e:
# #             print(f"Error editing product {old_name}: {e}")
# #             raise

# #     def delete_product(self, name):
# #         try:
# #             self.cursor.execute("DELETE FROM menu WHERE name = ?", (name,))
# #             self.conn.commit()
# #             print(f"Deleted product: {name}")
# #         except sqlite3.Error as e:
# #             print(f"Error deleting product {name}: {e}")
# #             raise

# #     def add_order(self, order_id, order_type, items, order_date, waiter):
# #         try:
# #             # Insert order metadata with waiter
# #             self.cursor.execute('''
# #                 INSERT INTO orders (order_id, order_type, order_date, waiter)
# #                 VALUES (?, ?, ?, ?)
# #             ''', (order_id, order_type, order_date, waiter))
# #             # Insert items
# #             for item in items:
# #                 self.cursor.execute('''
# #                     INSERT INTO order_items (order_id, item_name, quantity, price, total)
# #                     VALUES (?, ?, ?, ?, ?)
# #                 ''', (order_id, item["name"], item["quantity"], item["price"], item["total"]))
# #             self.conn.commit()
# #             print(f"DB: Saved order {order_id}, Type={order_type}, Items={items}, Date={order_date}, Waiter={waiter}")
# #         except sqlite3.Error as e:
# #             print(f"Error saving order {order_id}: {e}")
# #             self.conn.rollback()
# #             raise

# #     def get_orders_by_date(self, date):
# #         try:
# #             self.cursor.execute('''
# #                 SELECT o.order_id, o.order_type, o.order_date, o.waiter, SUM(oi.total) as total
# #                 FROM orders o
# #                 JOIN order_items oi ON o.order_id = oi.order_id
# #                 WHERE o.order_date LIKE ?
# #                 GROUP BY o.order_id, o.order_type, o.order_date, o.waiter
# #             ''', (f"{date}%",))
# #             return [{"order_id": row[0], "order_type": row[1], "order_date": row[2], "waiter": row[3], "total": row[4]} for row in self.cursor.fetchall()]
# #         except sqlite3.Error as e:
# #             print(f"Error retrieving orders for {date}: {e}")
# #             return []

# #     def get_order_items(self, order_id):
# #         try:
# #             self.cursor.execute('''
# #                 SELECT item_name, quantity, price, total
# #                 FROM order_items
# #                 WHERE order_id = ?
# #             ''', (order_id,))
# #             return [{"item_name": row[0], "quantity": row[1], "price": row[2], "total": row[3]} for row in self.cursor.fetchall()]
# #         except sqlite3.Error as e:
# #             print(f"Error retrieving items for order {order_id}: {e}")
# #             return []

# #     def add_expense(self, category, amount, date):
# #         try:
# #             self.cursor.execute('''
# #                 INSERT INTO expenses (category, amount, date)
# #                 VALUES (?, ?, ?)
# #             ''', (category, amount, date))
# #             self.conn.commit()
# #             print(f"Added expense: {category}, {amount}, {date}")
# #         except sqlite3.Error as e:
# #             print(f"Error adding expense: {e}")

# #     def get_expenses_today(self):
# #         try:
# #             today = datetime.now().strftime("%Y-%m-%d")
# #             self.cursor.execute("SELECT category, amount FROM expenses WHERE date = ?", (today,))
# #             return self.cursor.fetchall()
# #         except sqlite3.Error as e:
# #             print(f"Error retrieving today's expenses: {e}")
# #             return []

# #     def get_expenses_by_date(self, date):
# #         try:
# #             self.cursor.execute("SELECT category, amount FROM expenses WHERE date = ?", (date,))
# #             return self.cursor.fetchall()
# #         except sqlite3.Error as e:
# #             print(f"Error retrieving expenses for {date}: {e}")
# #             return []

# #     def __del__(self):
# #         try:
# #             self.conn.close()
# #             print("Database connection closed")
# #         except sqlite3.Error as e:
# #             print(f"Error closing database: {e}")

# # if __name__ == "__main__":
# #     db = Database()
# #     db.initialize_menu([
# #         {"name": "Burger", "price": 5.99},
# #         {"name": "Pizza", "price": 8.99},
# #     ])
# #     db.__del__()

# # import sqlite3
# # from datetime import datetime

# # class Database:
# #     def __init__(self):
# #         try:
# #             self.conn = sqlite3.connect("restaurant.db", check_same_thread=False)
# #             self.cursor = self.conn.cursor()
# #             self.create_tables()
# #             print("Database initialized")
# #         except sqlite3.Error as e:
# #             print(f"Database connection error: {e}")
# #             raise

# #     def create_tables(self):
# #         try:
# #             # Create product table (replacing menu)
# #             self.cursor.execute('''
# #                 CREATE TABLE IF NOT EXISTS product (
# #                     id INTEGER PRIMARY KEY AUTOINCREMENT,
# #                     name TEXT NOT NULL UNIQUE,
# #                     price REAL NOT NULL
# #                 )
# #             ''')
# #             # Create orders table with waiter
# #             self.cursor.execute('''
# #                 CREATE TABLE IF NOT EXISTS orders (
# #                     order_id TEXT PRIMARY KEY,
# #                     order_type TEXT NOT NULL,
# #                     order_date TEXT NOT NULL,
# #                     waiter TEXT NOT NULL
# #                 )
# #             ''')
# #             # Create order_items table
# #             self.cursor.execute('''
# #                 CREATE TABLE IF NOT EXISTS order_items (
# #                     id INTEGER PRIMARY KEY AUTOINCREMENT,
# #                     order_id TEXT NOT NULL,
# #                     item_name TEXT NOT NULL,
# #                     quantity INTEGER NOT NULL,
# #                     price REAL NOT NULL,
# #                     total REAL NOT NULL,
# #                     FOREIGN KEY (order_id) REFERENCES orders(order_id)
# #                 )
# #             ''')
# #             # Create expenses table
# #             self.cursor.execute('''
# #                 CREATE TABLE IF NOT EXISTS expenses (
# #                     expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
# #                     category TEXT NOT NULL,
# #                     amount REAL NOT NULL,
# #                     date TEXT NOT NULL
# #                 )
# #             ''')
# #             self.conn.commit()
# #             print("Tables created successfully")
# #         except sqlite3.Error as e:
# #             print(f"Error creating tables: {e}")
# #             raise

# #     def initialize_menu(self, menu_items):
# #         try:
# #             self.cursor.executemany('''
# #                 INSERT OR REPLACE INTO product (name, price)
# #                 VALUES (?, ?)
# #             ''', [(item["name"], item["price"]) for item in menu_items])
# #             self.conn.commit()
# #             print(f"Initialized product table with {len(menu_items)} items")
# #         except sqlite3.Error as e:
# #             print(f"Error initializing product table: {e}")
# #             raise

# #     def get_menu(self):
# #         try:
# #             self.cursor.execute("SELECT name, price FROM product")
# #             result = [{"name": row[0], "price": row[1]} for row in self.cursor.fetchall()]
# #             print(f"Retrieved product table: {result}")
# #             return result
# #         except sqlite3.Error as e:
# #             print(f"Error retrieving product table: {e}")
# #             return []

# #     def edit_product(self, old_name, new_name, price):
# #         try:
# #             print(f"Executing edit_product: old_name={old_name}, new_name={new_name}, price={price}")
# #             # Update product table
# #             self.cursor.execute('''
# #                 UPDATE product
# #                 SET name = ?, price = ?
# #                 WHERE name = ?
# #             ''', (new_name, price, old_name))
# #             if self.cursor.rowcount == 0:
# #                 print(f"No product found with name: {old_name}")
# #                 raise ValueError(f"No product found with name: {old_name}")
# #             # Update order_items if name changed
# #             if old_name != new_name:
# #                 self.cursor.execute('''
# #                     UPDATE order_items
# #                     SET item_name = ?
# #                     WHERE item_name = ?
# #                 ''', (new_name, old_name))
# #                 print(f"Updated {self.cursor.rowcount} order_items from {old_name} to {new_name}")
# #             self.conn.commit()
# #             print(f"Edited product: {old_name} -> {new_name}, Price={price}")
# #         except sqlite3.Error as e:
# #             print(f"Error editing product {old_name}: {e}")
# #             self.conn.rollback()
# #             raise

# #     def delete_product(self, name):
# #         try:
# #             print(f"Executing delete_product: name={name}")
# #             self.cursor.execute("DELETE FROM product WHERE name = ?", (name,))
# #             if self.cursor.rowcount == 0:
# #                 print(f"No product found with name: {name}")
# #                 raise ValueError(f"No product found with name: {name}")
# #             self.conn.commit()
# #             print(f"Deleted product: {name}")
# #         except sqlite3.Error as e:
# #             print(f"Error deleting product {name}: {e}")
# #             self.conn.rollback()
# #             raise

# #     def add_order(self, order_id, order_type, items, order_date, waiter):
# #         try:
# #             # Insert order metadata with waiter
# #             self.cursor.execute('''
# #                 INSERT INTO orders (order_id, order_type, order_date, waiter)
# #                 VALUES (?, ?, ?, ?)
# #             ''', (order_id, order_type, order_date, waiter))
# #             # Insert items
# #             for item in items:
# #                 self.cursor.execute('''
# #                     INSERT INTO order_items (order_id, item_name, quantity, price, total)
# #                     VALUES (?, ?, ?, ?, ?)
# #                 ''', (order_id, item["name"], item["quantity"], item["price"], item["total"]))
# #             self.conn.commit()
# #             print(f"DB: Saved order {order_id}, Type={order_type}, Items={items}, Date={order_date}, Waiter={waiter}")
# #         except sqlite3.Error as e:
# #             print(f"Error saving order {order_id}: {e}")
# #             self.conn.rollback()
# #             raise

# #     def get_orders_by_date(self, date):
# #         try:
# #             self.cursor.execute('''
# #                 SELECT o.order_id, o.order_type, o.order_date, o.waiter, SUM(oi.total) as total
# #                 FROM orders o
# #                 JOIN order_items oi ON o.order_id = oi.order_id
# #                 WHERE o.order_date LIKE ?
# #                 GROUP BY o.order_id, o.order_type, o.order_date, o.waiter
# #             ''', (f"{date}%",))
# #             return [{"order_id": row[0], "order_type": row[1], "order_date": row[2], "waiter": row[3], "total": row[4]} for row in self.cursor.fetchall()]
# #         except sqlite3.Error as e:
# #             print(f"Error retrieving orders for {date}: {e}")
# #             return []

# #     def get_order_items(self, order_id):
# #         try:
# #             self.cursor.execute('''
# #                 SELECT item_name, quantity, price, total
# #                 FROM order_items
# #                 WHERE order_id = ?
# #             ''', (order_id,))
# #             return [{"item_name": row[0], "quantity": row[1], "price": row[2], "total": row[3]} for row in self.cursor.fetchall()]
# #         except sqlite3.Error as e:
# #             print(f"Error retrieving items for order {order_id}: {e}")
# #             return []

# #     def add_expense(self, category, amount, date):
# #         try:
# #             self.cursor.execute('''
# #                 INSERT INTO expenses (category, amount, date)
# #                 VALUES (?, ?, ?)
# #             ''', (category, amount, date))
# #             self.conn.commit()
# #             print(f"Added expense: {category}, {amount}, {date}")
# #         except sqlite3.Error as e:
# #             print(f"Error adding expense: {e}")
# #             self.conn.rollback()
# #             raise

# #     def get_expenses_today(self):
# #         try:
# #             today = datetime.now().strftime("%Y-%m-%d")
# #             self.cursor.execute("SELECT category, amount FROM expenses WHERE date = ?", (today,))
# #             return self.cursor.fetchall()
# #         except sqlite3.Error as e:
# #             print(f"Error retrieving today's expenses: {e}")
# #             return []

# #     def get_expenses_by_date(self, date):
# #         try:
# #             self.cursor.execute("SELECT category, amount FROM expenses WHERE date = ?", (date,))
# #             return self.cursor.fetchall()
# #         except sqlite3.Error as e:
# #             print(f"Error retrieving expenses for {date}: {e}")
# #             return []

# #     def __del__(self):
# #         try:
# #             self.conn.close()
# #             print("Database connection closed")
# #         except sqlite3.Error as e:
# #             print(f"Error closing database: {e}")



# # import sqlite3
# # from datetime import datetime

# # class Database:
# #     def __init__(self):
# #         try:
# #             self.conn = sqlite3.connect("restaurant.db", check_same_thread=False)
# #             self.cursor = self.conn.cursor()
# #             self.create_tables()
# #             print("Database initialized")
# #         except sqlite3.Error as e:
# #             print(f"Database connection error: {e}")
# #             raise

# #     def create_tables(self):
# #         try:
# #             # Create product table with category
# #             self.cursor.execute('''
# #                 CREATE TABLE IF NOT EXISTS product (
# #                     id INTEGER PRIMARY KEY AUTOINCREMENT,
# #                     name TEXT NOT NULL UNIQUE,
# #                     price REAL NOT NULL,
# #                     category TEXT NOT NULL DEFAULT 'Uncategorized'
# #                 )
# #             ''')
# #             # Create orders table with waiter
# #             self.cursor.execute('''
# #                 CREATE TABLE IF NOT EXISTS orders (
# #                     order_id TEXT PRIMARY KEY,
# #                     order_type TEXT NOT NULL,
# #                     order_date TEXT NOT NULL,
# #                     waiter TEXT NOT NULL
# #                 )
# #             ''')
# #             # Create order_items table
# #             self.cursor.execute('''
# #                 CREATE TABLE IF NOT EXISTS order_items (
# #                     id INTEGER PRIMARY KEY AUTOINCREMENT,
# #                     order_id TEXT NOT NULL,
# #                     item_name TEXT NOT NULL,
# #                     quantity INTEGER NOT NULL,
# #                     price REAL NOT NULL,
# #                     total REAL NOT NULL,
# #                     FOREIGN KEY (order_id) REFERENCES orders(order_id)
# #                 )
# #             ''')
# #             # Create expenses table
# #             self.cursor.execute('''
# #                 CREATE TABLE IF NOT EXISTS expenses (
# #                     expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
# #                     category TEXT NOT NULL,
# #                     amount REAL NOT NULL,
# #                     date TEXT NOT NULL
# #                 )
# #             ''')
# #             self.conn.commit()
# #             print("Tables created successfully")
# #         except sqlite3.Error as e:
# #             print(f"Error creating tables: {e}")
# #             raise

# #     def initialize_menu(self, menu_items):
# #         try:
# #             self.cursor.executemany('''
# #                 INSERT OR REPLACE INTO product (name, price, category)
# #                 VALUES (?, ?, ?)
# #             ''', [(item["name"], item["price"], item.get("category", "Uncategorized")) for item in menu_items])
# #             self.conn.commit()
# #             print(f"Initialized product table with {len(menu_items)} items")
# #         except sqlite3.Error as e:
# #             print(f"Error initializing product table: {e}")
# #             raise

# #     def get_menu(self):
# #         try:
# #             self.cursor.execute("SELECT name, price, category FROM product")
# #             result = [{"name": row[0], "price": row[1], "category": row[2]} for row in self.cursor.fetchall()]
# #             print(f"Retrieved product table: {result}")
# #             return result
# #         except sqlite3.Error as e:
# #             print(f"Error retrieving product table: {e}")
# #             return []

# #     def edit_product(self, old_name, new_name, price, category="Uncategorized"):
# #         try:
# #             print(f"Executing edit_product: old_name={old_name}, new_name={new_name}, price={price}, category={category}")
# #             # Update product table
# #             self.cursor.execute('''
# #                 UPDATE product
# #                 SET name = ?, price = ?, category = ?
# #                 WHERE name = ?
# #             ''', (new_name, price, category, old_name))
# #             if self.cursor.rowcount == 0:
# #                 print(f"No product found with name: {old_name}")
# #                 raise ValueError(f"No product found with name: {old_name}")
# #             # Update order_items if name changed
# #             if old_name != new_name:
# #                 self.cursor.execute('''
# #                     UPDATE order_items
# #                     SET item_name = ?
# #                     WHERE item_name = ?
# #                 ''', (new_name, old_name))
# #                 print(f"Updated {self.cursor.rowcount} order_items from {old_name} to {new_name}")
# #             self.conn.commit()
# #             print(f"Edited product: {old_name} -> {new_name}, Price={price}, Category={category}")
# #         except sqlite3.Error as e:
# #             print(f"Error editing product {old_name}: {e}")
# #             self.conn.rollback()
# #             raise

# #     def delete_product(self, name):
# #         try:
# #             print(f"Executing delete_product: name={name}")
# #             self.cursor.execute("DELETE FROM product WHERE name = ?", (name,))
# #             if self.cursor.rowcount == 0:
# #                 print(f"No product found with name: {name}")
# #                 raise ValueError(f"No product found with name: {name}")
# #             self.conn.commit()
# #             print(f"Deleted product: {name}")
# #         except sqlite3.Error as e:
# #             print(f"Error deleting product {name}: {e}")
# #             self.conn.rollback()
# #             raise

# #     def add_order(self, order_id, order_type, items, order_date, waiter):
# #         try:
# #             # Insert order metadata with waiter
# #             self.cursor.execute('''
# #                 INSERT INTO orders (order_id, order_type, order_date, waiter)
# #                 VALUES (?, ?, ?, ?)
# #             ''', (order_id, order_type, order_date, waiter))
# #             # Insert items
# #             for item in items:
# #                 self.cursor.execute('''
# #                     INSERT INTO order_items (order_id, item_name, quantity, price, total)
# #                     VALUES (?, ?, ?, ?, ?)
# #                 ''', (order_id, item["name"], item["quantity"], item["price"], item["total"]))
# #             self.conn.commit()
# #             print(f"DB: Saved order {order_id}, Type={order_type}, Items={items}, Date={order_date}, Waiter={waiter}")
# #         except sqlite3.Error as e:
# #             print(f"Error saving order {order_id}: {e}")
# #             self.conn.rollback()
# #             raise

# #     def get_orders_by_date(self, date):
# #         try:
# #             self.cursor.execute('''
# #                 SELECT o.order_id, o.order_type, o.order_date, o.waiter, SUM(oi.total) as total
# #                 FROM orders o
# #                 JOIN order_items oi ON o.order_id = oi.order_id
# #                 WHERE o.order_date LIKE ?
# #                 GROUP BY o.order_id, o.order_type, o.order_date, o.waiter
# #             ''', (f"{date}%",))
# #             return [{"order_id": row[0], "order_type": row[1], "order_date": row[2], "waiter": row[3], "total": row[4]} for row in self.cursor.fetchall()]
# #         except sqlite3.Error as e:
# #             print(f"Error retrieving orders for {date}: {e}")
# #             return []

# #     def get_order_items(self, order_id):
# #         try:
# #             self.cursor.execute('''
# #                 SELECT item_name, quantity, price, total
# #                 FROM order_items
# #                 WHERE order_id = ?
# #             ''', (order_id,))
# #             return [{"item_name": row[0], "quantity": row[1], "price": row[2], "total": row[3]} for row in self.cursor.fetchall()]
# #         except sqlite3.Error as e:
# #             print(f"Error retrieving items for order {order_id}: {e}")
# #             return []

# #     def add_expense(self, category, amount, date):
# #         try:
# #             self.cursor.execute('''
# #                 INSERT INTO expenses (category, amount, date)
# #                 VALUES (?, ?, ?)
# #             ''', (category, amount, date))
# #             self.conn.commit()
# #             print(f"Added expense: {category}, {amount}, {date}")
# #         except sqlite3.Error as e:
# #             print(f"Error adding expense: {e}")
# #             self.conn.rollback()
# #             raise

# #     def get_expenses_today(self):
# #         try:
# #             today = datetime.now().strftime("%Y-%m-%d")
# #             self.cursor.execute("SELECT category, amount FROM expenses WHERE date = ?", (today,))
# #             return self.cursor.fetchall()
# #         except sqlite3.Error as e:
# #             print(f"Error retrieving today's expenses: {e}")
# #             return []

# #     def get_expenses_by_date(self, date):
# #         try:
# #             self.cursor.execute("SELECT category, amount FROM expenses WHERE date = ?", (date,))
# #             return self.cursor.fetchall()
# #         except sqlite3.Error as e:
# #             print(f"Error retrieving expenses for {date}: {e}")
# #             return []

# #     def __del__(self):
# #         try:
# #             self.conn.close()
# #             print("Database connection closed")
# #         except sqlite3.Error as e:
# #             print(f"Error closing database: {e}")




# import sqlite3
# from datetime import datetime

# class Database:
#     def __init__(self):
#         try:
#             self.conn = sqlite3.connect("restaurant.db", check_same_thread=False)
#             self.cursor = self.conn.cursor()
#             self.create_tables()
#             print("Database initialized")
#         except sqlite3.Error as e:
#             print(f"Database connection error: {e}")
#             raise

#     def create_tables(self):
#         try:
#             self.cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS product (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     name TEXT NOT NULL UNIQUE,
#                     price REAL NOT NULL,
#                     category TEXT NOT NULL DEFAULT 'Uncategorized'
#                 )
#             ''')
#             self.cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS orders (
#                     order_id TEXT PRIMARY KEY,
#                     order_type TEXT NOT NULL,
#                     order_date TEXT NOT NULL,
#                     waiter TEXT NOT NULL
#                 )
#             ''')
#             self.cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS order_items (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     order_id TEXT NOT NULL,
#                     item_name TEXT NOT NULL,
#                     quantity INTEGER NOT NULL,
#                     price REAL NOT NULL,
#                     total REAL NOT NULL,
#                     FOREIGN KEY (order_id) REFERENCES orders(order_id)
#                 )
#             ''')
#             self.cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS expenses (
#                     expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     category TEXT NOT NULL,
#                     amount REAL NOT NULL,
#                     date TEXT NOT NULL
#                 )
#             ''')
#             self.conn.commit()
#             print("Tables created successfully")
#         except sqlite3.Error as e:
#             print(f"Error creating tables: {e}")
#             raise

#     def initialize_menu(self, menu_items):
#         try:
#             self.cursor.executemany('''
#                 INSERT OR REPLACE INTO product (name, price, category)
#                 VALUES (?, ?, ?)
#             ''', [(item["name"], item["price"], item.get("category", "Uncategorized")) for item in menu_items])
#             self.conn.commit()
#             print(f"Initialized product table with {len(menu_items)} items")
#         except sqlite3.Error as e:
#             print(f"Error initializing product table: {e}")
#             raise

#     def get_menu(self):
#         try:
#             self.cursor.execute("SELECT name, price, category FROM product")
#             result = [{"name": row[0], "price": row[1], "category": row[2]} for row in self.cursor.fetchall()]
#             print(f"Retrieved product table: {result}")
#             return result
#         except sqlite3.Error as e:
#             print(f"Error retrieving product table: {e}")
#             return []

#     def edit_product(self, old_name, new_name, price, category="Uncategorized"):
#         try:
#             print(f"Executing edit_product: old_name={old_name}, new_name={new_name}, price={price}, category={category}")
#             self.cursor.execute('''
#                 UPDATE product
#                 SET name = ?, price = ?, category = ?
#                 WHERE name = ?
#             ''', (new_name, price, category, old_name))
#             if self.cursor.rowcount == 0:
#                 print(f"No product found with name: {old_name}")
#                 raise ValueError(f"No product found with name: {old_name}")
#             if old_name != new_name:
#                 self.cursor.execute('''
#                     UPDATE order_items
#                     SET item_name = ?
#                     WHERE item_name = ?
#                 ''', (new_name, old_name))
#                 print(f"Updated {self.cursor.rowcount} order_items from {old_name} to {new_name}")
#             self.conn.commit()
#             print(f"Edited product: {old_name} -> {new_name}, Price={price}, Category={category}")
#         except sqlite3.Error as e:
#             print(f"Error editing product {old_name}: {e}")
#             self.conn.rollback()
#             raise

#     def delete_product(self, name):
#         try:
#             print(f"Executing delete_product: name={name}")
#             self.cursor.execute("DELETE FROM product WHERE name = ?", (name,))
#             if self.cursor.rowcount == 0:
#                 print(f"No product found with name: {name}")
#                 raise ValueError(f"No product found with name: {name}")
#             self.conn.commit()
#             print(f"Deleted product: {name}")
#         except sqlite3.Error as e:
#             print(f"Error deleting product {name}: {e}")
#             self.conn.rollback()
#             raise

#     def add_order(self, order_id, order_type, items, order_date, waiter):
#         try:
#             self.cursor.execute('''
#                 INSERT INTO orders (order_id, order_type, order_date, waiter)
#                 VALUES (?, ?, ?, ?)
#             ''', (order_id, order_type, order_date, waiter))
#             for item in items:
#                 self.cursor.execute('''
#                     INSERT INTO order_items (order_id, item_name, quantity, price, total)
#                     VALUES (?, ?, ?, ?, ?)
#                 ''', (order_id, item["name"], item["quantity"], item["price"], item["total"]))
#             self.conn.commit()
#             print(f"DB: Saved order {order_id}, Type={order_type}, Items={items}, Date={order_date}, Waiter={waiter}")
#         except sqlite3.Error as e:
#             print(f"Error saving order {order_id}: {e}")
#             self.conn.rollback()
#             raise

#     def get_orders_by_date(self, date):
#         try:
#             self.cursor.execute('''
#                 SELECT o.order_id, o.order_type, o.order_date, o.waiter, SUM(oi.total) as total
#                 FROM orders o
#                 JOIN order_items oi ON o.order_id = oi.order_id
#                 WHERE o.order_date LIKE ?
#                 GROUP BY o.order_id, o.order_type, o.order_date, o.waiter
#             ''', (f"{date}%",))
#             return [{"order_id": row[0], "order_type": row[1], "order_date": row[2], "waiter": row[3], "total": row[4]} for row in self.cursor.fetchall()]
#         except sqlite3.Error as e:
#             print(f"Error retrieving orders for {date}: {e}")
#             return []

#     def get_order_items(self, order_id):
#         try:
#             self.cursor.execute('''
#                 SELECT item_name, quantity, price, total
#                 FROM order_items
#                 WHERE order_id = ?
#             ''', (order_id,))
#             return [{"item_name": row[0], "quantity": row[1], "price": row[2], "total": row[3]} for row in self.cursor.fetchall()]
#         except sqlite3.Error as e:
#             print(f"Error retrieving items for order {order_id}: {e}")
#             return []

#     def add_expense(self, category, amount, date):
#         try:
#             self.cursor.execute('''
#                 INSERT INTO expenses (category, amount, date)
#                 VALUES (?, ?, ?)
#             ''', (category, amount, date))
#             self.conn.commit()
#             print(f"Added expense: {category}, {amount}, {date}")
#         except sqlite3.Error as e:
#             print(f"Error adding expense: {e}")
#             self.conn.rollback()
#             raise

#     def get_expenses_today(self):
#         try:
#             today = datetime.now().strftime("%Y-%m-%d")
#             self.cursor.execute("SELECT category, amount FROM expenses WHERE date = ?", (today,))
#             return self.cursor.fetchall()
#         except sqlite3.Error as e:
#             print(f"Error retrieving today's expenses: {e}")
#             return []

#     def get_expenses_by_date(self, date):
#         try:
#             self.cursor.execute("SELECT category, amount FROM expenses WHERE date = ?", (date,))
#             return self.cursor.fetchall()
#         except sqlite3.Error as e:
#             print(f"Error retrieving expenses for {date}: {e}")
#             return []

#     def __del__(self):
#         try:
#             self.conn.close()
#             print("Database connection closed")
#         except sqlite3.Error as e:
#             print(f"Error closing database: {e}")



import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path="restaurant.db"):
        try:
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.create_tables()
            self.initialize_default_user()
            print("Database initialized")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise

    def create_tables(self):
        try:
            # Users table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('Admin', 'User'))
                )
            ''')
            # Waiters table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS waiters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            ''')
            # Product table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS product (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    price REAL NOT NULL,
                    category TEXT NOT NULL DEFAULT 'Uncategorized'
                )
            ''')
            # Orders table with foreign key to waiters
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    order_id TEXT PRIMARY KEY,
                    order_type TEXT NOT NULL,
                    order_date TEXT NOT NULL,
                    waiter TEXT NOT NULL,
                    FOREIGN KEY (waiter) REFERENCES waiters(name)
                )
            ''')
            # Order_items table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id TEXT NOT NULL,
                    item_name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    total REAL NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(order_id)
                )
            ''')
            # Expenses table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    date TEXT NOT NULL
                )
            ''')
            self.conn.commit()
            print("Tables created successfully")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            raise

    def initialize_default_user(self):
        try:
            self.cursor.execute('''
                INSERT OR IGNORE INTO users (username, password, role)
                VALUES (?, ?, ?)
            ''', ("admin", "admin123", "Admin"))
            self.conn.commit()
            print("Default admin user initialized")
        except sqlite3.Error as e:
            print(f"Error initializing default user: {e}")
            raise

    def add_user(self, username, password, role):
        try:
            self.cursor.execute('''
                INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)
            ''', (username, password, role))
            self.conn.commit()
            print(f"Added user: {username}, Role={role}")
        except sqlite3.IntegrityError:
            print(f"Error: Username {username} already exists")
            raise Exception("Username already exists")
        except sqlite3.Error as e:
            print(f"Error adding user {username}: {e}")
            self.conn.rollback()
            raise

    def update_user(self, user_id, username, password, role):
        try:
            self.cursor.execute('''
                UPDATE users
                SET username = ?, password = ?, role = ?
                WHERE id = ?
            ''', (username, password, role, user_id))
            if self.cursor.rowcount == 0:
                print(f"No user found with id: {user_id}")
                raise ValueError(f"No user found with id: {user_id}")
            self.conn.commit()
            print(f"Updated user: ID={user_id}, Username={username}, Role={role}")
        except sqlite3.IntegrityError:
            print(f"Error: Username {username} already exists")
            raise Exception("Username already exists")
        except sqlite3.Error as e:
            print(f"Error updating user ID {user_id}: {e}")
            self.conn.rollback()
            raise

    def delete_user(self, user_id):
        try:
            self.cursor.execute('''
                DELETE FROM users
                WHERE id = ?
            ''', (user_id,))
            if self.cursor.rowcount == 0:
                print(f"No user found with id: {user_id}")
                raise ValueError(f"No user found with id: {user_id}")
            self.conn.commit()
            print(f"Deleted user: ID={user_id}")
        except sqlite3.Error as e:
            print(f"Error deleting user ID {user_id}: {e}")
            self.conn.rollback()
            raise

    def authenticate_user(self, username, password):
        try:
            self.cursor.execute('''
                SELECT username, role
                FROM users
                WHERE username = ? AND password = ?
            ''', (username, password))
            result = self.cursor.fetchone()
            if result:
                print(f"Authenticated user: {username}")
                return {"username": result[0], "role": result[1]}
            print(f"Authentication failed for user: {username}")
            return None
        except sqlite3.Error as e:
            print(f"Error authenticating user {username}: {e}")
            return None

    def get_user_role(self, username):
        try:
            self.cursor.execute('''
                SELECT role
                FROM users
                WHERE username = ?
            ''', (username,))
            result = self.cursor.fetchone()
            if result:
                print(f"Retrieved role for {username}: {result[0]}")
                return result[0]
            print(f"No role found for user: {username}")
            return None
        except sqlite3.Error as e:
            print(f"Error retrieving role for {username}: {e}")
            return None

    def get_all_users(self):
        try:
            self.cursor.execute('''
                SELECT id, username, password, role
                FROM users
            ''')
            users = [{"id": row[0], "username": row[1], "password": row[2], "role": row[3]} for row in self.cursor.fetchall()]
            print(f"Retrieved {len(users)} users")
            return users
        except sqlite3.Error as e:
            print(f"Error retrieving users: {e}")
            return []

    def add_waiter(self, name):
        try:
            self.cursor.execute('''
                INSERT INTO waiters (name)
                VALUES (?)
            ''', (name,))
            self.conn.commit()
            print(f"Added waiter: {name}")
        except sqlite3.IntegrityError:
            print(f"Error: Waiter name {name} already exists")
            raise Exception("Waiter name already exists")
        except sqlite3.Error as e:
            print(f"Error adding waiter {name}: {e}")
            self.conn.rollback()
            raise

    def update_waiter(self, waiter_id, name):
        try:
            self.cursor.execute('''
                UPDATE waiters
                SET name = ?
                WHERE id = ?
            ''', (name, waiter_id))
            if self.cursor.rowcount == 0:
                print(f"No waiter found with id: {waiter_id}")
                raise ValueError(f"No waiter found with id: {waiter_id}")
            if self.cursor.rowcount > 0 and name:
                self.cursor.execute('''
                    UPDATE orders
                    SET waiter = ?
                    WHERE waiter = (SELECT name FROM waiters WHERE id = ?)
                ''', (name, waiter_id))
                print(f"Updated {self.cursor.rowcount} orders to new waiter name: {name}")
            self.conn.commit()
            print(f"Updated waiter: ID={waiter_id}, Name={name}")
        except sqlite3.IntegrityError:
            print(f"Error: Waiter name {name} already exists")
            raise Exception("Waiter name already exists")
        except sqlite3.Error as e:
            print(f"Error updating waiter ID {waiter_id}: {e}")
            self.conn.rollback()
            raise

    def delete_waiter(self, waiter_id):
        try:
            self.cursor.execute('''
                SELECT name
                FROM waiters
                WHERE id = ?
            ''', (waiter_id,))
            result = self.cursor.fetchone()
            if not result:
                print(f"No waiter found with id: {waiter_id}")
                raise ValueError(f"No waiter found with id: {waiter_id}")
            self.cursor.execute('''
                DELETE FROM waiters
                WHERE id = ?
            ''', (waiter_id,))
            self.conn.commit()
            print(f"Deleted waiter: ID={waiter_id}")
        except sqlite3.Error as e:
            print(f"Error deleting waiter ID {waiter_id}: {e}")
            Ascending
            self.conn.rollback()
            raise

    def get_all_waiters(self):
        try:
            self.cursor.execute('''
                SELECT id, name
                FROM waiters
            ''')
            waiters = [{"id": row[0], "name": row[1]} for row in self.cursor.fetchall()]
            print(f"Retrieved {len(waiters)} waiters")
            return waiters
        except sqlite3.Error as e:
            print(f"Error retrieving waiters: {e}")
            return []

    def initialize_menu(self, menu_items):
        try:
            self.cursor.executemany('''
                INSERT OR REPLACE INTO product (name, price, category)
                VALUES (?, ?, ?)
            ''', [(item["name"], item["price"], item.get("category", "Uncategorized")) for item in menu_items])
            self.conn.commit()
            print(f"Initialized product table with {len(menu_items)} items")
        except sqlite3.Error as e:
            print(f"Error initializing product table: {e}")
            self.conn.rollback()
            raise

    def get_menu(self):
        try:
            self.cursor.execute("SELECT name, price, category FROM product")
            result = [{"name": row[0], "price": row[1], "category": row[2]} for row in self.cursor.fetchall()]
            print(f"Retrieved product table: {result}")
            return result
        except sqlite3.Error as e:
            print(f"Error retrieving product table: {e}")
            return []

    def edit_product(self, old_name, new_name, price, category="Uncategorized"):
        try:
            print(f"Executing edit_product: old_name={old_name}, new_name={new_name}, price={price}, category={category}")
            self.cursor.execute('''
                UPDATE product
                SET name = ?, price = ?, category = ?
                WHERE name = ?
            ''', (new_name, price, category, old_name))
            if self.cursor.rowcount == 0:
                print(f"No product found with name: {old_name}")
                raise ValueError(f"No product found with name: {old_name}")
            if old_name != new_name:
                self.cursor.execute('''
                    UPDATE order_items
                    SET item_name = ?
                    WHERE item_name = ?
                ''', (new_name, old_name))
                print(f"Updated {self.cursor.rowcount} order_items from {old_name} to {new_name}")
            self.conn.commit()
            print(f"Edited product: {old_name} -> {new_name}, Price={price}, Category={category}")
        except sqlite3.Error as e:
            print(f"Error editing product {old_name}: {e}")
            self.conn.rollback()
            raise

    def delete_product(self, name):
        try:
            print(f"Executing delete_product: name={name}")
            self.cursor.execute("DELETE FROM product WHERE name = ?", (name,))
            if self.cursor.rowcount == 0:
                print(f"No product found with name: {name}")
                raise ValueError(f"No product found with name: {name}")
            self.conn.commit()
            print(f"Deleted product: {name}")
        except sqlite3.Error as e:
            print(f"Error deleting product {name}: {e}")
            self.conn.rollback()
            raise

    def add_order(self, order_id, order_type, items, order_date, waiter):
        try:
            self.cursor.execute('''
                INSERT INTO orders (order_id, order_type, order_date, waiter)
                VALUES (?, ?, ?, ?)
            ''', (order_id, order_type, order_date, waiter))
            for item in items:
                self.cursor.execute('''
                    INSERT INTO order_items (order_id, item_name, quantity, price, total)
                    VALUES (?, ?, ?, ?, ?)
                ''', (order_id, item["name"], item["quantity"], item["price"], item["total"]))
            self.conn.commit()
            print(f"DB: Saved order {order_id}, Type={order_type}, Items={items}, Date={order_date}, Waiter={waiter}")
        except sqlite3.Error as e:
            print(f"Error saving order {order_id}: {e}")
            self.conn.rollback()
            raise

    def get_orders_by_date(self, date):
        try:
            self.cursor.execute('''
                SELECT o.order_id, o.order_type, o.order_date, o.waiter, SUM(oi.total) as total
                FROM orders o
                JOIN order_items oi ON o.order_id = oi.order_id
                WHERE o.order_date LIKE ?
                GROUP BY o.order_id, o.order_type, o.order_date, o.waiter
            ''', (f"{date}%",))
            return [{"order_id": row[0], "order_type": row[1], "order_date": row[2], "waiter": row[3], "total": row[4]} for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error retrieving orders for {date}: {e}")
            return []

    def get_order_items(self, order_id):
        try:
            self.cursor.execute('''
                SELECT item_name, quantity, price, total
                FROM order_items
                WHERE order_id = ?
            ''', (order_id,))
            return [{"item_name": row[0], "quantity": row[1], "price": row[2], "total": row[3]} for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error retrieving items for order {order_id}: {e}")
            return []

    def add_expense(self, category, amount, date):
        try:
            self.cursor.execute('''
                INSERT INTO expenses (category, amount, date)
                VALUES (?, ?, ?)
            ''', (category, amount, date))
            self.conn.commit()
            print(f"Added expense: {category}, {amount}, {date}")
        except sqlite3.Error as e:
            print(f"Error adding expense: {e}")
            self.conn.rollback()
            raise

    def get_expenses_today(self):
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            self.cursor.execute("SELECT category, amount FROM expenses WHERE date = ?", (today,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving today's expenses: {e}")
            return []

    def get_expenses_by_date(self, date):
        try:
            self.cursor.execute("SELECT category, amount FROM expenses WHERE date = ?", (date,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving expenses for {date}: {e}")
            return []

    def __del__(self):
        try:
            self.conn.close()
            print("Database connection closed")
        except sqlite3.Error as e:
            print(f"Error closing database: {e}")
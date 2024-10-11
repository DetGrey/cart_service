import sqlite3

DB_NAME = 'cart.db'

def create_table():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            amount INTEGER
        )
        """
        
        # Execute the create table statement
        cur.execute(create_table_query)

def add_new_item(data):
    try:
        product_id = data.get('product_id', None)
        amount = data.get('amount', None)
        if product_id and amount:
            existing = find_item_by_product_id(product_id)
            if existing[0] == 200:
                return update_amount(existing[1]["id"], amount)

        # Connect to db/file - both read or create if not exists
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            
            cur.execute(
                '''
                INSERT OR IGNORE INTO cart (product_id, amount)
                VALUES (?, ?)
                ''',
                (
                    data.get('product_id', None),
                    data.get('amount', None),
                )
            )
            return [201, {"message": "New item added to cart successfully."}]

    except sqlite3.Error as e:
        return [500, {"error": str(e)}]
        

def update_amount(id, amount):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()

            cur.execute(f'UPDATE cart SET amount = {amount} WHERE id = {id}')
            return [200, {"message": "Product amount updated successfully."}]
        
    except sqlite3.Error as e:
        return [500, {"error": str(e)}]


def select_all_items():
    try:
        # Connect to db/file - both read or create if not exists
        with sqlite3.connect(DB_NAME) as conn:
            # Set the row factory to sqlite3.Row - By setting conn.row_factory = sqlite3.Row, you tell SQLite to return rows as sqlite3.Row objects, which can be accessed like dictionaries.
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute('SELECT * FROM cart')

            # Fetch all rows and convert them to dictionaries
            data = cur.fetchall()
        
            if data:
                return [200, [dict(row) for row in data]]
            else:
                return [204, {"message": "No items in cart"}]
    
    except sqlite3.Error as e:
        return [500, {"error": str(e)}]


def delete_item_by_id(id):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()

            # Delete the row with the specified id
            cur.execute('DELETE FROM cart WHERE id = ?', (id,))
            return [204, {"message": "Item deleted from cart successfully."}]

    except sqlite3.Error as e:
        return [500, {"error": str(e)}]


def find_item_by_id(id):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            # Set the row factory to sqlite3.Row - By setting conn.row_factory = sqlite3.Row, you tell SQLite to return rows as sqlite3.Row objects, which can be accessed like dictionaries.
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            cur.execute('SELECT * FROM cart WHERE id = ?', (id,))
            data = cur.fetchall()
        
            if data:
                return [200, [dict(row) for row in data][0]]
            else:
                return [404, {"message": "Item not found"}]
        
    except sqlite3.Error as e:
        return [500, {"error": str(e)}]

def find_item_by_product_id(product_id):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            # Set the row factory to sqlite3.Row - By setting conn.row_factory = sqlite3.Row, you tell SQLite to return rows as sqlite3.Row objects, which can be accessed like dictionaries.
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            cur.execute('SELECT * FROM cart WHERE product_id = ?', (product_id,))
            data = cur.fetchall()
        
            if data:
                return [200, [dict(row) for row in data][0]]
            else:
                return [404, {"message": "Item not found"}]
        
    except sqlite3.Error as e:
        return [500, {"error": str(e)}]

#create_table()
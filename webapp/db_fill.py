from config import Config
import psycopg2

db_url = Config.SQLALCHEMY_DATABASE_URI

def create_users():
    try:
        conn = psycopg2.connect(db_url, sslmode='require')
        
        cur = conn.cursor()
        
        # Create user
        user1 = ("bailey","password")
        user2 = ("pedro","password")
        
        users = [user1,user2]
        
        for user in users:
            sql = """
            INSERT INTO users (username, password) VALUES {}
            """.format(user)
            cur.execute(sql)
            
        conn.commit()
        
        cur.close()
        conn.close()
    except (Exception, psycopg2.Error) as e:
        print("Error: ",e)
    
def create_token():
    try:
        conn = psycopg2.connect(db_url, sslmode='require')
        
        cur = conn.cursor()
        
        # Create token
        token1 = (1,"bailey_token", "BDVT",1000)
        
        sql = """
        INSERT INTO tokens (user_id, name, symbol, total_supply) VALUES {}
        """.format(token1)
        
        cur.execute(sql)
        
        # Update ownership
        owner = (1, 1, 1000)
        sql = """
        INSERT INTO ownership (user_id, token_id, quantity) VALUES {}
        """.format(owner)
        
        cur.execute(sql)
        
        conn.commit()
        
        cur.close()
        conn.close()
    except (Exception, psycopg2.Error) as e:
        print("Error: ",e)

def test_orders():
    try: 
        conn = psycopg2.connect(db_url, sslmode='require')
    
        cur = conn.cursor()        
        
        # Bailey sell orders
        order1 = (1, 1, "offer", 12, 10, False, 0)
        order2 = (1, 1, "offer", 8, 5, False, 0)
        
        # Pedro bid orders
        order3 = (2, 1, "bid", 14, 5, False, 0)
        order4 = (2, 1, "bid", 9, 7, False, 0)
        
        orders = [order1, order2, order3, order4]
        
        for order in orders:
            sql = """
            INSERT INTO orders (user_id, token_id, type, price, quantity, filled, amount_filled) 
            VALUES {}
            """.format(order)
        
            cur.execute(sql)
            
            conn.commit()
        
        cur.close()
        conn.close()
    except (Exception, psycopg2.Error) as e:
        print("Error: ",e)
        
def main():
    create_users()
    create_token()
    test_orders()
    
if __name__=="__main__":
    main()
from config import Config
import psycopg2

db_url = Config.SQLALCHEMY_DATABASE_URI

def create_user():
    try:
        conn = psycopg2.connect(db_url, sslmode='require')
        
        cur = conn.cursor()
        
        # Create user
        user1 = ("bailey","password")
        
        sql = """
        INSERT INTO users (username, password) VALUES {}
        """.format(user1)
        
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
        conn.commit()
        
        cur.close()
        conn.close()
    except (Exception, psycopg2.Error) as e:
        print("Error: ",e)

def test_orders():
    try: 
        conn = psycopg2.connect(db_url, sslmode='require')
    
        cur = conn.cursor()        
        
        # Create orders
        order1 = (1, 1, "bid", 12, 10, False, 0)
        order2 = (1, 1, "offer", 8, 7, False, 0)
        order3 = (1, 1, "bid", 8, 5, False, 0)
        order4 = (1, 1, "offer", 7, 5, False, 0)
        order5 = (1, 1, "bid", 5, 25, False, 0)
        
        orders = [order1, order2, order3, order4, order5]
        
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
    create_user()
    create_token()
    test_orders()
    
if __name__=="__main__":
    main()
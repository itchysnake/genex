import psycopg2
import pandas as pd

db_url = "postgres://tkvzeqhgrnbszs:899301ba612f5b92a57b37a2cf961522c71580809f6eb8c79c9b404cde0e4450@ec2-52-210-120-210.eu-west-1.compute.amazonaws.com:5432/da532n97r99dvu"

def day_trades(token_id, delta):
    """
    *
    * delta (int): number of days back from today
    """
    try:
        conn = psycopg2.connect(db_url, sslmode='require')
    
        cur = conn.cursor()
        
        sql = """
        SELECT * FROM trades 
        WHERE token_id = {} AND date(timestamp) = current_date - INTEGER '{}'
        ORDER BY timestamp ASC
        """.format(token_id, delta)
        
        cur.execute(sql)

        # Get last trade
        trade = cur.fetechall()
        
        if trade is None:
            return None
        else:
            eod_price = trade[0]
            return eod_price
        
    except (Exception, psycopg2.Error) as e:
        print("Error fetching data: ",e)
        
def last_trade(token_id, delta):
    """
    *
    * delta (int): number of days back from today (1 for yesterday)
    """
    try:
        conn = psycopg2.connect(db_url, sslmode='require')
    
        cur = conn.cursor()
        
        sql = """
        SELECT price FROM trades 
        WHERE token_id = {} AND date(timestamp) = current_date - INTEGER '{}'
        ORDER BY timestamp ASC
        """.format(token_id, delta)
        
        cur.execute(sql)

        trade = cur.fetchone()
        
        if trade is None:
            return None
        else:
            return trade

    except (Exception, psycopg2.Error) as e:
        print("Error fetching data: ",e)

def set_price(token_id, price):
    """
    """
    try:
        conn = psycopg2.connect(db_url, sslmode='require')
    
        cur = conn.cursor()
        
        sql = """
        UPDATE quotes SET price = {} WHERE token_id = {} AND date(timestamp) = current_date
        """.format(price, token_id)
        
        cur.execute(sql)
        
        conn.commit()
        conn.close()

    except (Exception, psycopg2.Error) as e:
        print("Error fetching data: ",e)

def set_close(token_id):
    """
    Sets last trade as close price
    """
    
    # Get todays last trade
    last_trade = last_trade(token_id, 0)
    
    # Set to todays close
    last_trade_price = last_trade["price"]
    
    sql = """
    UPDATE quotes SET 
    """

    try:
        conn = psycopg2.connect(db_url, sslmode='require')
    
        cur = conn.cursor()

def set_open(token_id):
    """
    Sets last close as current open
    """

def set_min(token_id):
    """
    """    

def set_max(token_id):

def ref_price(token_id):
    """
    """
    try:
        conn = psycopg2.connect(db_url, sslmode='require')
    
        cur = conn.cursor()

        sql = """
        SELECT price FROM trades WHERE token_id = {} ORDER BY timestamp ASC
        """.format(token_id)
        
        cur.execute(sql)

        # Get trade
        trade = cur.fetchone()
        
        # If no trade yet
        if trade is None:
            return None
        else:
            ref_price = trade[0]
            return ref_price
        
        # Close DB
        cur.close()
        conn.close()
        
    except (Exception, psycopg2.Error) as e:
        print("Error fetching data: ",e)
        
def eod_price(token_id):
    try:
        conn = psycopg2.connect(db_url, sslmode='require')
    
        cur = conn.cursor()
        
        sql = """
        SELECT price FROM trades 
        WHERE token_id = {} AND date(timestamp) = current_date - INTEGER '1'
        ORDER BY timestamp ASC
        """.format(token_id)
        
        cur.execute(sql)

        # Get last trade
        trade = cur.fetchone()
        
        if trade is None:
            return None
        else:
            eod_price = trade[0]
            return eod_price
        
    except (Exception, psycopg2.Error) as e:
        print("Error fetching data: ",e)

def price_delta(token_id):
    """
    Current price versus yesterdays closing
    """
    _eod_price = eod_price(token_id)
    _ref_price = ref_price(token_id)
    
    delta = (_ref_price - _eod_price) / _eod_price
    
    return delta

def get_tags(token_id):
    """
    """
    try:
        conn = psycopg2.connect(db_url, sslmode='require')
    
        cur = conn.cursor()
        
        sql = """
        SELECT (primary_tag, secondary_tag) FROM tokens 
        WHERE id = {}
        """.format(token_id)
        
        cur.execute(sql)

        # Get tags
        tags = cur.fetchone()
        
        if tags == None:
            return None
        else:
            tags = tags[0]
            return tags
        
    except (Exception, psycopg2.Error) as e:
        print("Error fetching data: ",e)


def volume(token_id, type = None):
    """
    * type (str): "bid" or "offer"
    """
    try:
        conn = psycopg2.connect(db_url, sslmode='require')
    
        cur = conn.cursor()
        
        if type == None:
            sql = """
            SELECT quantity, amount_filled FROM orders
            WHERE token_id = {} AND filled = False
            """.format(token_id)
        else:
            sql = """
            SELECT quantity, amount_filled FROM orders
            WHERE token_id = {} AND type = '{}' AND filled = False 
            """.format(token_id, type)

        cur.execute(sql)

        # Get all orders
        orders = cur.fetchall()
        
        if orders is None:
            return None
        else:
            vol = 0
            
            # Iterate and add to vol for every bid
            for order in orders:
                quantity = order[0]
                filled = order[1]
                
                vol += quantity - filled
                
            return vol
        
    except (Exception, psycopg2.Error) as e:
        print("Error fetching data: ",e)
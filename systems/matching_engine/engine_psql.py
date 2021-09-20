import psycopg2
from config import Config
import pandas as pd

def get_token_ids():
    # Collects all token_ids so they can be used in lookup for parse
    
    try:
        conn = psycopg2.connect(Config.DATABASE_URL, sslmode='require')
    
        cur = conn.cursor()
        
        sql = """
        select id from tokens
        """
        
        cur.execute(sql)
        
        token_ids = cur.fetchone()
        
        cur.close()
        conn.close()
        
        return token_ids
    
    except (Exception, psycopg2.Error) as e:
        print("Error fetching data: ",e)
        
def get_orders(token_id, direction, sort_by):
    """
    :Params:
        * token_id
        * direction
        * sort_by
    """
    try:
        conn = psycopg2.connect(Config.DATABASE_URL, sslmode='require')
    
        cur = conn.cursor()
        
        sql = """
        select * from orders WHERE token_id = {} AND type = '{}' ORDER BY price {}
        """.format(token_id, direction, sort_by)
        
        cur.execute(sql)
        
        orders = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return orders
    
    except (Exception, psycopg2.Error) as e:
        print("Error fetching data: ",e)    

def submit_trade():
    pass

def delete_order()

def parse():
    """
    Parses over current orders and finds matching ones which are turned
    into trades.
    """
    token_ids = get_token_ids()

    for token_id in token_ids:
        
        buy_orders = get_orders(token_id, "bid", "DESC")
        sell_orders = get_orders(token_id, "offer", "ASC")
        
        # only if there are outstanding orders is it parsed
        if len(buy_orders) > 0 and len(sell_orders) > 0:
            
            # Format orders into dataframes and sort them in descending order
            cols = ["id",
                    "user_id",
                    "token_id",
                    "type",
                    "price",
                    "quantity"]
            
            buy_df = pd.DataFrame(buy_orders, columns=cols)
            sell_df = pd.DataFrame(sell_orders, columns=cols)

            print(buy_df)
            print(sell_df)
            
            # Process from the bid side until all trades are matched
            for i in range(len(buy_df)):
                # highest bid of the orderbook
                highest_bid = buy_df.loc[0]
                
                # all orders with an ask price lower than the highest bid
                df = sell_df.loc[highest_bid["price"] > sell_df["price"]]
                
                # if prices don't line up, can't be matched and process ends
                if df.empty:
                    print("Orders cannot be settled (price).")
                
                # building the trade order(s) for this bid
                settle_amount = highest_bid["quantity"]
                
                for sell_order in sell_df.iterrows():
                    print(sell_order)
                    
                    # the sell order is fully consumed
                    if settle_amount - sell_order["quantity"] > 0:
                        settle_amount -= sell_order["quantity"]
                        
                        submit_trade()
                        delete_order()
                    
                    # the bid order is filled
                    elif settle_amount - sell_order["quantity"] < 0:
                        sell_order["quantity"] -= settle_amount
                        
                        # sell order was fully consumed
                        if sell_order["quantity"] == 0:
                             submit_trade()
                             delete_order("buy order")
                             delete_order("sell order")
                        
                        # sell order was not fully consumed
                        else:
                            update_order("sell order")
                            
                        submit_trade()
                        delete_order("buy order")

        else:
            print("No outstanding settlement (volume).")


def main():

    try:
        conn = psycopg2.connect(Config.DATABASE_URI, sslmode='require')
    
        cursor = conn.cursor()
        
        sql_query = """
        select * from users
        """
        
        cursor.execute(sql_query)
        
        data = cursor.fetchall()
        
        for row in data:
            print(row)
    except (Exception, psycopg2.Error) as e:
        print("Error fetching data: ",e)
        
    finally:
        if conn:
            cursor.close()
            conn.close()
            
if __name__=="__main__":
    parse()
import psycopg2

class Db:
    def __init__(self):
        self.db_url = "postgres://tkvzeqhgrnbszs:899301ba612f5b92a57b37a2cf961522c71580809f6eb8c79c9b404cde0e4450@ec2-52-210-120-210.eu-west-1.compute.amazonaws.com:5432/da532n97r99dvu"

    def get_table_colnames(self, table):
        try:
            conn = psycopg2.connect(self.db_url, sslmode='require')
        
            cur = conn.cursor()
            
            sql = """
            SELECT * FROM {} LIMIT 0
            """.format(table)
            
            cur.execute(sql)
            # fancy inline iteration to get all col names
            colnames = [desc[0] for desc in cur.description]
            
            cur.close()
            conn.close()
            
            return colnames
        
        except (Exception, psycopg2.Error) as e:
            print("Error fetching data: ",e)

    def get_token_ids(self):
        """
        Collects all token IDs from "tokens" table
        
        :Params:
        None
        
        :Returns:
        * token_ids (list>ints): List of token_ids (integers)
        """
        try:
            conn = psycopg2.connect(self.db_url, sslmode='require')
        
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
            

    def get_orders(self, token_id, type, sort_by, filled = False):
        """
        Gets filled or unfilled orders for a specific ID, direction and sorts
        the output in ascending or descending price.
        
        :Params:
        * token_id (int): token lookup
        * type (str): "bid" or "offer" - direction of trade
        * sort_by (str): "ASC" or "DESC" - sort by ascending or descending price
        * filled (bool): filters by filled or unfilled orders 
        
        :Returns:
        * orders (list>tuples): all columns of all available orders
        """
        try:
            conn = psycopg2.connect(self.db_url, sslmode='require')
        
            cur = conn.cursor()
            
            # looking for tokens of a specific id, either bid or offer, and that haven't been filled
            # and is ordered ascending or descending depending on if its bid or offer
            sql = """
            select * from orders WHERE token_id = {} AND type = '{}' AND filled = '{}'
            ORDER BY price {}
            """.format(token_id, type, filled, sort_by)
            
            cur.execute(sql)
            
            orders = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return orders
        
        except (Exception, psycopg2.Error) as e:
            print("Error fetching data: ",e)
    
    def submit_trade(self, timestamp, bid_order_id, offer_order_id, buyer_id, seller_id, token_id, price, quantity):
        """
        Inserts a trade into "trades" table
        
        :Params:
        * timestamp (datetime): UTC datetime of current trade
        * bid_order_id (int): order ID from bid used to settle this trade
        * offer_order_id (int): order ID from offer used to settle this trade
        * buyer_id (int): user ID of the bidding party
        * seller_id (int): user ID of the offering party
        * token_id (int): token being traded
        * price (float): price trade is occuring at
        * quantity (int): quantity of tokens traded
        
        :Returns:
        None
        """
        try: 
            conn = psycopg2.connect(self.db_url, sslmode='require')
        
            cur = conn.cursor()
            
            sql = """
            INSERT INTO trades (timestamp,
                                bid_order_id,
                                offer_order_id,
                                buyer_id,
                                seller_id,
                                token_id,
                                price,
                                quantity) 
            VALUES (TIMESTAMP '{}', {}, {}, {}, {}, {}, {}, {})
            """.format(timestamp, 
                        bid_order_id,
                        offer_order_id,
                        buyer_id,
                        seller_id,
                        token_id,
                        price,
                        quantity)
            
            cur.execute(sql)
            
            conn.commit()
            
            cur.close()
            conn.close()
            
        except (Exception, psycopg2.Error) as e:
            conn.rollback()
            print("Error: ",e)
    
    def delete_order(self, order_id):
        # shouldn't be used
        try: 
            conn = psycopg2.connect(self.db_url, sslmode='require')
        
            cur = conn.cursor()
            
            sql = """
            DELETE FROM orders WHERE id = {}
            """.format(order_id)
            
            cur.execute(sql)
            
            conn.commit()
            
            cur.close()
            conn.close()
        except (Exception, psycopg2.Error) as e:
            print("Error: ",e)
    
    def update_order(self, order_id, amount_filled, filled = False):
        """
        Update an order in "orders" table
        
        :Params:
        * order_id (int): order lookup
        * amount_filled (int): volume filled of total quantity
        * filled (bool): True if order is filled (amount_filled = quantity)
        
        :Returns:
        None
        """
        try: 
            conn = psycopg2.connect(self.db_url, sslmode='require')
        
            cur = conn.cursor()
            
            sql = """
            UPDATE orders SET amount_filled = {}, filled = {} WHERE id = {}
            """.format(amount_filled, filled, order_id)
            
            cur.execute(sql)
            
            conn.commit()
            
            cur.close()
            conn.close()
    
        except (Exception, psycopg2.Error) as e:
            print("Error: ",e)
            
    def update_ownership(self, user_id, token_id, quantity):
        
        try:
            conn = psycopg2.connect(self.db_url, sslmode='require')
        
            cur = conn.cursor()
            
            # Get current ownership
            sql = """
            SELECT quantity FROM ownership WHERE user_id = {} AND token_id = {}
            """.format(user_id, token_id)
            
            cur.execute(sql)
            
            current_amount = cur.fetchone()
            
            # If this is his first trade of the asset
            if current_amount is None:
                sql = """
                INSERT INTO ownership (user_id, token_id, quantity) 
                VALUES ({}, {}, {}) 
                """.format(user_id, token_id, quantity)
                
                cur.execute(sql)
                cur.close()
            
            # Update ownership
            else:
                # select first tuple returned by sql lookup
                current_amount = current_amount[0]
                new_amount = current_amount + quantity
                
                sql = """
                UPDATE ownership SET quantity = {} WHERE user_id = {} AND token_id = {}
                """.format(new_amount, user_id, token_id)
            
                cur.execute(sql)
                cur.close()
                
            conn.commit()
            conn.close()
        
        except (Exception, psycopg2.Error) as e:
            print("Error updating ownership: ",e)
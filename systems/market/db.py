import psycopg2

class Db:
    def __init__(self):
        self.db_url = "postgres://tkvzeqhgrnbszs:899301ba612f5b92a57b37a2cf961522c71580809f6eb8c79c9b404cde0e4450@ec2-52-210-120-210.eu-west-1.compute.amazonaws.com:5432/da532n97r99dvu"
            
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
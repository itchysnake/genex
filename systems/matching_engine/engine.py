import psycopg2
import pandas as pd

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
    
    def submit_trade(self, bid_order_id, offer_order_id, buyer_id, seller_id, token_id, price, quantity):
        """
        Inserts a trade into "trades" table
        
        :Params:
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
            INSERT INTO trades (bid_order_id,
                                offer_order_id,
                                buyer_id,
                                seller_id,
                                token_id,
                                price,
                                quantity) 
            VALUES ({}, {}, {}, {}, {}, {}, {})
            """.format(bid_order_id,
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

class Parse:
    def __init__(self):
        self.db = Db()
    
    def match(self, token_id):
        """
        Iterates over a specific token's outstanding bids and offers. Matches
        from left to right. Top left bid to outstanding offers. Stops if:
            no bids or no offers
            bids are too low for outstanding offers
            no remaining offers
        
        :Params:
        * token_id (int): token lookup
        
        :Returns:
        None
        """
            
        # try and work this better to see if there are available trades so I don't pull
        # the entire order log
        bid_orders = self.db.get_orders(token_id, "bid", "DESC")
        offer_orders = self.db.get_orders(token_id, "offer", "ASC")
        
        # only if there are outstanding orders is it parsed
        if len(bid_orders) > 0 and len(offer_orders) > 0:
            
            # Format bids so they can be iterrated over as the 'static list'
            cols = ["id",
                    "user_id",
                    "token_id",
                    "type",
                    "price",
                    "quantity",
                    "filled",
                    "amount_filled"]
            bid_df = pd.DataFrame(bid_orders, columns=cols)
            
            # Process from the highest bid until matches are exhausted
            # df's already sorted so first row is highest bid / lowest offer
            # bids are static, only offers are manipulated
            for bid in bid_df.iterrows():
                
                # select the row from the tuple returned by iterrows
                bid = bid[1]
    
                # pulls latest list of offer_orders (per iteration)
                offer_orders = self.db.get_orders(token_id, "offer", "ASC")
                offer_df = pd.DataFrame(offer_orders, columns=cols)
                
                print("Handling Bid: ",bid["id"])
                
                # checks if there are offers left
                if not offer_df.empty:
                    lowest_offer = offer_df.loc[0]
                else:
                    print("No more valid offers")
                    break
                
                # stop parsing if bids are lower than offers
                if bid["price"] < lowest_offer["price"]:
                    print("Bids too low")
                    break
                
                # amount needed to close bid
                bid_unfilled = bid["quantity"] - bid["amount_filled"]
    
                # building the trade order(s) for this bid
                for offer in offer_df.iterrows():
                    
                    # select row from tuple returned by iterrows
                    offer = offer[1]
    
                    # fill available through this offer
                    offer_unfilled = offer["quantity"] - offer["amount_filled"]
    
                    # the sell order is fully consumed
                    if bid_unfilled - offer_unfilled > 0:
                        
                        # how much of bid is left over
                        # carried over to next offer iteration until bid closed
                        bid_unfilled -= offer_unfilled
                        
                        # building the trade
                        bid_order_id = bid["id"]
                        offer_order_id = offer["id"]
                        buyer_id = bid["user_id"]
                        seller_id = offer["user_id"]
                        token_id = offer["token_id"]
                        price = offer["price"] # check how this works might need to be based on bid price
                        quantity = offer_unfilled
                        
                        # submit trade
                        self.db.submit_trade(bid_order_id,
                                     offer_order_id,
                                     buyer_id,
                                     seller_id,
                                     token_id,
                                     price,
                                     quantity)
                        
                        # update (close) offer
                        amount_filled = offer["amount_filled"] + offer_unfilled
                        self.db.update_order(offer["id"], offer["quantity"], filled = True)
                        
                    # the bid order is filled
                    elif bid_unfilled - offer_unfilled <= 0:
                        
                        # how much of offer is left over
                        offer_unfilled -= bid_unfilled
                        
                        # building the trade
                        bid_order_id = bid["id"]
                        offer_order_id = offer["id"]
                        buyer_id = bid["user_id"]
                        seller_id = offer["user_id"]
                        token_id = bid["token_id"]
                        price = offer["price"] # check how this works might need to be based on bid price
                        quantity = bid_unfilled
                        
                        # submit trade
                        self.db.submit_trade(bid_order_id,
                                     offer_order_id,
                                     buyer_id,
                                     seller_id,
                                     token_id,
                                     price,
                                     quantity)
                        
                        # update (close) bid
                        amount_filled = bid["quantity"]
                        self.db.update_order(bid["id"], amount_filled, filled = True)
                        
                        # sell order was fully consumed
                        if offer_unfilled == 0:                        
                            amount_filled = offer["amount_filled"] + bid_unfilled
                            self.db.update_order(offer["id"], amount_filled, filled = True)
                        
                        # sell order was not fully consumed
                        elif offer_unfilled > 0:                        
                            amount_filled = offer["amount_filled"] + bid_unfilled
                            self.db.update_order(offer["id"], amount_filled, filled = False)
                            
                        # sets outstanding fill to 0
                        bid_unfilled = 0
            
                #offers did not satisfy bid
                if bid_unfilled > 0:
    
                    amount_filled = bid["quantity"] - bid_unfilled             
                    self.db.update_order(bid["id"], amount_filled, filled = False)
    
            else:
                print("No outstanding settlement (volume).")

    def parse_all(self):
        """
        Iterates over all token IDs in "tokens" table, and applies matching
        logic to settle outstanding orders.
        
        :Params:
        None
        
        :Returns:
        None
        """
        token_ids = self.db.get_token_ids()
        
        print("*"*25)
        print("Starting parse")
        print("*"*25)
    
        for token_id in token_ids:
            self.match(token_id)
            
        print("*"*25)
        print("Parse ended")
        print("*"*25)

            
if __name__=="__main__":
    Parse().parse_all()
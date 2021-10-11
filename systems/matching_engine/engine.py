from db import Db
import pandas as pd
import datetime
from system import quotes
           
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
            colnames = self.db.get_table_colnames("orders")
            
            bid_df = pd.DataFrame(bid_orders, columns=colnames)
            
            # Process from the highest bid until matches are exhausted
            # df's already sorted so first row is highest bid / lowest offer
            # bids are static, only offers are manipulated
            for bid in bid_df.iterrows():
                
                # select the row from the tuple returned by iterrows
                bid = bid[1]
    
                # pulls latest list of offer_orders (per iteration)
                offer_orders = self.db.get_orders(token_id, "offer", "ASC")
                offer_df = pd.DataFrame(offer_orders, columns=colnames)
                
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
                    
                    # if bid is filled, break looking for offers
                    if bid_unfilled == 0:
                        break
    
                    # the sell order is fully consumed
                    if bid_unfilled - offer_unfilled > 0:
                        
                        # how much of bid is left over
                        # carried over to next offer iteration until bid closed
                        bid_unfilled -= offer_unfilled
                        
                        # building the trade
                        timestamp = datetime.datetime.utcnow()
                        bid_order_id = bid["id"]
                        offer_order_id = offer["id"]
                        buyer_id = bid["user_id"]
                        seller_id = offer["user_id"]
                        token_id = offer["token_id"]
                        price = offer["price"] # check how this works might need to be based on bid price
                        quantity = offer_unfilled
                        
                        # submit trade
                        print("Sell order fully conumsed: Submitting Trade!")
                        self.db.submit_trade(timestamp,
                                             bid_order_id,
                                             offer_order_id,
                                             buyer_id,
                                             seller_id,
                                             token_id,
                                             price,
                                             quantity)
                        
                        # update (close) offer
                        amount_filled = offer["amount_filled"] + offer_unfilled
                        self.db.update_order(offer["id"], offer["quantity"], filled = True)
                        
                        # update ownership
                        self.db.update_ownership(seller_id, token_id, -quantity)
                        self.db.update_ownership(buyer_id, token_id, quantity)
                        
                        # update quotes
                        quotes.
                        
                    # the bid order is perfectly filled
                    elif bid_unfilled - offer_unfilled == 0:

                        # building the trade
                        timestamp = datetime.datetime.utcnow()
                        bid_order_id = bid["id"]
                        offer_order_id = offer["id"]
                        buyer_id = bid["user_id"]
                        seller_id = offer["user_id"]
                        token_id = bid["token_id"]
                        price = offer["price"]
                        quantity = bid_unfilled
                        
                        # submit trade
                        self.db.submit_trade(timestamp,
                                             bid_order_id,
                                             offer_order_id,
                                             buyer_id,
                                             seller_id,
                                             token_id,
                                             price,
                                             quantity)
                        
                        # update (close) offer
                        amount_filled = offer["amount_filled"] + offer_unfilled
                        self.db.update_order(offer["id"], offer["quantity"], filled = True)

                        # update (close) both orders
                        amount_filled = bid["quantity"]
                        self.db.update_order(bid["id"], amount_filled, filled = True)
                        
                        #amount_filled = offer["amount_filled"] + bid_unfilled
                        #self.db.update_order(offer["id"], amount_filled, filled = True)
                        
                        # update ownership
                        self.db.update_ownership(seller_id, token_id, -quantity)
                        self.db.update_ownership(buyer_id, token_id, quantity)
                        
                        # breaks iteration
                        bid_unfilled = 0
                        break
                    
                    # the bid order is overfilled
                    elif bid_unfilled - offer_unfilled < 0:

                        # how much of offer is left over
                        offer_unfilled -= bid_unfilled
                        
                        # building the trade
                        timestamp = datetime.datetime.utcnow()
                        bid_order_id = bid["id"]
                        offer_order_id = offer["id"]
                        buyer_id = bid["user_id"]
                        seller_id = offer["user_id"]
                        token_id = bid["token_id"]
                        price = offer["price"] # check how this works might need to be based on bid price
                        quantity = bid_unfilled
                        
                        # submit trade
                        self.db.submit_trade(timestamp,
                                             bid_order_id,
                                             offer_order_id,
                                             buyer_id,
                                             seller_id,
                                             token_id,
                                             price,
                                             quantity)
                        
                        # update (close) bid
                        amount_filled = bid["quantity"]
                        self.db.update_order(bid["id"], amount_filled, filled = True)
                        
                        # update ownership
                        self.db.update_ownership(seller_id, token_id, -quantity)
                        self.db.update_ownership(buyer_id, token_id, quantity)
                        
                        # sell order was not fully consumed
                        amount_filled = offer["amount_filled"] + bid_unfilled
                        self.db.update_order(offer["id"], amount_filled, filled = False)
                            
                        # breaks iteration
                        bid_unfilled = 0
                        break
            
                #offers did not satisfy bid
                if bid_unfilled > 0:
    
                    amount_filled = bid["quantity"] - bid_unfilled             
                    self.db.update_order(bid["id"], amount_filled, filled = False)
    
            else:
                print("No outstanding settlement (volume).")

    def main(self):
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
    Parse().main()
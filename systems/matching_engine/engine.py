import pandas as pd
import numpy as np

class Order:
    # uninitialised, used for organisation
    
    # might need an order_id param
    def marketOrder(order_id, token_id, dir, price, qty):

        order = {"order_id": order_id,
                 "token_id": token_id,
                 "dir": dir,
                 "price": price,
                 "qty": qty}
            
        return order
       
class OrderBook:
    # initialised to allow insert of a pre-existing bid-ask data
    def __init__(self, bid_data = [], ask_data = []):
        cols = ["order_id",
                "token_id",
                "dir",
                 "price",
                 "qty"]
        
        self.bids = pd.DataFrame(data = bid_data, columns = cols)
        self.asks = pd.DataFrame(data = ask_data, columns = cols)
    
    # Orders must be passed as lists
    def add(self, orders):
        
        # iterates and adds
        for order in orders:
            # adds to bids df                
            if order["dir"] == "buy":
                # creates new idx
                idx = len(self.bids)
                # adds to df without duplicating current df (saves space)
                self.bids.loc[idx] = order
                
            # adds to asks df
            else:
                idx = len(self.asks)
                self.asks.loc[idx] = order
            
            
    # remove an order
    def remove(self, order):
        if order["dir"] == "buy":
            # find the row according to order_id
            # imagine df[df["column"] == param].index.values[0]
            index = self.bids[self.bids["order_id"] == order["order_id"]].index.values[0]
            self.bids = self.bids.drop(index)
        else:
            index = self.asks[self.asks["order_id"] == order["order_id"]].index.values[0]
            self.asks = self.asks.drop(index)

class TradeBook:
    def __init__(self, data =[]):
        cols = ["order_id",
                "token_id",
                "dir",
                "price",
                "qty"]
        self.tradebook = pd.DataFrame(data = data, columns = cols)

    def add(self, trade):
        idx = len(self.tradebook)
        self.tradebook.loc[idx] = trade

    def remove(self, trade):
        pass        


class MatchingEngine:
    def __init__(self):
        self.orderbook = OrderBook()
        self.tradebook = TradeBook()
    
    def match(self, order):
        """
        :param: order (pd.Series):  Order stored in OrderBook
        """
        filled = 0
        
        if order["dir"] == "buy":
            
            # sort to find relevant securities
            sameAsset = self.orderbook.asks["token_id"] == order["token_id"]
            relAssetOrders = self.orderbook.asks[sameAsset]
            
            # finds ask orders below bid price
            isCheaper = relAssetOrders["price"] <= order["price"]
            askOrders = relAssetOrders[isCheaper]            
            
            # sort to be cheapest at the top
            askOrders = askOrders.sort_values("price", ascending = True)
            
            # iterate until order is filled
            for ask in askOrders.values:
                if filled != order["qty"]:
                
                    # reconstruct easy dtype because fuck me pandas are IMPOSSIBLE
                    askData = {"order_id":ask[0],
                            "token_id":ask[1],
                            "dir": ask[2],
                            "price": ask[3],
                            "qty": ask[4]}
                    
                    # order isn't filled by ask
                    if filled + askData["qty"] <= order["qty"]:
                        filled += askData["qty"]
    
                        # close and remove ask order
                        self.tradebook.add(askData)
                        self.orderbook.remove(askData)
                    
                    # order is overfilled by ask
                    elif filled + askData["qty"] > order["qty"]:
                        print("\n")
                        print("Order filled...")
                        print("\n")
                        # update all figures
                        remainder = order["qty"] - filled                    
                        askData["qty"] -= remainder
                        filled += remainder
                        
                        # close and remove this bid order
                        self.tradebook.add(order)
                        self.orderbook.remove(order)
                        
                        # reduce quantity of unfilled order
                        # not sure if perfect because might override an item with same index ! Check
                        index = self.orderbook.asks[self.orderbook.asks["order_id"] == askData["order_id"]].index.values[0]
                        self.orderbook.asks.loc[index] = askData.values()
                        
                        partialTrade = askData
                        partialTrade["qty"] = remainder
                        self.tradebook.add(partialTrade)
    
                    print("\n")
                    print("Updated Bids/Asks")
                    print(self.orderbook.bids)
                    print(self.orderbook.asks)
                    print("\n")
                    
            # add any remaining unfilled quantity to orderbook
            if filled <= order["qty"]:
                order["qty"] = order.loc["qty"] - filled
                # remove old order
                self.orderbook.remove(order)
                # insert new order, must be in list format
                self.orderbook.add([order])
        
        elif order["dir"] == "sell":
            
            sameAsset = self.orderbook.bids["token_id"] == order["token_id"]
            relAssetOrders = self.orderbook.bids[sameAsset]
            
            isMore = relAssetOrders["price"] >= order["price"]
            bidOrders = relAssetOrders[isMore]            
            
            bidOrders = bidOrders.sort_values("price", ascending = False)
            
            for bid in bidOrders.values:
                if filled != order["qty"]:
                
                    bidData = {"order_id":bid[0],
                            "token_id":bid[1],
                            "dir": bid[2],
                            "price": bid[3],
                            "qty": bid[4]}
                    
                    if filled + bidData["qty"] <= order["qty"]:
                        print("\n")
                        print("Partial Fill...")
                        print("\n")
                        filled += bidData["qty"]
    
                        # close and remove ask order
                        self.tradebook.add(bidData)
                        self.orderbook.remove(bidData)
                    
                    elif filled + bidData["qty"] > order["qty"]:
                        print("\n")
                        print("Order filled...")
                        print("\n")
                        remainder = order["qty"] - filled                    
                        bidData["qty"] -= remainder
                        filled += remainder
                        
                        self.tradebook.add(order)
                        self.orderbook.remove(order)
                        
                        index = self.orderbook.bids[self.orderbook.bids["order_id"] == bidData["order_id"]].index.values[0]
                        self.orderbook.bids.loc[index] = bidData.values()
                        
                        partialTrade = bidData
                        partialTrade["qty"] = remainder
                        self.tradebook.add(partialTrade)
    
                    print("\n")
                    print("Updated Bids/Asks")
                    print(self.orderbook.bids)
                    print(self.orderbook.asks)
                    print("\n")
                    
            # add any remaining unfilled quantity to orderbook
            if filled < order["qty"]:
                order["qty"] = order.loc["qty"] - filled
                # remove old order
                self.orderbook.remove(order)
                # insert new order, must be in list format
                self.orderbook.add([order])
                
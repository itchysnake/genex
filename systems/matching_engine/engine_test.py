import engine
import random

def test_marketOrder():
    token_id = "BDV"
    dir = "buy"
    price = 1.20
    quantity = 100
    
    marketOrder = engine.Order.marketOrder(token_id,
                                           dir,
                                           price,
                                           quantity)
    
    print("Succesfully built marketOrder")
    print(marketOrder)
    return marketOrder
    
def test_orderbookAdd():
    # create order
    order = test_marketOrder()
    
    # add order
    OrderBook = engine.OrderBook()
    OrderBook.add(order)
    
    print("Succesfully added order")
    print(OrderBook.orderbook)
    
    return OrderBook

MatchingEngine = engine.MatchingEngine()
print("Engine Built")

# sample orders
order_list = []

for i in range(50):
    order_id = i
    token_id = "BDV"
    dir_samp = random.randint(1,2)
    if dir_samp == 1:
        dir = "buy"
    elif dir_samp == 2:
        dir = "sell"
    
    price = random.randint(1,15)/10
    qty = random.randint(0,10)
    
    order = {"order_id":order_id,
             "token_id":token_id,
             "dir":dir,
             "price":price,
             "qty":qty}
    
    order_list.append(order)
    
print("Orders Built")

# add orders
MatchingEngine.orderbook.add(order_list)
print("Orders Added")

print("\n")
print("Current Bids/Asks")
print(MatchingEngine.orderbook.bids)
print(MatchingEngine.orderbook.asks)
print("\n")

# matching
_len = len(MatchingEngine.orderbook.bids)
for i in range(_len):
    print("Current Iteration: ",i)
    order = MatchingEngine.orderbook.bids.loc[i]
    print("Order Selected: ",order)
    MatchingEngine.match(order)

print("\n")
print("Final Bids/Asks")
print(MatchingEngine.orderbook.bids)
print(MatchingEngine.orderbook.asks)
print("\n")

print("\n")
print("Trades Completed")
print(MatchingEngine.tradebook.tradebook)
print("\n")
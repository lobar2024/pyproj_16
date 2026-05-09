class EventEmitter:
    def __init__(self):
        self._listeners = {}

    def on(self, event, callback):
        self._listeners.setdefault(event, []).append(callback)

    def off(self, event, callback):
        if event in self._listeners:
            self._listeners[event].remove(callback)

    def emit(self, event, *args, **kwargs):
        for cb in self._listeners.get(event, []):
            cb(*args, **kwargs)

class Shop(EventEmitter):
    def __init__(self):
        super().__init__()
        self._stock = {}

    def add_item(self, item, count):
        self._stock[item] = self._stock.get(item, 0) + count
        self.emit("stock_added", item, count)

    def sell(self, item, count):
        if self._stock.get(item, 0) < count:
            self.emit("out_of_stock", item)
            return
        self._stock[item] -= count
        self.emit("sale", item, count)

if __name__ == "__main__":
    shop = Shop()

    shop.on("sale",          lambda item, n: print(f"  Sotildi: {item} x{n}"))
    shop.on("stock_added",   lambda item, n: print(f"  Keldi  : {item} x{n}"))
    shop.on("out_of_stock",  lambda item:    print(f"  Tugadi : {item}!"))

    shop.add_item("Olma", 10)
    shop.sell("Olma", 3)
    shop.sell("Olma", 9)

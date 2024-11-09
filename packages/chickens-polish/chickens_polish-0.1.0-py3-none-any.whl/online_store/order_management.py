class OrderManager:
    def __init__(self):
        self.orders = dict()

    def create_order(self, order_id, order_data):
        if order_id in self.orders:
            print(f'Заказ с ID {order_id} уже существует')
            return
        self.orders[order_id] = order_data
        print(f'Заказ с ID {order_id} добавлен')

    def update_order(self, order_id, order_data):
        if order_id not in self.orders:
            print(f'Заказ с ID {order_id} не найден')
            return
        for key in order_data:
            self.orders[order_id][key] = order_data[key]
        print(f'Заказ с ID {order_id} обновлён')

    def cancel_order(self, order_id):
        if order_id not in self.orders:
            print(f'Заказ с ID {order_id} не найден')
            return
        del self.orders[order_id]
        print(f'Заказ с ID {order_id} отменён')

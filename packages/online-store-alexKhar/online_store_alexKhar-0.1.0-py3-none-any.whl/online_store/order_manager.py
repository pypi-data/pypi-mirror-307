class OrderManager:
    def __init__(self):
        self.data = {}

    def create_order(self, order_id, order_data):
        if order_id in self.data:
            print(f'Order {order_id} has already been created')
        else:
            self.data[order_id] = order_data

    def update_order(self, order_id, order_data):
        if order_id in self.data:
            self.data[order_id].update(order_data)
            print(f'Client with {order_id} has been updated')
        else:
            print(f'User {order_id} has not been found')

    def cancel_order(self, order_id):
        if order_id in self.data:
            self.data.pop(order_id)
            print(f'Order {order_id} has been deleted')
        else:
            print(f'Order {order_id} did not exist')
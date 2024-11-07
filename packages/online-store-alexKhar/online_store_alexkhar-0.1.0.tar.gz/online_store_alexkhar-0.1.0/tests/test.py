from online_store.user_manager import UserManager
from online_store.order_manager import OrderManager

manager = UserManager()

manager.add_user('user1@example.com', {'name': 'John Doe', 'age': 30})

manager.update_user('user1@example.com', {'age': 31})

print(manager.find_user('user1@example.com'))

manager.remove_user('user1@example.com')

print(manager.find_user('user1@example.com'))



order_manager = OrderManager()

order_manager.create_order('order1001', {'user': 'Alice', 'item': 'Smartphone', 'price': 799})

order_manager.update_order('order1001', {'status': 'shipped'})

order_manager.cancel_order('order1001')
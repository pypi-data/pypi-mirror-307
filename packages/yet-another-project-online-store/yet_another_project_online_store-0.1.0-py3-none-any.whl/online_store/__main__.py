from online_store import UserManager, OrderManager


user_manager = UserManager() # Создай экземпляр класса управления учётными записями клиентов
order_manager = OrderManager() # Создай экземпляр класса управления заказами

def main_menu():
   while True:
       print('\nВыберите действие:')
       print('1. Управление учётными записями')
       print('2. Управление заказами')
       print('3. Выход')

       choice = input('Введите номер действия: ')

       if choice == '1':
           user_menu()
       elif choice == '2':
           order_menu()
       elif choice == '3':
           print('Работа завершена.')
           break
       else:
           print('Некорректный ввод. Попробуйте снова.')

def user_menu():
   print('\nУправление учётными записями клиентов:')
   print('1. Добавить учётную запись')
   print('2. Найти учётную запись')
   print('3. Удалить учётную запись')
   print('4. Назад')

   choice = input('Выберите действие: ')

   if choice == '1':
       user_id = input('Введите email клиента: ')
       name = input('Введите имя: ')
       age = int(input('Введите возраст: '))
       # Вызови метод создания учётной записи клиента
       user_manager.add_user(user_id, {'name': name, 'age': age})
       print(f'Клиент с ID {user_id} добавлен')
   elif choice == '2':
       user_id = input('Введите email клиента: ')
       print(f'{user_manager.find_user(user_id)}')
   elif choice == '3':
       user_id = input('Введите email клиента: ')
       # Вызови метод удаления учётной записи клиента
       user_manager.remove_user(user_id)
       print(f'Клиент с ID {user_id} удалён')
   elif choice == '4':
       return
   else:
       print('Некорректный ввод.')

def order_menu():
   print('\nУправление заказами:')
   print('1. Создать заказ')
   print('2. Обновить заказ')
   print('3. Отменить заказ')
   print('4. Назад')

   choice = input('Выберите действие: ')

   if choice == '1':
       order_id = input('Введите ID заказа: ')
       user = input('Введите учётную запись клиента: ')
       item = input('Введите товар: ')
       price = float(input('Введите цену: '))
       # Вызови метод создания заказа
       order_manager.create_order(order_id, {'user': user, 'item': item, 'price': price})
       print(f'Заказ с ID {order_id} добавлен')
   elif choice == '2':
       order_id = input('Введите ID заказа: ')
       status = input('Введите статус: ')
       # Вызови метод обновления заказа
       order_manager.update_order(order_id, {'status': status})
       print(f'Заказ с ID {order_id} обновлён')
   elif choice == '3':
       order_id = input('Введите ID заказа: ')
       # Вызови метод отмены заказа
       order_manager.cancel_order(order_id)
       print(f'Заказ с ID {order_id} отменён')
   elif choice == '4':
       return
   else:
       print('Некорректный ввод.')

if __name__ == '__main__':
   main_menu()

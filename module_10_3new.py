import threading
import random
from time import sleep

class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):
        for _ in range(100):  # 100 транзакций пополнения
            amount = random.randint(50, 500)
            self.lock.acquire()  # Блокировка для безопасного изменения баланса
            self.balance += amount
            print(f"Пополнение: {amount}. Баланс: {self.balance}")
            # Разблокировка, если баланс больше или равен 500
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            else:
                self.lock.release()  # Разблокируем в любом случае
            sleep(0.001)  # Задержка для симуляции скорости выполнения

    def take(self):
        for _ in range(100):  # 100 транзакций снятия
            amount = random.randint(50, 500)
            print(f"Запрос на {amount}")
            if amount <= self.balance:
                self.lock.acquire()  # Блокировка перед снятием
                self.balance -= amount
                print(f"Снятие: {amount}. Баланс: {self.balance}")
                self.lock.release()
            else:
                print("Запрос отклонён, недостаточно средств")
                self.lock.acquire()  # Блокируем поток

if __name__ == "__main__":
    bk = Bank()

    # Создаём два потока для пополнения и снятия
    th1 = threading.Thread(target=Bank.deposit, args=(bk,))
    th2 = threading.Thread(target=Bank.take, args=(bk,))

    # Запускаем потоки
    th1.start()
    th2.start()

    # Ждём завершения работы потоков
    th1.join()
    th2.join()

    # Итоговый баланс
    print(f"Итоговый баланс: {bk.balance}")
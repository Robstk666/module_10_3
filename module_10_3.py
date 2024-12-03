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
            with self.lock:
                self.balance += amount
                print(f"Пополнение: {amount}. Баланс: {self.balance}")
                # Разблокируем поток, если баланс >= 500
                if self.balance >= 500 and self.lock.locked():
                    self.lock.release()
            sleep(0.001)  # Задержка для симуляции выполнения

    def take(self):
        for _ in range(100):  # 100 транзакций снятия
            amount = random.randint(50, 500)
            print(f"Запрос на {amount}")
            with self.lock:
                if amount <= self.balance:
                    self.balance -= amount
                    print(f"Снятие: {amount}. Баланс: {self.balance}")
                else:
                    print("Запрос отклонён, недостаточно средств")
                    # Блокируем поток, так как недостаточно средств
                    self.lock.acquire()
            sleep(0.001)  # Задержка для симуляции выполнения

# Основной блок программы
if __name__ == "__main__":
    bk = Bank()

    # Создание потоков для методов deposit и take
    th1 = threading.Thread(target=Bank.deposit, args=(bk,))
    th2 = threading.Thread(target=Bank.take, args=(bk,))

    th1.start()
    th2.start()

    th1.join()
    th2.join()

    # Вывод итогового баланса
    print(f"Итоговый баланс: {bk.balance}")
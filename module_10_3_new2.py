import threading
import random
from time import sleep

class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):
        for _ in range(100):
            amount = random.randint(50, 500)
            self.lock.acquire()
            self.balance += amount
            print(f"Пополнение: {amount}. Баланс: {self.balance}")
            # Если баланс >= 500 и замок заблокирован, то разблокировать
            # Здесь lock уже захвачен нами, locked() будет True.
            # По условию: если >=500, то надо разблокировать.
            if self.balance >= 500:
                self.lock.release()
            else:
                self.lock.release()
            sleep(0.001)  # имитация скорости выполнения

    def take(self):
        for _ in range(100):
            amount = random.randint(50, 500)
            print(f"Запрос на {amount}")
            # Без with и без sleep
            # Сначала проверим баланс без блокировки
            if amount <= self.balance:
                # Есть достаточно средств
                self.lock.acquire()
                # Повторная проверка после acquire для корректности
                if amount <= self.balance:
                    self.balance -= amount
                    print(f"Снятие: {amount}. Баланс: {self.balance}")
                # Если вдруг за время ожидания lock баланс изменился, здесь можно было бы проверять ещё раз,
                # но по условию это не оговорено, оставим так.
                self.lock.release()
            else:
                # Недостаточно средств - заблокируем поток
                print("Запрос отклонён, недостаточно средств")
                self.lock.acquire()
                # Поток здесь остаётся заблокированным (acquire без release)

if __name__ == "__main__":
    bk = Bank()

    th1 = threading.Thread(target=bk.deposit)
    th2 = threading.Thread(target=bk.take)

    th1.start()
    th2.start()

    th1.join()
    th2.join()

    print(f"Итоговый баланс: {bk.balance}")
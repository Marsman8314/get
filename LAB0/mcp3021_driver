import time
import io
import fcntl


class MCP3021:
    I2C_SLAVE = 0x0703
    I2C_DEVICE_PATH = "/dev/i2c-1"

    def __init__(self, dynamic_range, address=0x4D, verbose=False):
        self.dynamic_range = dynamic_range
        self.address = address
        self.verbose = verbose
        # Открываем шину I2C напрямую (обход SMBus, который несовместим с MCP3021)
        self.fh = io.open(self.I2C_DEVICE_PATH, "rb", buffering=0)
        fcntl.ioctl(self.fh, self.I2C_SLAVE, self.address)
        time.sleep(0.1)  # небольшая пауза на стабилизацию шины

    def deinit(self):
        try:
            self.fh.close()
        except Exception:
            pass

    def __del__(self):
        try:
            self.deinit()
        except Exception:
            pass

    def get_number(self):
        # MCP3021 отдаёт 2 байта: старшие 4 бита + младшие 6 бит (10-битный результат)
        values = list(self.fh.read(2))
        if len(values) < 2:
            raise RuntimeError("Не удалось прочитать 2 байта с MCP3021")
        number = (values[0] * 256 + values[1]) >> 2  # 10-битное значение
        if self.verbose:
            print(f"Байты: {values}, Число: {number}")
        return number

    def get_voltage(self):
        number = self.get_number()
        voltage = number * self.dynamic_range / (2 ** 10 - 1)
        return voltage


if __name__ == "__main__":
    DYNAMIC_RANGE = 5.0
    adc = MCP3021(dynamic_range=DYNAMIC_RANGE, verbose=True)
    try:
        while True:
            voltage = adc.get_voltage()
            print(f"Напряжение: {voltage:.3f} В")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nЗавершение работы")
    finally:
        adc.deinit()
import time
import adc_plot
from mcp3021_driver import MCP3021

DYNAMIC_RANGE = 5.0
T_ON = 50          # секунд с поданным напряжением
T_OFF = 20         # секунд после отключения
SWITCH_GPIO = 14   # пин, управляющий реле/транзистором (поменяйте под себя)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH_GPIO, GPIO.OUT, initial=GPIO.HIGH)  # HIGH = напряжение подано

adc = MCP3021(dynamic_range=DYNAMIC_RANGE, verbose=False)

voltage_values = []
time_values = []

try:
    start_time = time.time()

    # Фаза 1: напряжение подано (T_ON секунд)
    while time.time() - start_time < T_ON:
        voltage_values.append(adc.get_voltage())
        time_values.append(time.time() - start_time)
        time.sleep(0.01)

    # Отключаем напряжение
    GPIO.output(SWITCH_GPIO, GPIO.LOW)
    t_switch = time.time() - start_time
    print(f"Напряжение отключено на {t_switch:.2f} с")

    # Фаза 2: напряжение отключено (T_OFF секунд)
    while time.time() - start_time < T_ON + T_OFF:
        voltage_values.append(adc.get_voltage())
        time_values.append(time.time() - start_time)
        time.sleep(0.01)

    adc_plot.plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)
    adc_plot.plot_sampling_period_hist(time_values)

finally:
    adc.deinit()
    GPIO.output(SWITCH_GPIO, GPIO.LOW)
    GPIO.cleanup()
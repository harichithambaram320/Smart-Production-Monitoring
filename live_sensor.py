import csv
import random
import time
from datetime import datetime
import os


MACHINES = [
    "Machine-01",
    "Machine-02",
    "Machine-03",
    "Machine-04",
    "Machine-05"
]

FILE_PATH = "data/sensor_data.csv"


def generate_reading(machine):

    machine_state = random.choices(
        ["Normal", "Warning", "Critical"],
        weights=[75, 15, 10]
    )[0]

    if machine_state == "Critical":

        temperature = round(random.normalvariate(85, 5), 2)
        vibration = round(random.normalvariate(4.5, 0.6), 2)
        pressure = round(random.normalvariate(7.0, 0.7), 2)

        production_count = random.randint(40, 90)
        error_count = random.randint(4, 10)

    elif machine_state == "Warning":

        temperature = round(random.normalvariate(75, 4), 2)
        vibration = round(random.normalvariate(3.5, 0.5), 2)
        pressure = round(random.normalvariate(6.2, 0.6), 2)

        production_count = random.randint(60, 120)
        error_count = random.randint(2, 6)

    else:

        temperature = round(random.normalvariate(65, 5), 2)
        vibration = round(random.normalvariate(2.5, 0.4), 2)
        pressure = round(random.normalvariate(5.5, 0.5), 2)

        production_count = random.randint(80, 160)
        error_count = random.randint(0, 3)

    return [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        machine,
        temperature,
        vibration,
        pressure,
        production_count,
        error_count,
        machine_state
    ]


def add_readings():

    file_exists = os.path.exists(FILE_PATH)

    with open(FILE_PATH, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "timestamp",
                "machine",
                "temperature",
                "vibration",
                "pressure",
                "production_count",
                "error_count",
                "machine_condition"
            ])

        for machine in MACHINES:

            reading = generate_reading(machine)

            writer.writerow(reading)

            print(
                f"{reading[0]} | "
                f"{reading[1]} | "
                f"{reading[2]}°C | "
                f"{reading[7]}"
            )


if __name__ == "__main__":

    print("Live sensor simulator started...")
    print("Generating new readings every 10 seconds.")
    print("Press Ctrl+C to stop.\n")

    while True:

        add_readings()

        print("\nWaiting 60 seconds...\n")

        time.sleep(60)
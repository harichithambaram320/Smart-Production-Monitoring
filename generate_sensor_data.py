import csv
import random
from datetime import datetime, timedelta


MACHINES = [
    "Machine-01",
    "Machine-02",
    "Machine-03",
    "Machine-04",
    "Machine-05"
]


def generate_sensor_data(rows=500):

    start_time = datetime.now() - timedelta(hours=24)

    data = []

    for i in range(rows):

        timestamp = start_time + timedelta(minutes=3 * i)

        machine = random.choice(MACHINES)

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

        data.append([
            timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            machine,
            temperature,
            vibration,
            pressure,
            production_count,
            error_count,
            machine_state
        ])

    return data


def save_data(data):

    filename = "data/sensor_data.csv"

    with open(filename, "w", newline="") as file:

        writer = csv.writer(file)

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

        writer.writerows(data)


if __name__ == "__main__":

    sensor_data = generate_sensor_data()

    save_data(sensor_data)

    print("Sensor data generated successfully.")
    print(f"Total records: {len(sensor_data)}")
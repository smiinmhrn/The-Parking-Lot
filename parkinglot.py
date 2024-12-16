import threading
from datetime import datetime
import time
import random

#this function is return a deictionary including the number of floors, spots and cars that user wanted
def get_inputs():
    return {
        "floors": int(input("Enter the number of floors: ")),
        "spots_per_floor": int(input("Enter the number of spots per floor: ")),
        "num_cars": int(input("Enter the number of cars:"))
    }

#this function is crating semaphores for each floors and spots and a lock for printing
def initialize_parking_lot(floors, spots_per_floor):
    return {
        "spots_each_floor": [[threading.Semaphore(1) for _ in range(spots_per_floor)] for _ in range(floors)],
        "floor_capacity": [threading.Semaphore(spots_per_floor) for _ in range(floors)],
        "parking_capacity": threading.Semaphore(floors * spots_per_floor),
        "lock": threading.Lock()
    }

#for log the time in console
def log(message, lock):
    with lock:
        print(f"{datetime.now().strftime('%H:%M:%S')} - {message}")

#controls the parking
def park_cars(car_id, parking):

    log(f"Car {car_id} is trying to enter the parking lot.", parking["lock"])
    parking["parking_capacity"].acquire()

    for floor_index, floor_semaphore in enumerate(parking["floor_capacity"]):
        if floor_semaphore.acquire(blocking=False):
            for spot_index, spot_semaphore in enumerate(parking["spots_each_floor"][floor_index]):
                if spot_semaphore.acquire(blocking=False):

                    log(f"Car {car_id} is parking in spot {spot_index} on floor {floor_index}.", parking["lock"])
                    time.sleep(1)  # Simulate parking time
                    park_time = random.randint(1, 5)
                    log(f"Car {car_id} has parked in spot {spot_index} on floor {floor_index}.", parking["lock"])
                    log(f"Car {car_id} is parked for {park_time} seconds.", parking["lock"])
                    time.sleep(park_time)

                    log(f"Car {car_id} is leaving the spot {spot_index} on floor {floor_index}.", parking["lock"])
                    time.sleep(1)  # Simulate leaving time
                    spot_semaphore.release()
                    floor_semaphore.release()

                    time.sleep(floor_index)
                    parking["parking_capacity"].release()
                    log(f"Car {car_id} has left the parking lot.", parking["lock"])

                    return
        else:
            log(f"Car {car_id} could not find a valid spot on floor {floor_index}.", parking["lock"])
            log(f"Car {car_id} is moving to floor {floor_index + 1}.", parking["lock"])
            time.sleep(1)

#for running the programe
def main():
    user_inputs = get_inputs()
    print() #printing a space for seprating
    parking = initialize_parking_lot(user_inputs["floors"], user_inputs["spots_per_floor"])
    
    car_threads = []

    for car_id in range(user_inputs["num_cars"]):
        car_thread = threading.Thread(target=park_cars, args=(car_id + 1, parking))
        car_threads.append(car_thread)
        car_thread.start()

    for car_thread in car_threads:
        car_thread.join()

main()
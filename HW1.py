import numpy as np 
import heapq

class Event:
    def __init__(self, time, event_type, passenger_id=None):
        self.time = time
        self.event_type = event_type
        self.passenger_id = passenger_id

    def __lt__(self, other):
        return self.time < other.time

class Passenger:
    def __init__(self, id):
        self.id = id

# Function to generate arrival time for passengers
def generate_arrival_time():
    return np.random.uniform(3, 7)  # Uniform distribution: 2 to 5 minutes

# Function to generate inspection time for passengers
def generate_inspection_time():
    return np.random.exponential(10)  # Exponential distribution with mean 10 minutes

# Main simulation function
def simulate():
    # Initialize future event list (FEL), queue, denied passengers set, and other variables
    fel = []  # FEL (future event list) to hold events
    passengers_queue = []  # Queue to hold passengers awaiting inspection
    denied_passengers = set()  # Set to hold passengers denied entry
    total_queue_length = 0  # Total length of queue over time
    max_queue_length = 0  # Maximum length of queue observed
    current_time = 0  # Current simulation time
    next_passenger_id = 1  # ID for the next passenger
    total_passengers = 0  # Total number of passengers that have arrived
    fel_changed = True  # Flag to indicate if FEL has changed

    # File to save simulation output
    output_file = open("simulation_output.txt", "w+")

    # Initializing simulation
    output_file.write(f"t={int(current_time)}: system initialized.\n")
    fel_changed = True

    # Schedule the first arrival event
    first_arrival_time = generate_arrival_time()
    heapq.heappush(fel, Event(current_time + first_arrival_time, "arrival", next_passenger_id))
    output_file.write(f"initial arrival event generated and scheduled for t={int(first_arrival_time)}\n")
    fel_changed = True

    # Main simulation loop
    while total_passengers < 2000 and len(denied_passengers) < 100:  # Continue until 2000 passengers or 100 denied
        # Get the next event from the FEL
        event = heapq.heappop(fel)
        current_time = event.time  # Update current time to event time

        # Process the event based on its type
        if event.event_type == "arrival":
            output_file.write(f"\nt={int(current_time)}: passenger {event.passenger_id} arrived for inspection.\n")
            total_passengers += 1
            # Create a new Passenger object for the arrived passenger
            passenger = Passenger(event.passenger_id)
            # Add the passenger to the queue
            passengers_queue.append(passenger)
            output_file.write("inspection starts\n")
            output_file.write(f"queue length={len(passengers_queue)}\n")
            # Update total queue length and max queue length
            total_queue_length += len(passengers_queue)
            max_queue_length = max(max_queue_length, len(passengers_queue))
            # Schedule inspection start for the passenger
            inspection_time = generate_inspection_time()
            heapq.heappush(fel, Event(current_time + inspection_time, "inspection_start", passenger.id))
            # Schedule next arrival event
            next_passenger_id += 1
            next_arrival_time = current_time + generate_arrival_time()
            heapq.heappush(fel, Event(next_arrival_time, "arrival", next_passenger_id))
            output_file.write(f"new arrival generated and scheduled for t={int(next_arrival_time)}\n")
            fel_changed = True

        elif event.event_type == "inspection_start":
            output_file.write(f"t={int(current_time)}: inspection completed for passenger {event.passenger_id}.\n")
            # Get the ID of the passenger being inspected
            passenger_id = event.passenger_id
            # Remove the passenger from the queue
            passengers_queue.pop(0)
            output_file.write(f"queue length={len(passengers_queue)}\n")
            # Update total queue length and max queue length
            total_queue_length += len(passengers_queue)
            max_queue_length = max(max_queue_length, len(passengers_queue))
            # Simulate inspection outcome for the passenger
            if np.random.rand() < 0.05:  # 5% chance of failing inspection
                output_file.write(f"passenger inspection failed (failed no. {passenger_id})\n")
                denied_passengers.add(passenger_id)
            else:
                output_file.write(f"passenger inspection passed (passed no. {passenger_id})\n")
            fel_changed = True

        # Print FEL contents if it has changed
        if fel_changed:
            fel_contents = [f"{int(e.time)}" for e in fel]
            output_file.write(f"t={int(current_time)}: FEL contents: [{', '.join(fel_contents)}]\n")
            fel_changed = False

    # Simulation completed, print simulation report
    output_file.write("\n--- Simulation Report ---\n")
    output_file.write(f"Total simulation time: {int(current_time)} minutes\n")
    output_file.write(f"Average length of queue: {total_queue_length / current_time if current_time != 0 else 0}\n")
    output_file.write(f"Maximum length of queue: {max_queue_length}\n")
    output_file.write(f"Number of passengers denied entry: {len(denied_passengers)}\n")
    output_file.write(f"Denied passengers list: {list(denied_passengers)}\n")

    # Close the file after writing
    output_file.close()

# Run the simulation
simulate()

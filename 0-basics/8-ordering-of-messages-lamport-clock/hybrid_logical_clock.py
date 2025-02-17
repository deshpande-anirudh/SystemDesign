from datetime import datetime


def current_system_time_in_milliseconds():
    return datetime.now().timestamp()


def get_physical_time():
    return int(datetime.utcnow().timestamp()) * 1000

class HLC:
    def __init__(self):
        self.T = get_physical_time()  # Wall clock time
        self.C = 0  # Logical counter

    def get_physical_time(self):
        return current_system_time_in_milliseconds()  # Assume monotonic clock

    def generate_event(self):
        """ Called when the local system generates a new event """
        new_T = max(self.T, get_physical_time())
        if new_T > self.T:  # If the physical clock moves forward
            self.C = 0  # Reset counter
        else:  # If same timestamp, increment counter
            self.C += 1
        self.T = new_T
        return (self.T, self.C)

    def receive_event(self, T_recv, C_recv):
        """ Called when receiving an event with HLC (T_recv, C_recv) """
        new_T = max(self.T, T_recv, get_physical_time())

        if new_T == self.T and new_T == T_recv:
            self.C = max(self.C, C_recv) + 1  # If timestamps match, increment counter
        elif new_T == self.T:
            self.C += 1  # If only local time is the max, just increment counter
        else:
            self.C = 0  # If new_T is from physical clock, reset counter

        self.T = new_T
        return (self.T, self.C)  # Updated HLC timestamp


hlc = HLC()
print("Generate events ==> Ordered by (timestamp, counter)")
for i in range(5):
    time, count = hlc.generate_event()
    print(f"event {i}, timestamp {time}, counter {count}")


print("\nReception of events, I'm ahead ==> Ordered by (timestamp, counter)")
time, count = hlc.receive_event(1739747436000, 0)
print(f"After receiving, timestamp {time}, counter {count}")

print("\nReception of events, I'm behind ==> Ordered by (timestamp, counter)")
time, count = hlc.receive_event(1839747436000, 0)
print(f"After receiving, timestamp {time}, counter {count}")

import time
from redlock import RedLock

# Initialize Redlock with Redis nodes
lock_manager = RedLock([
    {"host": "localhost", "port": 6379, "db": 0},
])

# Constants
LOCK_TTL_MILLISECONDS = 600000  # 10 minutes (in milliseconds)
TICKET_TABLE = {}  # Simulate ticket DB: {ticket_id: "AVAILABLE" or "BOOKED"}


def reserve_ticket(ticket_id, user_id):
    lock_key = f"ticket:{ticket_id}"

    # Acquire lock with TTL
    lock = lock_manager.lock(lock_key, LOCK_TTL_MILLISECONDS)

    if lock:
        print(f"Ticket {ticket_id} reserved for User {user_id}. Complete payment within 10 minutes.")
        return lock
    else:
        print(f"Ticket {ticket_id} is already reserved.")
        return None


def complete_booking(ticket_id, user_id, lock):
    lock_key = f"ticket:{ticket_id}"

    # Ensure lock is still valid and active
    if lock and lock_manager.valid(lock):
        # Update DB state
        TICKET_TABLE[ticket_id] = "BOOKED"

        # Release the lock
        lock_manager.unlock(lock)
        print(f"Ticket {ticket_id} successfully booked by User {user_id}.")
    else:
        print(f"Booking failed. Ticket {ticket_id} not reserved or lock expired.")


def simulate_payment_flow(ticket_id, user_id):
    lock = reserve_ticket(ticket_id, user_id)
    if lock:
        print("Simulating payment process...")
        time.sleep(5)  # Simulate payment latency
        complete_booking(ticket_id, user_id, lock)
    else:
        print("Couldn't reserve ticket. Try again later.")


# Example Usage
TICKET_TABLE[1] = "AVAILABLE"  # Ticket initialization

simulate_payment_flow(1, "user123")  # Successful reservation and booking
simulate_payment_flow(1, "user456")  # Should fail as ticket is already booked

"""
Set 3 - Hospital Appointment Desk
"""

import csv
import random
import time
from collections import deque
from datetime import datetime
from pathlib import Path
from bisect import bisect_right


# ---------------------------------------------------------------------------
# Configuration and CSV Loading
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "records.csv"

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

URGENCY_PRIORITY = {
    "Critical": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4
}


def load_records(file_path):

    records = []

    with file_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        required_columns = {
            "patientId",
            "patientName",
            "doctorId",
            "specialty",
            "urgencyLevel",
            "arrivalTime",
            "slotStart",
            "slotEnd",
            "durationMinutes"
        }

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError("CSV is missing one or more required columns.")

        for row in reader:
            records.append({
                "patientId": row["patientId"],
                "patientName": row["patientName"],
                "doctorId": row["doctorId"],
                "specialty": row["specialty"],
                "urgencyLevel": row["urgencyLevel"],
                "arrivalTime": datetime.strptime(
                    row["arrivalTime"], DATE_FORMAT
                ),
                "slotStart": datetime.strptime(
                    row["slotStart"], DATE_FORMAT
                ),
                "slotEnd": datetime.strptime(
                    row["slotEnd"], DATE_FORMAT
                ),
                "durationMinutes": int(row["durationMinutes"])
            })

    return records


# ---------------------------------------------------------------------------
# Task 1 - Linear Search and Binary Search
# ---------------------------------------------------------------------------

def linear_search(records, target_patient_id):

    for record in records:
        if record["patientId"] == target_patient_id:
            return record

    return None


def binary_search(sorted_records, target_patient_id):

    low = 0
    high = len(sorted_records) - 1

    while low <= high:

        middle = (low + high) // 2
        current_id = sorted_records[middle]["patientId"]

        if current_id == target_patient_id:
            return sorted_records[middle]

        if current_id < target_patient_id:
            low = middle + 1

        else:
            high = middle - 1

    return None


def task_1(records):

    print("\n" + "=" * 72)
    print("TASK 1 - LINEAR SEARCH VS BINARY SEARCH")
    print("=" * 72)

    # Extract unique patient records for searching.
    patient_map = {}

    for record in records:
        patient_map[record["patientId"]] = record

    unique_patients = list(patient_map.values())

    sorted_patients = sorted(
        unique_patients,
        key=lambda record: record["patientId"]
    )

    patient_count = len(sorted_patients)

    # Select 1,000 patient IDs for lookup benchmarking.
    random.seed(42)

    sample_size = min(1000, patient_count)

    target_ids = random.sample(
        [record["patientId"] for record in sorted_patients],
        sample_size
    )

    print(f"Unique Patient Records: {patient_count:,}")
    print(f"Lookup Operations      : {sample_size:,}")

    # Linear Search Benchmark.
    start = time.perf_counter()

    for target_id in target_ids:
        linear_search(unique_patients, target_id)

    linear_time = time.perf_counter() - start

    # Binary Search Benchmark.
    start = time.perf_counter()

    for target_id in target_ids:
        binary_search(sorted_patients, target_id)

    binary_time = time.perf_counter() - start

    print("\nExecution Time for 1,000 Lookups:")
    print(f"Linear Search : {linear_time:.6f} seconds")
    print(f"Binary Search : {binary_time:.6f} seconds")

    print("\nComplexity:")
    print("- Linear Search: O(n) average/worst-case.")
    print("- Binary Search: O(log n) average/worst-case.")
    print("- Both have O(1) best-case complexity.")
    print("- Binary Search requires sorted data.")

    # Demonstrate both algorithms.
    target = target_ids[0]

    linear_result = linear_search(unique_patients, target)
    binary_result = binary_search(sorted_patients, target)

    print("\nSample Lookup:")
    print("Patient ID:", target)
    print("Linear Search Found:", linear_result is not None)
    print("Binary Search Found:", binary_result is not None)


# ---------------------------------------------------------------------------
# Task 2 - Selection Sort and Quick Sort
# ---------------------------------------------------------------------------

def sort_key(record):

    return (
        URGENCY_PRIORITY[record["urgencyLevel"]],
        record["arrivalTime"]
    )


def selection_sort(records):

    result = records.copy()

    n = len(result)
    swaps = 0

    for i in range(n - 1):

        minimum_index = i

        for j in range(i + 1, n):

            if (
                sort_key(result[j])
                < sort_key(result[minimum_index])
            ):
                minimum_index = j

        if minimum_index != i:

            result[i], result[minimum_index] = (
                result[minimum_index],
                result[i]
            )

            swaps += 1

    return result, swaps


def quick_sort(records):

    result = records.copy()
    swaps = 0

    def partition(low, high):

        nonlocal swaps

        pivot = sort_key(result[high])

        i = low - 1

        for j in range(low, high):

            if sort_key(result[j]) <= pivot:

                i += 1

                if i != j:

                    result[i], result[j] = (
                        result[j],
                        result[i]
                    )

                    swaps += 1

        if i + 1 != high:

            result[i + 1], result[high] = (
                result[high],
                result[i + 1]
            )

            swaps += 1

        return i + 1

    def sort(low, high):

        if low < high:

            pivot_index = partition(low, high)

            sort(low, pivot_index - 1)
            sort(pivot_index + 1, high)

    sort(0, len(result) - 1)

    return result, swaps


def task_2(records):

    print("\n" + "=" * 72)
    print("TASK 2 - SELECTION SORT VS QUICK SORT")
    print("=" * 72)

    print(f"Total Appointments: {len(records):,}")

    print("\nSorting criteria:")
    print("1. Urgency: Critical > High > Medium > Low")
    print("2. Arrival Time: Earlier arrival first")

    # Selection Sort Benchmark.
    start = time.perf_counter()

    selection_result, selection_swaps = selection_sort(records)

    selection_time = time.perf_counter() - start

    # Quick Sort Benchmark.
    start = time.perf_counter()

    quick_result, quick_swaps = quick_sort(records)

    quick_time = time.perf_counter() - start

    print("\nSorting Results:")
    print(f"Selection Sort Time  : {selection_time:.6f} seconds")
    print(f"Selection Sort Swaps : {selection_swaps:,}")

    print(f"\nQuick Sort Time      : {quick_time:.6f} seconds")
    print(f"Quick Sort Swaps     : {quick_swaps:,}")

    print("\nCorrectness Checks:")

    selection_keys = [
        sort_key(record)
        for record in selection_result
    ]

    quick_keys = [
        sort_key(record)
        for record in quick_result
    ]

    print(
        "Selection Sort Correct:",
        all(
            selection_keys[i] <= selection_keys[i + 1]
            for i in range(len(selection_keys) - 1)
        )
    )

    print(
        "Quick Sort Correct:",
        all(
            quick_keys[i] <= quick_keys[i + 1]
            for i in range(len(quick_keys) - 1)
        )
    )

    print(
        "Both Algorithms Agree:",
        selection_keys == quick_keys
    )

    print("\nFirst 10 Appointments:")

    for record in quick_result[:10]:

        print(
            f'{record["patientId"]} | '
            f'{record["urgencyLevel"]:8} | '
            f'{record["arrivalTime"]} | '
            f'{record["doctorId"]}'
        )

    print("\nComplexity:")
    print("- Selection Sort: O(n^2) time and O(1) auxiliary space.")
    print("- Quick Sort: O(n log n) average, O(n^2) worst-case.")
    print("- Quick Sort uses O(log n) average recursion space.")
    print("- Selection Sort performs at most O(n) swaps.")
    print("- Quick Sort is generally faster for larger datasets.")

    print("\nStability:")
    print("- Selection Sort is generally not stable.")
    print("- This Quick Sort implementation is not stable.")
    print("- Equal urgency and arrival-time records may change relative order.")


# ---------------------------------------------------------------------------
# Task 3 - Detect Double-Booked Appointment Slots
# ---------------------------------------------------------------------------

def find_double_bookings(records):

    booking_map = {}

    for record in records:

        key = (
            record["patientId"],
            record["slotStart"]
        )

        if key not in booking_map:
            booking_map[key] = []

        booking_map[key].append(record)

    duplicates = []

    for key, matching_records in booking_map.items():

        if len(matching_records) > 1:
            duplicates.append((key, matching_records))

    return duplicates


def task_3(records):

    print("\n" + "=" * 72)
    print("TASK 3 - DOUBLE-BOOKED APPOINTMENT DETECTION")
    print("=" * 72)

    duplicates = find_double_bookings(records)

    duplicate_count = sum(
        len(group)
        for _, group in duplicates
    )

    print(f"Double-Booked Slots Found : {len(duplicates):,}")
    print(f"Records Involved          : {duplicate_count:,}")

    print("\nFirst 5 Double-Booked Slots:")

    for key, group in duplicates[:5]:

        patient_id, slot_start = key

        print(f"\nPatient ID : {patient_id}")
        print(f"Slot Start : {slot_start}")

        for record in group:

            print(
                f'  Doctor: {record["doctorId"]}, '
                f'Specialty: {record["specialty"]}'
            )

    print("\nData Structure:")
    print("- Dictionary (Hash Table).")

    print("\nComplexity:")
    print("- Average Time: O(n).")
    print("- Space: O(n).")

    print("\nWhy not a List Scan?")
    print("- A list scan can require O(n) for each new booking.")
    print("- Processing n bookings this way can take O(n^2) time.")
    print("- Hashing provides approximately O(1) average lookup.")
    print("- This makes duplicate detection more efficient at scale.")


# ---------------------------------------------------------------------------
# Task 4 - Custom Queue and Stack
# ---------------------------------------------------------------------------

class Queue:

    def __init__(self):

        self.items = []
        self.front = 0

    def enqueue(self, patient):

        self.items.append(patient)

    def dequeue(self):

        if self.is_empty():
            raise IndexError("Walk-in queue is empty.")

        patient = self.items[self.front]

        self.front += 1

        # Periodically discard consumed entries.
        if self.front > 50 and self.front * 2 >= len(self.items):

            self.items = self.items[self.front:]
            self.front = 0

        return patient

    def is_empty(self):

        return self.front >= len(self.items)

    def size(self):

        return len(self.items) - self.front


class Stack:

    def __init__(self):

        self.items = []

    def push(self, patient):

        self.items.append(patient)

    def pop(self):

        if self.is_empty():
            raise IndexError("Patient history is empty.")

        return self.items.pop()

    def peek(self):

        if self.is_empty():
            raise IndexError("Patient history is empty.")

        return self.items[-1]

    def is_empty(self):

        return len(self.items) == 0

    def size(self):

        return len(self.items)


def task_4(records):

    print("\n" + "=" * 72)
    print("TASK 4 - WALK-IN QUEUE AND RECENT PATIENTS STACK")
    print("=" * 72)

    # Custom Queue Demonstration.
    walk_in_queue = Queue()

    for record in records[:5]:

        walk_in_queue.enqueue(record["patientId"])

    print("Custom Queue - Initial Size:", walk_in_queue.size())

    print("\nWalk-In Token Processing:")

    while not walk_in_queue.is_empty():

        print("Now Serving:", walk_in_queue.dequeue())

    # Custom Stack Demonstration.
    recent_patients = Stack()

    for record in records[:5]:

        recent_patients.push(record["patientId"])

    print("\nRecent Patients History:")

    print("Most Recently Viewed:", recent_patients.peek())

    print("Removing Last Viewed Patient:", recent_patients.pop())

    print("Remaining History Size:", recent_patients.size())

    # Built-in Queue Equivalent.
    builtin_queue = deque()

    builtin_queue.extend([
        "PATIENT-1",
        "PATIENT-2",
        "PATIENT-3"
    ])

    print("\nBuilt-in Queue (collections.deque):")

    while builtin_queue:

        print("Now Serving:", builtin_queue.popleft())

    # Built-in Stack Equivalent.
    builtin_stack = []

    builtin_stack.extend([
        "PATIENT-1",
        "PATIENT-2",
        "PATIENT-3"
    ])

    print("\nBuilt-in Stack (list):")

    print("Most Recently Viewed:", builtin_stack.pop())

    print("\nComplexity:")
    print("- Queue Enqueue: O(1) amortized.")
    print("- Queue Dequeue: O(1) amortized.")
    print("- Stack Push: O(1) amortized.")
    print("- Stack Pop: O(1) amortized.")
    print("- deque is efficient for FIFO operations.")
    print("- list is suitable for LIFO operations.")


# ---------------------------------------------------------------------------
# Task 5 - Dynamic Programming vs Greedy Appointment Scheduling
# ---------------------------------------------------------------------------

def prepare_appointments(records):

    doctor_appointments = {}

    for record in records:

        doctor_id = record["doctorId"]

        if doctor_id not in doctor_appointments:
            doctor_appointments[doctor_id] = []

        doctor_appointments[doctor_id].append(record)

    selected_doctor = max(
        doctor_appointments,
        key=lambda doctor: len(doctor_appointments[doctor])
    )

    appointments = doctor_appointments[selected_doctor]

    appointments.sort(
        key=lambda record: (
            record["slotEnd"],
            record["slotStart"]
        )
    )

    return selected_doctor, appointments


def dp_scheduling(appointments):

    n = len(appointments)

    if n == 0:
        return 0, []

    # Extract sorted finishing times.
    finish_times = [
        appointment["slotEnd"]
        for appointment in appointments
    ]

    # predecessor[i] = number of appointments ending before
    # appointment i starts.
    predecessor = []

    for i in range(n):

        compatible_count = bisect_right(
            finish_times,
            appointments[i]["slotStart"],
            0,
            i
        )

        predecessor.append(compatible_count)

    # Dynamic Programming Table.
    dp = [0] * (n + 1)

    for i in range(1, n + 1):

        include = 1 + dp[predecessor[i - 1]]
        exclude = dp[i - 1]

        dp[i] = max(include, exclude)

    # Reconstruct the selected appointment schedule.
    selected = []

    i = n

    while i > 0:

        include = 1 + dp[predecessor[i - 1]]
        exclude = dp[i - 1]

        if include > exclude:

            selected.append(appointments[i - 1])

            i = predecessor[i - 1]

        else:

            i -= 1

    selected.reverse()

    return dp[n], selected


def greedy_scheduling(appointments):

    sorted_appointments = sorted(
        appointments,
        key=lambda record: (
            record["slotEnd"],
            record["slotStart"]
        )
    )

    selected = []
    last_finish_time = None

    for appointment in sorted_appointments:

        if (
            last_finish_time is None
            or appointment["slotStart"] >= last_finish_time
        ):

            selected.append(appointment)
            last_finish_time = appointment["slotEnd"]

    return len(selected), selected


def task_5(records):

    print("\n" + "=" * 72)
    print("TASK 5 - DYNAMIC PROGRAMMING VS GREEDY SCHEDULING")
    print("=" * 72)

    doctor_id, appointments = prepare_appointments(records)

    print(f"Selected Doctor       : {doctor_id}")
    print(f"Total Appointments    : {len(appointments):,}")

    # Dynamic Programming.
    start = time.perf_counter()

    dp_count, dp_schedule = dp_scheduling(appointments)

    dp_time = time.perf_counter() - start

    # Greedy.
    start = time.perf_counter()

    greedy_count, greedy_schedule = greedy_scheduling(
        appointments
    )

    greedy_time = time.perf_counter() - start

    print("\nDynamic Programming:")
    print(f"Maximum Appointments : {dp_count}")
    print(f"Execution Time       : {dp_time:.6f} seconds")

    print("\nGreedy Algorithm:")
    print(f"Maximum Appointments : {greedy_count}")
    print(f"Execution Time       : {greedy_time:.6f} seconds")

    print("\nComparison:")
    print("Both algorithms agree:", dp_count == greedy_count)

    print("\nSelected Appointments (Dynamic Programming):")

    for appointment in dp_schedule[:10]:

        print(
            f'{appointment["patientId"]} | '
            f'{appointment["slotStart"].strftime("%H:%M")} - '
            f'{appointment["slotEnd"].strftime("%H:%M")} | '
            f'{appointment["durationMinutes"]} minutes'
        )

    print("\nComplexity:")
    print("- DP: O(n log n) time due to sorting and predecessor lookup.")
    print("- DP table: O(n) space.")
    print("- Greedy: O(n log n) time due to sorting.")
    print("- Greedy selection after sorting: O(n).")

    print("\nExplanation:")
    print("- Dynamic Programming considers both include and exclude choices.")
    print("- Greedy always selects the compatible appointment finishing earliest.")
    print("- For unweighted interval scheduling, earliest-finish-time Greedy")
    print("  is optimal, so both methods should find the same maximum count.")
    print("- Different appointment durations do not invalidate this property.")


# ---------------------------------------------------------------------------
# Main Program
# ---------------------------------------------------------------------------

if not CSV_FILE.exists():

    raise FileNotFoundError(
        f"Could not find {CSV_FILE.name}. "
        "Place records.csv in the same folder as code_file.py."
    )

records = load_records(CSV_FILE)

print("=" * 72)
print("HOSPITAL APPOINTMENT DESK")
print("=" * 72)

print(f"Loaded {len(records):,} appointment records.")

unique_patient_ids = {
    record["patientId"]
    for record in records
}

print(f"Unique Patients: {len(unique_patient_ids):,}")

task_1(records)
task_2(records)
task_3(records)
task_4(records)
task_5(records)
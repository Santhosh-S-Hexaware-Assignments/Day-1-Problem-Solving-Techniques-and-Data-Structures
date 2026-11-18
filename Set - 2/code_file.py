"""
Set 2 - Retail Banking Transaction Review
"""

import csv
import random
import time
from collections import Counter, deque
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration and CSV Loading
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "transactions.csv"

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def load_transactions(file_path):

    transactions = []

    with file_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        required_columns = {
            "transactionId",
            "accountId",
            "amount",
            "merchant",
            "postingDate"
        }

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError("CSV is missing one or more required columns.")

        for row in reader:
            transactions.append({
                "transactionId": row["transactionId"],
                "accountId": row["accountId"],
                "amount": float(row["amount"]),
                "merchant": row["merchant"],
                "postingDate": datetime.strptime(
                    row["postingDate"], DATE_FORMAT
                )
            })

    return transactions


# ---------------------------------------------------------------------------
# Task 1 - Binary Search and Linear Search
# ---------------------------------------------------------------------------

def binary_search(transaction_ids, target):

    low = 0
    high = len(transaction_ids) - 1
    comparisons = 0

    while low <= high:
        middle = (low + high) // 2
        comparisons += 1

        if transaction_ids[middle] == target:
            return middle, comparisons

        if transaction_ids[middle] < target:
            low = middle + 1
        else:
            high = middle - 1

    return -1, comparisons


def linear_search(transaction_ids, target):

    comparisons = 0

    for index, transaction_id in enumerate(transaction_ids):
        comparisons += 1

        if transaction_id == target:
            return index, comparisons

    return -1, comparisons


def task_1(transactions):

    print("\n" + "=" * 72)
    print("TASK 1 - BINARY SEARCH VS LINEAR SEARCH")
    print("=" * 72)

    transaction_ids = sorted(
        transaction["transactionId"]
        for transaction in transactions
    )

    n = len(transaction_ids)

    # Best case: target is at the middle.
    best_target = transaction_ids[n // 2]

    _, best_comparisons = binary_search(
        transaction_ids, best_target
    )

    # Worst case: an ID that does not exist.
    worst_target = "TXN99999999"

    _, worst_comparisons = binary_search(
        transaction_ids, worst_target
    )

    # Average case: test 1,000 randomly selected existing IDs.
    random.seed(42)

    sample_targets = random.sample(
        transaction_ids, min(1000, n)
    )

    total_comparisons = 0

    for target in sample_targets:
        _, comparisons = binary_search(transaction_ids, target)
        total_comparisons += comparisons

    average_comparisons = total_comparisons / len(sample_targets)

    print(f"Total transaction IDs: {n:,}")

    print("\nBinary Search Comparisons:")
    print(f"Best case    : {best_comparisons}")
    print(f"Average case : {average_comparisons:.2f}")
    print(f"Worst case   : {worst_comparisons}")

    # Compare with linear search.
    print("\nLinear Search Comparison:")

    best_linear_target = transaction_ids[0]
    worst_linear_target = transaction_ids[-1]

    _, linear_best = linear_search(
        transaction_ids, best_linear_target
    )

    _, linear_worst = linear_search(
        transaction_ids, worst_linear_target
    )

    total_linear_comparisons = 0

    for target in sample_targets:
        _, comparisons = linear_search(transaction_ids, target)
        total_linear_comparisons += comparisons

    linear_average = (
        total_linear_comparisons / len(sample_targets)
    )

    print(f"Best case    : {linear_best}")
    print(f"Average case : {linear_average:.2f}")
    print(f"Worst case   : {linear_worst}")

    print("\nComplexity:")
    print("- Binary Search: O(1) best, O(log n) average/worst.")
    print("- Linear Search: O(1) best, O(n) average/worst.")
    print("- Binary Search requires sorted input.")

    # Timing comparison for one existing target.
    target = transaction_ids[-1]

    start = time.time()
    linear_search(transaction_ids, target)
    linear_time = time.time() - start

    start = time.time()
    binary_search(transaction_ids, target)
    binary_time = time.time() - start

    print("\nExecution time:")
    print(f"Linear Search : {linear_time:.8f} seconds")
    print(f"Binary Search : {binary_time:.8f} seconds")


# ---------------------------------------------------------------------------
# Task 2 - Insertion Sort and Merge Sort
# ---------------------------------------------------------------------------

def insertion_sort(transactions):

    result = transactions.copy()

    for index in range(1, len(result)):
        current = result[index]
        previous = index - 1

        while (
            previous >= 0
            and result[previous]["postingDate"] > current["postingDate"]
        ):
            result[previous + 1] = result[previous]
            previous -= 1

        result[previous + 1] = current

    return result


def merge_sort(transactions):

    if len(transactions) <= 1:
        return transactions.copy()

    middle = len(transactions) // 2

    left = merge_sort(transactions[:middle])
    right = merge_sort(transactions[middle:])

    merged = []

    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):

        if (
            left[left_index]["postingDate"]
            <= right[right_index]["postingDate"]
        ):
            merged.append(left[left_index])
            left_index += 1

        else:
            merged.append(right[right_index])
            right_index += 1

    merged.extend(left[left_index:])
    merged.extend(right[right_index:])

    return merged


def task_2(transactions):

    print("\n" + "=" * 72)
    print("TASK 2 - INSERTION SORT VS MERGE SORT")
    print("=" * 72)

    # Select the account with the highest number of transactions.
    account_counts = Counter(
        transaction["accountId"]
        for transaction in transactions
    )

    selected_account = account_counts.most_common(1)[0][0]

    statement = [
        transaction
        for transaction in transactions
        if transaction["accountId"] == selected_account
    ]

    print(f"Selected Account : {selected_account}")
    print(f"Statement Size   : {len(statement):,} transactions")

    # Insertion Sort benchmark.
    start = time.time()
    insertion_result = insertion_sort(statement)
    insertion_time = time.time() - start

    # Merge Sort benchmark.
    start = time.time()
    merge_result = merge_sort(statement)
    merge_time = time.time() - start

    # Built-in sort for comparison.
    start = time.time()

    builtin_result = sorted(
        statement,
        key=lambda transaction: transaction["postingDate"]
    )

    builtin_time = time.time() - start

    print("\nSorting Execution time:")
    print(f"Insertion Sort : {insertion_time:.6f} seconds")
    print(f"Merge Sort     : {merge_time:.6f} seconds")
    print(f"Built-in Sort  : {builtin_time:.6f} seconds")

    print("\nCorrectness Checks:")

    print(
        "Insertion Sort correct:",
        [x["postingDate"] for x in insertion_result]
        == [x["postingDate"] for x in builtin_result]
    )

    print(
        "Merge Sort correct:",
        [x["postingDate"] for x in merge_result]
        == [x["postingDate"] for x in builtin_result]
    )

    print("\nStability Demonstration:")

    # Create two transactions with identical timestamps.
    timestamp = datetime(2026, 11, 18, 12, 30, 0)

    stability_sample = [
        {
            "transactionId": "TXN-A",
            "postingDate": timestamp
        },
        {
            "transactionId": "TXN-B",
            "postingDate": timestamp
        },
        {
            "transactionId": "TXN-C",
            "postingDate": datetime(2026, 11, 18, 12, 31, 0)
        }
    ]

    insertion_stable = insertion_sort(stability_sample)
    merge_stable = merge_sort(stability_sample)

    print(
        "Original order:",
        [x["transactionId"] for x in stability_sample]
    )

    print(
        "Insertion Sort:",
        [x["transactionId"] for x in insertion_stable]
    )

    print(
        "Merge Sort:",
        [x["transactionId"] for x in merge_stable]
    )

    print("\nExplanation:")
    print("- Insertion Sort: O(n^2) average/worst-case time.")
    print("- Merge Sort: O(n log n) time and O(n) auxiliary space.")
    print("- Both algorithms are stable in these implementations.")
    print("- Stability preserves the original order of equal timestamps.")


# ---------------------------------------------------------------------------
# Task 3 - Detect Duplicate Transaction Postings
# ---------------------------------------------------------------------------

def find_duplicates(transactions):

    grouped_transactions = {}

    for transaction in transactions:

        key = (
            transaction["accountId"],
            transaction["amount"],
            transaction["merchant"]
        )

        if key not in grouped_transactions:
            grouped_transactions[key] = []

        grouped_transactions[key].append(transaction)

    duplicate_groups = []

    for key, group in grouped_transactions.items():

        group.sort(key=lambda transaction: transaction["postingDate"])

        current_group = [group[0]] if group else []

        for index in range(1, len(group)):

            previous_time = group[index - 1]["postingDate"]
            current_time = group[index]["postingDate"]

            difference = (
                current_time - previous_time
            ).total_seconds()

            if difference <= 60:
                current_group.append(group[index])

            else:
                if len(current_group) > 1:
                    duplicate_groups.append((key, current_group))

                current_group = [group[index]]

        if len(current_group) > 1:
            duplicate_groups.append((key, current_group))

    return duplicate_groups


def task_3(transactions):

    print("\n" + "=" * 72)
    print("TASK 3 - DUPLICATE TRANSACTION DETECTION")
    print("=" * 72)

    duplicates = find_duplicates(transactions)

    duplicate_record_count = sum(
        len(group)
        for _, group in duplicates
    )

    print(f"Duplicate groups found : {len(duplicates):,}")
    print(f"Records in those groups: {duplicate_record_count:,}")

    print("\nFirst 5 Duplicate Groups:")

    for key, group in duplicates[:5]:

        account_id, amount, merchant = key

        transaction_ids = [
            transaction["transactionId"]
            for transaction in group
        ]

        print(f"\nAccount  : {account_id}")
        print(f"Amount   : {amount:.2f}")
        print(f"Merchant : {merchant}")
        print(f"IDs      : {transaction_ids}")

    print("\nData Structure and Complexity:")
    print("- Dictionary provides average O(1) key lookup.")
    print("- Grouping takes O(n) average time.")
    print("- Sorting the groups takes O(n log n) time in total, at most.")
    print("- Overall time: O(n log n) worst case.")
    print("- Space: O(n) for the dictionary and grouped records.")

    print("\nReason:")
    print("Hashing avoids repeatedly scanning the entire transaction list.")
    print("timestamp sorting allows efficient comparison of nearby postings.")


# ---------------------------------------------------------------------------
# Task 4 - Custom Queue and Stack
# ---------------------------------------------------------------------------

class Queue:

    def __init__(self):
        self.items = []
        self.front = 0

    def enqueue(self, transaction):
        self.items.append(transaction)

    def dequeue(self):

        if self.is_empty():
            raise IndexError("Review queue is empty.")

        transaction = self.items[self.front]
        self.front += 1

        # Periodically remove consumed entries.
        if self.front > 50 and self.front * 2 >= len(self.items):
            self.items = self.items[self.front:]
            self.front = 0

        return transaction

    def is_empty(self):
        return self.front >= len(self.items)

    def size(self):
        return len(self.items) - self.front


class Stack:

    def __init__(self):
        self.items = []

    def push(self, adjustment):
        self.items.append(adjustment)

    def pop(self):

        if self.is_empty():
            raise IndexError("Adjustment stack is empty.")

        return self.items.pop()

    def peek(self):

        if self.is_empty():
            raise IndexError("Adjustment stack is empty.")

        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


def task_4(transactions):

    print("\n" + "=" * 72)
    print("TASK 4 - MANUAL REVIEW QUEUE AND ADJUSTMENT STACK")
    print("=" * 72)

    # Custom Queue demonstration.
    review_queue = Queue()

    for transaction in transactions[:5]:
        review_queue.enqueue(transaction["transactionId"])

    print("Custom Queue - Initial Size:", review_queue.size())

    print("Custom Queue - Review Order:")

    while not review_queue.is_empty():
        print(review_queue.dequeue())

    # Custom Stack demonstration.
    adjustment_stack = Stack()

    adjustment_stack.push("Adjustment 1")
    adjustment_stack.push("Adjustment 2")
    adjustment_stack.push("Adjustment 3")

    print("\nCustom Stack - Last Adjustment:")
    print(adjustment_stack.pop())

    print("Custom Stack - Remaining Size:", adjustment_stack.size())

    # Built-in equivalents.
    builtin_queue = deque()

    builtin_queue.extend([
        "Transaction 1",
        "Transaction 2",
        "Transaction 3"
    ])

    print("\nBuilt-in Queue (deque):")

    while builtin_queue:
        print(builtin_queue.popleft())

    builtin_stack = []

    builtin_stack.extend([
        "Adjustment 1",
        "Adjustment 2",
        "Adjustment 3"
    ])

    print("\nBuilt-in Stack (list):")
    print("Reversed adjustment:", builtin_stack.pop())

    print("\nComplexity:")
    print("- Queue enqueue/dequeue: O(1) amortized.")
    print("- Stack push/pop: O(1) amortized.")
    print("- collections.deque provides efficient FIFO operations.")
    print("- Python list provides efficient stack operations.")


# ---------------------------------------------------------------------------
# Task 5 - Divide and Conquer: Minimum and Maximum
# ---------------------------------------------------------------------------

def divide_and_conquer(values):

    if len(values) == 0:
        raise ValueError("Cannot find min/max of an empty list.")

    if len(values) == 1:
        return values[0], values[0], 0

    if len(values) == 2:

        if values[0] < values[1]:
            return values[0], values[1], 1

        return values[1], values[0], 1

    middle = len(values) // 2

    left_min, left_max, left_comparisons = (
        divide_and_conquer(values[:middle])
    )

    right_min, right_max, right_comparisons = (
        divide_and_conquer(values[middle:])
    )

    comparisons = left_comparisons + right_comparisons + 2

    minimum = left_min if left_min < right_min else right_min
    maximum = left_max if left_max > right_max else right_max

    return minimum, maximum, comparisons


def brute_force(values):

    if not values:
        raise ValueError("Cannot find min/max of an empty list.")

    minimum = values[0]
    maximum = values[0]
    comparisons = 0

    for value in values[1:]:

        comparisons += 1

        if value < minimum:
            minimum = value

        comparisons += 1

        if value > maximum:
            maximum = value

    return minimum, maximum, comparisons


def task_5(transactions):

    print("\n" + "=" * 72)
    print("TASK 5 - DIVIDE AND CONQUER MINIMUM AND MAXIMUM")
    print("=" * 72)

    amounts = [
        transaction["amount"]
        for transaction in transactions
    ]

    # Divide and Conquer.
    start = time.time()

    dc_min, dc_max, dc_comparisons = (
        divide_and_conquer(amounts)
    )

    dc_time = time.time() - start

    # Brute-force scan.
    start = time.time()

    brute_min, brute_max, brute_comparisons = (
        brute_force(amounts)
    )

    brute_time = time.time() - start

    print(f"Transactions analysed: {len(amounts):,}")

    print("\nDivide and Conquer:")
    print(f"Minimum Amount : {dc_min:.2f}")
    print(f"Maximum Amount : {dc_max:.2f}")
    print(f"Comparisons    : {dc_comparisons:,}")
    print(f"Execution time : {dc_time:.6f} seconds")

    print("\nBrute-Force Scan:")
    print(f"Minimum Amount : {brute_min:.2f}")
    print(f"Maximum Amount : {brute_max:.2f}")
    print(f"Comparisons    : {brute_comparisons:,}")
    print(f"Execution time : {brute_time:.6f} seconds")

    print("\nCorrectness Check:")
    print("Minimum values match:", dc_min == brute_min)
    print("Maximum values match:", dc_max == brute_max)

    print("\nComplexity:")
    print("- Divide and Conquer: O(n) time, O(n) recursion space here.")
    print("- Brute Force: O(n) time and O(1) auxiliary space.")
    print("- Divide and Conquer reduces the number of min/max comparisons.")
    print("- Both methods examine all values.")


# ---------------------------------------------------------------------------
# Main Program
# ---------------------------------------------------------------------------

if not CSV_FILE.exists():
    raise FileNotFoundError(
        f"Could not find {CSV_FILE.name}. "
        "Place transactions.csv in the same folder as code_file.py."
    )

transactions = load_transactions(CSV_FILE)

print("=" * 72)
print("RETAIL BANKING TRANSACTION REVIEW")
print("=" * 72)

print(
    f"Loaded {len(transactions):,} transactions "
    f"from {CSV_FILE.name}"
)

task_1(transactions)
task_2(transactions)
task_3(transactions)
task_4(transactions)
task_5(transactions)
"""
Set 1 - Retail Order Desk
"""

import csv
import time
from collections import deque
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration and CSV Loading
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "orders.csv"


def load_orders(file_path):
    orders = []

    with file_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        required_columns = {"orderId", "customerId", "amount", "createdAt"}
        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError(
                f"CSV must contain these columns: {', '.join(sorted(required_columns))}"
            )

        for row in reader:
            orders.append({
                "orderId": row["orderId"],
                "customerId": row["customerId"],
                "amount": float(row["amount"]),
                "createdAt": row["createdAt"],
            })

    return orders


# ---------------------------------------------------------------------------
# Task 1 - Linear Search and Binary Search
# ---------------------------------------------------------------------------

def linear_search(orders, target_order_id):
    for order in orders:
        if order["orderId"] == target_order_id:
            return order
    return None


def binary_search(sorted_orders, target_order_id):
    low = 0
    high = len(sorted_orders) - 1

    while low <= high:
        middle = (low + high) // 2
        current_id = sorted_orders[middle]["orderId"]

        if current_id == target_order_id:
            return sorted_orders[middle]
        if current_id < target_order_id:
            low = middle + 1
        else:
            high = middle - 1

    return None


def task_1(orders):
    print("\n" + "=" * 72)
    print("TASK 1 - LINEAR SEARCH VS BINARY SEARCH")
    print("=" * 72)

    # Use an existing ID so both algorithms search for the same record.
    target_order_id = orders[len(orders) // 2]["orderId"]
    sorted_orders = sorted(orders, key=lambda order: order["orderId"])

    start = time.time()
    linear_result = linear_search(orders, target_order_id)
    linear_time = time.time() - start

    start = time.time()
    binary_result = binary_search(sorted_orders, target_order_id)
    binary_time = time.time() - start

    print(f"Dataset size       : {len(orders):,} orders")
    print(f"Target order ID    : {target_order_id}")
    print(f"Linear search      : {linear_time:.8f} seconds")
    print(f"Binary search      : {binary_time:.8f} seconds")
    print(f"Linear result found: {linear_result is not None}")
    print(f"Binary result found: {binary_result is not None}")

    print("\nObservation:")
    print("- Linear search checks records one by one: O(n) time.")
    print("- Binary search repeatedly halves the search range: O(log n) time.")
    print("- Binary search needs the data to be sorted first.")
    print("- The sorting cost should be considered if the list is not already sorted.")


# ---------------------------------------------------------------------------
# Task 2 - O(n^2) and O(n log n) Sorting Algorithms
# ---------------------------------------------------------------------------

def bubble_sort_descending(items):
    result = items.copy()
    n = len(result)

    for end in range(n - 1, 0, -1):
        swapped = False

        for index in range(end):
            if result[index]["amount"] < result[index + 1]["amount"]:
                result[index], result[index + 1] = (
                    result[index + 1],
                    result[index],
                )
                swapped = True

        if not swapped:
            break

    return result


def merge_sort_descending(items):
    if len(items) <= 1:
        return items.copy()

    middle = len(items) // 2
    left = merge_sort_descending(items[:middle])
    right = merge_sort_descending(items[middle:])

    merged = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        # Use >= so equal amounts retain their original relative order.
        if left[left_index]["amount"] >= right[right_index]["amount"]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged


def task_2(orders):
    print("\n" + "=" * 72)
    print("TASK 2 - SORTING ORDERS BY AMOUNT (DESCENDING)")
    print("=" * 72)

    # The assignment asks for a comparison on 10,000 records.
    sample_size = min(10_000, len(orders))
    sample = orders[:sample_size]

    print(f"\nBenchmarking on {sample_size:,} records...")

    start = time.time()
    bubble_result = bubble_sort_descending(sample)
    bubble_time = time.time() - start

    start = time.time()
    merge_result = merge_sort_descending(sample)
    merge_time = time.time() - start

    start = time.time()
    builtin_result = sorted(
        sample,
        key=lambda order: order["amount"],
        reverse=True
    )
    builtin_time = time.time() - start

    print(f"Bubble sort : {bubble_time:.4f} seconds")
    print(f"Merge sort  : {merge_time:.4f} seconds")
    print(f"Built-in sort: {builtin_time:.4f} seconds")

    # Confirm that every implementation produced descending amounts.
    print("\nCorrectness checks:")

    print(
        "Bubble sort descending:",
        all(
            bubble_result[i]["amount"] >= bubble_result[i + 1]["amount"]
            for i in range(len(bubble_result) - 1)
        ),
    )

    print(
        "Merge sort matches built-in amounts:",
        [x["amount"] for x in merge_result]
        == [x["amount"] for x in builtin_result],
    )

    print("\nTop 5 orders by amount (built-in sort):")

    for order in builtin_result[:5]:
        print(f'{order["orderId"]}: {order["amount"]:.2f}')


# ---------------------------------------------------------------------------
# Task 3 - Detect Duplicate Orders Using a Hash-Based Structure
# ---------------------------------------------------------------------------

def find_duplicate_orders(orders):
    seen = {}
    duplicate_groups = []

    for order in orders:
        # Amount is stored to 2 decimal places in the generated CSV.
        minute = order["createdAt"][:16]  # YYYY-MM-DD HH:MM
        key = (order["customerId"], order["amount"], minute)

        if key in seen:
            seen[key].append(order)
        else:
            seen[key] = [order]

    for key, matching_orders in seen.items():
        if len(matching_orders) > 1:
            duplicate_groups.append((key, matching_orders))

    return duplicate_groups


def task_3(orders):
    print("\n" + "=" * 72)
    print("TASK 3 - DUPLICATE ORDER DETECTION")
    print("=" * 72)

    duplicates = find_duplicate_orders(orders)

    duplicate_record_count = sum(
        len(group) for _, group in duplicates
    )

    print(f"Duplicate groups found : {len(duplicates):,}")
    print(f"Records in those groups: {duplicate_record_count:,}")

    print("\nFirst 5 duplicate groups:")

    for key, matching_orders in duplicates[:5]:
        customer_id, amount, minute = key
        order_ids = [order["orderId"] for order in matching_orders]

        print(
            f"Customer={customer_id}, Amount={amount:.2f}, "
            f"Minute={minute}, Orders={order_ids}"
        )

    print("\nComplexity:")
    print("- Average time: O(n), because dictionary lookup/insertion is O(1) on average.")
    print("- Space: O(n), because the dictionary stores keys and matching orders.")
    print("- Worst-case hash-table operations can degrade, but are uncommon.")


# ---------------------------------------------------------------------------
# Task 4 - Implement Stack and Queue From Scratch, Then Compare
# ---------------------------------------------------------------------------

class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Cannot undo: stack is empty.")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty.")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)


class Queue:
    def __init__(self):
        self._items = []
        self._front = 0

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Cannot dispatch: queue is empty.")

        item = self._items[self._front]
        self._front += 1

        # Periodically discard consumed elements to avoid retaining them.
        if self._front > 50 and self._front * 2 >= len(self._items):
            self._items = self._items[self._front:]
            self._front = 0

        return item

    def is_empty(self):
        return self._front >= len(self._items)

    def __len__(self):
        return len(self._items) - self._front


def task_4(orders):
    print("\n" + "=" * 72)
    print("TASK 4 - STACK (UNDO) AND QUEUE (DISPATCH)")
    print("=" * 72)

    # Demonstrate undo using a custom stack.
    custom_stack = Stack()

    custom_stack.push({
        "orderId": "ORD-DEMO-1",
        "amount": 500.00
    })

    custom_stack.push({
        "orderId": "ORD-DEMO-2",
        "amount": 750.00
    })

    last_edit = custom_stack.pop()
    print("Custom stack - undone edit:", last_edit)

    # Demonstrate FIFO dispatch using a custom queue.
    custom_queue = Queue()

    for order in orders[:3]:
        custom_queue.enqueue(order["orderId"])

    print(
        "Custom queue - dispatch order:",
        [custom_queue.dequeue() for _ in range(3)]
    )

    # Built-in equivalents: list for stack, collections.deque for queue.
    builtin_stack = []

    builtin_stack.append("Edit 1")
    builtin_stack.append("Edit 2")

    print("Built-in list stack - undone edit:", builtin_stack.pop())

    builtin_queue = deque()
    builtin_queue.extend(["Order 1", "Order 2", "Order 3"])

    print(
        "Built-in deque queue - dispatch order:",
        [builtin_queue.popleft() for _ in range(3)]
    )

    print("\nComplexity:")
    print("- Stack push/pop: O(1) amortized.")
    print("- Queue enqueue/dequeue: O(1) amortized with the front-pointer implementation.")
    print("- collections.deque provides efficient O(1) append and popleft operations.")


# ---------------------------------------------------------------------------
# Task 5 - Greedy Refund and Dynamic Programming
# ---------------------------------------------------------------------------

def greedy_change(amount, denominations):
    remaining = amount
    result = {}

    for denomination in sorted(denominations, reverse=True):
        count, remaining = divmod(remaining, denomination)

        if count:
            result[denomination] = count

    if remaining != 0:
        return None

    return result


def dp_change(amount, denominations):
    infinity = amount + 1
    dp = [infinity] * (amount + 1)
    previous_coin = [None] * (amount + 1)

    dp[0] = 0

    for value in range(1, amount + 1):
        for coin in denominations:
            if coin <= value and dp[value - coin] + 1 < dp[value]:
                dp[value] = dp[value - coin] + 1
                previous_coin[value] = coin

    if dp[amount] == infinity:
        return None, None

    breakdown = {}
    current = amount

    while current > 0:
        coin = previous_coin[current]
        breakdown[coin] = breakdown.get(coin, 0) + 1
        current -= coin

    return dp[amount], breakdown


def task_5():
    print("\n" + "=" * 72)
    print("TASK 5 - GREEDY REFUND AND DYNAMIC PROGRAMMING")
    print("=" * 72)

    refund_amount = 786

    indian_denominations = [
        2000, 500, 200, 100, 50, 20, 10, 5, 2, 1
    ]

    greedy_result = greedy_change(
        refund_amount,
        indian_denominations
    )

    greedy_count = sum(greedy_result.values())

    print(f"Refund amount: Rs. {refund_amount}")
    print("Greedy denomination breakdown:", greedy_result)
    print("Total notes/coins:", greedy_count)

    # Demonstrate a denomination system for which greedy is not optimal.
    failing_denominations = [1, 3, 4]
    failing_amount = 6

    greedy_failure = greedy_change(
        failing_amount,
        failing_denominations
    )

    dp_count, dp_breakdown = dp_change(
        failing_amount,
        failing_denominations
    )

    print("\nExample where greedy fails:")
    print(f"Denominations: {failing_denominations}")
    print(f"Amount: {failing_amount}")

    print(
        "Greedy result:",
        greedy_failure,
        "=>", sum(greedy_failure.values()), "pieces",
    )

    print(
        "DP result:",
        dp_breakdown,
        "=>", dp_count, "pieces"
    )

    print("\nComplexity:")
    print("- Greedy: O(d log d) including denomination sorting, then O(d) selection.")
    print("- Dynamic Programming: O(amount * d) time and O(amount) space.")
    print("- Greedy is not optimal for every denomination system; DP finds the minimum.")


# ---------------------------------------------------------------------------
# Main Program
# ---------------------------------------------------------------------------

if not CSV_FILE.exists():
    raise FileNotFoundError(
        f"Could not find {CSV_FILE.name}. "
        "Place orders.csv in the same folder as code_file.py."
    )

orders = load_orders(CSV_FILE)

print("=" * 72)
print("RETAIL ORDER DESK")
print("=" * 72)

print(f"Loaded {len(orders):,} orders from {CSV_FILE.name}")

task_1(orders)
task_2(orders)
task_3(orders)
task_4(orders)
task_5()
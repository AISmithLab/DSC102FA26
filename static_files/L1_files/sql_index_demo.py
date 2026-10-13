"""Same SQL query, different plan: SQLite with and without an index.

Usage: python sql_index_demo.py   (creates a temporary database in memory)
"""
import random
import sqlite3
import time

random.seed(0)
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, price REAL)")
db.executemany("INSERT INTO orders (customer_id, price) VALUES (?, ?)",
               ((random.randrange(100_000), random.random() * 100) for _ in range(2_000_000)))

QUERY = "SELECT AVG(price) FROM orders WHERE customer_id = 42"


def best_time(repeats=5):
    best = float("inf")
    for _ in range(repeats):
        t0 = time.perf_counter()
        db.execute(QUERY).fetchall()
        best = min(best, time.perf_counter() - t0)
    return best


for label in ["no index", "with index"]:
    if label == "with index":
        db.execute("CREATE INDEX idx_customer ON orders(customer_id)")
    plan = db.execute("EXPLAIN QUERY PLAN " + QUERY).fetchall()[0][-1]
    print(f"{label:<11} plan: {plan:<55} time: {best_time() * 1e3:.3f} ms")

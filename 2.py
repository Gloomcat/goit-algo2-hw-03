import csv
import timeit

from functools import partial

from BTrees.OOBTree import OOBTree


def add_item_to_tree(tree_store: OOBTree, item: dict[str, str]) -> None:
    tree_store[int(item["ID"])] = {
        "Name": item["Name"],
        "Category": item["Category"],
        "Price": float(item["Price"]),
    }


def add_item_to_dict(dict_store: dict[int, dict], item: dict[str, str]) -> None:
    dict_store[int(item["ID"])] = {
        "Name": item["Name"],
        "Category": item["Category"],
        "Price": float(item["Price"]),
    }

# It is impossible to effectively use items() method on prices because it can be used only with
# OOBTree keys (ref https://btrees.readthedocs.io/en/latest/api.html#BTrees.OOBTree.OOBTree.items).
# In order to correctly analyze struct's performance we apply range to keys.
def range_query_tree(tree_store: OOBTree, low: int, high: int):
    return list(tree_store.items(min=low, max=high))

def range_query_dict(dict_store: dict[int, dict], low: int, high: int):
    return [(k, v) for k, v in dict_store.items() if low <= k <= high]

if __name__ == "__main__":
    tree_store = OOBTree()
    dict_store = {}

    with open(
        "generated_items_data.csv", mode="r", newline="", encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)
        for item in reader:
            add_item_to_tree(tree_store, item)
            add_item_to_dict(dict_store, item)

    low = 1000
    high = 10000

    time_tree = timeit.timeit(
        partial(range_query_tree, tree_store, low, high), number=100)
    print(f"Total range_query time for OOBTree: {time_tree} seconds")

    time_dict = timeit.timeit(
        partial(range_query_dict, dict_store, low, high), number=100)
    print(f"Total range_query time for Dict: {time_dict} seconds")

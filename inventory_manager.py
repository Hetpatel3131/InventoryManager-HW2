"""CPS310 Inventory Manager, refactored from the instructor checkpoint."""

INVENTORY_FILE = "inventory.txt"
LOW_STOCK_THRESHOLD = 5


def load_inventory(filename):
    """Load records; ignore blank lines and allow a missing file."""
    inventory = []
    try:
        with open(filename, encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                name, category, quantity = line.split("|")
                inventory.append({
                    "name": name,
                    "category": category,
                    "quantity": int(quantity),
                })
    except FileNotFoundError:
        return []
    return inventory


def save_inventory(inventory, filename):
    """Save records using Name|Category|Quantity format."""
    with open(filename, "w", encoding="utf-8") as file:
        for item in inventory:
            file.write(
                f'{item["name"]}|{item["category"]}|{item["quantity"]}\n'
            )


def parse_quantity(value):
    """Return a nonnegative integer or reject invalid quantity input."""
    text = str(value).strip()
    if not text.isdecimal():
        raise ValueError("Quantity must be a nonnegative whole number.")
    return int(text)


def validate_new_item(inventory, name, category, quantity):
    """Return a validated item without changing the inventory."""
    name = name.strip()
    category = category.strip()
    if not name:
        raise ValueError("Item name cannot be empty.")
    if "|" in name:
        raise ValueError("Item name may not contain the | character.")
    if not category:
        raise ValueError("Category cannot be empty.")
    if "|" in category:
        raise ValueError("Category may not contain the | character.")
    for item in inventory:
        if item["name"].lower() == name.lower():
            raise ValueError("An item with that name already exists.")
    return {
        "name": name,
        "category": category,
        "quantity": parse_quantity(quantity),
    }


def find_matching_items(inventory, search_term):
    """Return case-insensitive name matches; reject blank searches."""
    search_term = search_term.strip()
    if not search_term:
        raise ValueError("Search term cannot be empty.")
    return [
        item for item in inventory
        if search_term.lower() in item["name"].lower()
    ]


def get_item_index(inventory, item_number):
    """Convert a valid one-based item number to a list index."""
    if type(item_number) is not int:
        raise ValueError("Item number must be a whole number.")
    if item_number < 1 or item_number > len(inventory):
        raise ValueError("Item number is outside the available range.")
    return item_number - 1


def remove_item_by_number(inventory, item_number):
    """Remove and return the selected item without saving a file."""
    index = get_item_index(inventory, item_number)
    return inventory.pop(index)


def update_item_quantity(inventory, item_number, new_quantity):
    """Validate and change only the selected item's quantity."""
    index = get_item_index(inventory, item_number)
    quantity = parse_quantity(new_quantity)
    inventory[index]["quantity"] = quantity
    return inventory[index]


def calculate_summary(inventory):
    """Return summary data with lowercase category keys."""
    summary = {
        "unique_items": len(inventory),
        "total_quantity": 0,
        "low_stock_items": 0,
        "category_counts": {},
    }
    for item in inventory:
        summary["total_quantity"] += item["quantity"]
        if item["quantity"] < LOW_STOCK_THRESHOLD:
            summary["low_stock_items"] += 1
        category = item["category"].lower()
        counts = summary["category_counts"]
        counts[category] = counts.get(category, 0) + 1
    return summary


def display_menu():
    print("\nInventory Manager")
    print("1. View inventory")
    print("2. Add an item")
    print("3. Update an item quantity")
    print("4. Remove an item")
    print("5. Search inventory")
    print("6. View inventory summary")
    print("7. Exit")


def view_inventory(inventory):
    if not inventory:
        print("No inventory items found.")
        return
    print("\nInventory:")
    for number, item in enumerate(inventory, start=1):
        print(
            f'{number}. {item["name"]} | {item["category"]} | '
            f'Quantity: {item["quantity"]}'
        )


def add_item(inventory):
    name = input("Enter the item name: ")
    category = input("Enter the category: ")
    quantity = input("Enter the quantity: ")
    try:
        item = validate_new_item(inventory, name, category, quantity)
    except ValueError as error:
        print(error)
        return
    inventory.append(item)
    save_inventory(inventory, INVENTORY_FILE)
    print("Item added successfully.")


def update_quantity(inventory):
    if not inventory:
        print("No inventory items found.")
        return
    view_inventory(inventory)
    try:
        number = int(input("Enter the item number to update: "))
        get_item_index(inventory, number)
        quantity = input("Enter the new quantity: ")
        item = update_item_quantity(inventory, number, quantity)
    except ValueError as error:
        print(error)
        return
    save_inventory(inventory, INVENTORY_FILE)
    print(f'{item["name"]} quantity updated to {item["quantity"]}.')


def remove_item(inventory):
    if not inventory:
        print("No inventory items found.")
        return
    view_inventory(inventory)
    try:
        number = int(input("Enter the item number to remove: "))
        item = remove_item_by_number(inventory, number)
    except ValueError as error:
        print(error)
        return
    save_inventory(inventory, INVENTORY_FILE)
    print(f'Item removed: {item["name"]}')


def search_inventory(inventory):
    term = input("Enter part or all of an item name: ")
    try:
        matches = find_matching_items(inventory, term)
    except ValueError as error:
        print(error)
        return
    if not matches:
        print("No inventory items matched your search.")
        return
    print("\nSearch Results:")
    view_inventory(matches)


def display_summary(inventory):
    summary = calculate_summary(inventory)
    print("\nInventory Summary")
    print(f'Unique items: {summary["unique_items"]}')
    print(f'Total quantity: {summary["total_quantity"]}')
    print(f'Low-stock items: {summary["low_stock_items"]}')
    print("\nItems by category:")
    if not summary["category_counts"]:
        print("No categories found.")
    for category, count in summary["category_counts"].items():
        print(f"{category}: {count}")


def main():
    inventory = load_inventory(INVENTORY_FILE)
    while True:
        display_menu()
        choice = input("Choose an option (1-7): ").strip()
        if choice == "1":
            view_inventory(inventory)
        elif choice == "2":
            add_item(inventory)
        elif choice == "3":
            update_quantity(inventory)
        elif choice == "4":
            remove_item(inventory)
        elif choice == "5":
            search_inventory(inventory)
        elif choice == "6":
            display_summary(inventory)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Please enter a menu option from 1 through 7.")


if __name__ == "__main__":
    main()
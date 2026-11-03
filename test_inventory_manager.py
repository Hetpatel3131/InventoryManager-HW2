from copy import deepcopy

import pytest
import inventory_manager as im


@pytest.fixture
def sample_inventory():
    return [
        {"name": "Laptop Charger", "category": "Electronics", "quantity": 8},
        {"name": "USB-C Cable", "category": "electronics", "quantity": 12},
        {"name": "Printer Paper", "category": "Office Supplies", "quantity": 25},
        {"name": "Dry-Erase Markers", "category": "Classroom Supplies", "quantity": 4},
        {"name": "Sticky Notes", "category": "Office Supplies", "quantity": 5},
    ]


def test_load_valid_inventory(tmp_path):
    # Arrange
    path = tmp_path / "inventory.txt"
    path.write_text("Cable|Electronics|8\nPaper|Office|12\n", encoding="utf-8")
    expected = [
        {"name": "Cable", "category": "Electronics", "quantity": 8},
        {"name": "Paper", "category": "Office", "quantity": 12},
    ]

    # Act
    result = im.load_inventory(path)

    # Assert
    assert result == expected


def test_load_converts_quantity_to_integer(tmp_path):
    # Arrange
    path = tmp_path / "inventory.txt"
    path.write_text("Cable|Electronics|8\n", encoding="utf-8")

    # Act
    result = im.load_inventory(path)

    # Assert
    assert result[0]["quantity"] == 8
    assert type(result[0]["quantity"]) is int


def test_load_ignores_blank_lines(tmp_path):
    # Arrange
    path = tmp_path / "inventory.txt"
    path.write_text("\n  \nCable|Electronics|8\n\n", encoding="utf-8")

    # Act
    result = im.load_inventory(path)

    # Assert
    assert result == [
        {"name": "Cable", "category": "Electronics", "quantity": 8}
    ]


def test_load_missing_file_returns_empty_inventory(tmp_path):
    # Arrange
    path = tmp_path / "missing.txt"

    # Act
    result = im.load_inventory(path)

    # Assert
    assert result == []
    assert not path.exists()


def test_save_writes_correct_format(tmp_path, sample_inventory):
    # Arrange
    path = tmp_path / "saved.txt"
    expected = (
        "Laptop Charger|Electronics|8\n"
        "USB-C Cable|electronics|12\n"
        "Printer Paper|Office Supplies|25\n"
        "Dry-Erase Markers|Classroom Supplies|4\n"
        "Sticky Notes|Office Supplies|5\n"
    )

    # Act
    im.save_inventory(sample_inventory, path)

    # Assert
    assert path.read_text(encoding="utf-8") == expected


def test_save_empty_inventory_empties_existing_file(tmp_path):
    # Arrange
    path = tmp_path / "saved.txt"
    path.write_text("Old Item|Office|2\n", encoding="utf-8")

    # Act
    im.save_inventory([], path)

    # Assert
    assert path.read_text(encoding="utf-8") == ""


def test_save_and_load_round_trip(tmp_path, sample_inventory):
    # Arrange
    path = tmp_path / "round_trip.txt"
    expected = deepcopy(sample_inventory)

    # Act
    im.save_inventory(sample_inventory, path)
    result = im.load_inventory(path)

    # Assert
    assert result == expected
    assert sample_inventory == expected


@pytest.mark.parametrize(
    "term, expected_indices",
    [
        ("Laptop Charger", [0]),
        ("Cable", [1]),
        ("CHARGER", [0]),
        ("a", [0, 1, 2, 3]),
        ("not-found", []),
    ],
    ids=[
        "exact",
        "partial",
        "case-insensitive",
        "multiple-matches",
        "no-match",
    ],
)
def test_search_results(sample_inventory, term, expected_indices):
    # Arrange
    before = deepcopy(sample_inventory)
    expected = [before[index] for index in expected_indices]

    # Act
    result = im.find_matching_items(sample_inventory, term)

    # Assert
    assert result == expected
    assert sample_inventory == before


@pytest.mark.parametrize(
    "term",
    ["", "   "],
    ids=["empty", "spaces"],
)
def test_search_rejects_blank_terms(sample_inventory, term):
    # Arrange
    before = deepcopy(sample_inventory)

    # Act and Assert
    with pytest.raises(ValueError, match="Search term cannot be empty"):
        im.find_matching_items(sample_inventory, term)

    assert sample_inventory == before

@pytest.mark.parametrize(
    "number, remaining_indices",
    [
        (1, [1, 2, 3, 4]),
        (3, [0, 1, 3, 4]),
        (5, [0, 1, 2, 3]),
    ],
    ids=["first", "middle", "last"],
)
def test_remove_correct_item(sample_inventory, number, remaining_indices):
    # Arrange
    before = deepcopy(sample_inventory)
    expected = [before[index] for index in remaining_indices]

    # Act
    removed = im.remove_item_by_number(sample_inventory, number)

    # Assert
    assert sample_inventory == expected
    assert removed == before[number - 1]


@pytest.mark.parametrize(
    "number",
    [0, -1, 6],
    ids=["zero", "negative", "too-large"],
)
def test_remove_rejects_invalid_numbers(sample_inventory, number):
    # Arrange
    before = deepcopy(sample_inventory)

    # Act and Assert
    with pytest.raises(ValueError, match="outside the available range"):
        im.remove_item_by_number(sample_inventory, number)

    assert sample_inventory == before


@pytest.mark.parametrize(
    "quantity",
    [7, 0],
    ids=["positive", "zero"],
)
def test_update_changes_only_selected_item(sample_inventory, quantity):
    # Arrange
    expected = deepcopy(sample_inventory)
    expected[1]["quantity"] = quantity

    # Act
    result = im.update_item_quantity(sample_inventory, 2, quantity)

    # Assert
    assert sample_inventory == expected
    assert result == expected[1]


@pytest.mark.parametrize(
    "number",
    [0, -1, 6],
    ids=["zero", "negative", "too-large"],
)
def test_update_rejects_invalid_numbers(sample_inventory, number):
    # Arrange
    before = deepcopy(sample_inventory)

    # Act and Assert
    with pytest.raises(ValueError, match="outside the available range"):
        im.update_item_quantity(sample_inventory, number, 10)

    assert sample_inventory == before


@pytest.mark.parametrize(
    "quantity",
    [-1, "six", "2.5"],
    ids=["negative", "nonnumeric", "fractional"],
)
def test_update_rejects_invalid_quantities(sample_inventory, quantity):
    # Arrange
    before = deepcopy(sample_inventory)

    # Act and Assert
    with pytest.raises(ValueError, match="nonnegative whole number"):
        im.update_item_quantity(sample_inventory, 2, quantity)

    assert sample_inventory == before


@pytest.mark.parametrize(
    "quantity",
    ["6", "0"],
    ids=["normal", "zero"],
)
def test_validate_accepts_new_item(sample_inventory, quantity):
    # Arrange
    before = deepcopy(sample_inventory)
    expected_quantity = 6 if quantity == "6" else 0

    # Act
    result = im.validate_new_item(
        sample_inventory, " HDMI Cable ", " Electronics ", quantity
    )

    # Assert
    assert result == {
        "name": "HDMI Cable",
        "category": "Electronics",
        "quantity": expected_quantity,
    }
    assert sample_inventory == before


@pytest.mark.parametrize(
    "name, category, quantity, message",
    [
        ("", "Office", "1", "Item name cannot be empty"),
        ("   ", "Office", "1", "Item name cannot be empty"),
        ("Pen", "", "1", "Category cannot be empty"),
        ("Pen", "   ", "1", "Category cannot be empty"),
        ("Pen|Blue", "Office", "1", "Item name may not contain"),
        ("Pen", "Office|School", "1", "Category may not contain"),
        ("Pen", "Office", "-1", "nonnegative whole number"),
        ("Pen", "Office", "six", "nonnegative whole number"),
        ("Pen", "Office", "2.5", "nonnegative whole number"),
        ("Laptop Charger", "Electronics", "1", "already exists"),
        ("laptop charger", "Electronics", "1", "already exists"),
    ],
    ids=[
        "empty-name",
        "blank-name",
        "empty-category",
        "blank-category",
        "pipe-in-name",
        "pipe-in-category",
        "negative-quantity",
        "nonnumeric-quantity",
        "fractional-quantity",
        "duplicate",
        "duplicate-case",
    ],
)
def test_validate_rejects_invalid_item(
    sample_inventory, name, category, quantity, message
):
    # Arrange
    before = deepcopy(sample_inventory)

    # Act and Assert
    with pytest.raises(ValueError, match=message):
        im.validate_new_item(sample_inventory, name, category, quantity)

    assert sample_inventory == before


def test_summary_counts_items_quantities_and_categories(sample_inventory):
    # Arrange
    before = deepcopy(sample_inventory)
    expected = {
        "unique_items": 5,
        "total_quantity": 54,
        "low_stock_items": 1,
        "category_counts": {
            "electronics": 2,
            "office supplies": 2,
            "classroom supplies": 1,
        },
    }

    # Act
    result = im.calculate_summary(sample_inventory)

    # Assert
    assert result == expected
    assert sample_inventory == before


def test_summary_for_empty_inventory():
    # Arrange
    inventory = []

    # Act
    result = im.calculate_summary(inventory)

    # Assert
    assert result == {
        "unique_items": 0,
        "total_quantity": 0,
        "low_stock_items": 0,
        "category_counts": {},
    }


@pytest.mark.parametrize(
    "quantity, expected_low_stock",
    [
        (0, 1),
        (4, 1),
        (5, 0),
        (6, 0),
    ],
    ids=["zero", "four-low", "five-not-low", "six-not-low"],
)
def test_summary_low_stock_boundary(quantity, expected_low_stock):
    # Arrange
    inventory = [
        {"name": "Pen", "category": "Office", "quantity": quantity}
    ]

    # Act
    result = im.calculate_summary(inventory)

    # Assert
    assert result["low_stock_items"] == expected_low_stock


def test_summary_counts_items_quantities_and_categories(sample_inventory):
    # Arrange
    before = deepcopy(sample_inventory)
    expected = {
        "unique_items": 5,
        "total_quantity": 54,
        "low_stock_items": 1,
        "category_counts": {
            "electronics": 2,
            "office supplies": 2,
            "classroom supplies": 1,
        },
    }

    # Act
    result = im.calculate_summary(sample_inventory)

    # Assert
    assert result == expected
    assert sample_inventory == before


def test_summary_for_empty_inventory():
    # Arrange
    inventory = []

    # Act
    result = im.calculate_summary(inventory)

    # Assert
    assert result == {
        "unique_items": 0,
        "total_quantity": 0,
        "low_stock_items": 0,
        "category_counts": {},
    }


@pytest.mark.parametrize(
    "quantity, expected_low_stock",
    [
        (0, 1),
        (4, 1),
        (5, 0),
        (6, 0),
    ],
    ids=["zero", "four-low", "five-not-low", "six-not-low"],
)
def test_summary_low_stock_boundary(quantity, expected_low_stock):
    # Arrange
    inventory = [
        {"name": "Pen", "category": "Office", "quantity": quantity}
    ]

    # Act
    result = im.calculate_summary(inventory)

    # Assert
    assert result["low_stock_items"] == expected_low_stock

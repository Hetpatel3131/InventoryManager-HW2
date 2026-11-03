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
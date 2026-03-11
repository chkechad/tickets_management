import pytest

from app.schemas.ticket import validate_title


def test_validate_title_fail() -> None:
    """Validate the title fail."""
    with pytest.raises(ValueError):
        validate_title("  ")
        validate_title("")

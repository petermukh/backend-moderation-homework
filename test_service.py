from unittest.mock import Mock

import pytest

from schemas import PredictionRequest
from services import PredictionService


@pytest.mark.parametrize(
    ("is_verified_seller", "images_qty", "minimum_images", "has_violation"),
    [
        (True, 0, 2, False),
        (False, 0, 1, True),
        (False, 1, 1, False),
        (False, 1, 2, True),
        (False, 2, 2, False),
    ],
)
def test_prediction_service(
    is_verified_seller, images_qty, minimum_images, has_violation
):
    repository = Mock()
    repository.minimum_images_for_unverified_seller.return_value = minimum_images
    advertisement = PredictionRequest(
        seller_id=1,
        is_verified_seller=is_verified_seller,
        item_id=2,
        name="Книга",
        description="Книга в хорошем состоянии",
        category=3,
        images_qty=images_qty,
    )

    result = PredictionService(repository).predict(advertisement)

    assert result is has_violation
    if is_verified_seller:
        repository.minimum_images_for_unverified_seller.assert_not_called()
    else:
        repository.minimum_images_for_unverified_seller.assert_called_once_with()

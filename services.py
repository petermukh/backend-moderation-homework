from repositories import ModerationRepository
from schemas import PredictionRequest


class PredictionService:
    def __init__(self, repository: ModerationRepository) -> None:
        self.repository = repository

    def predict(self, advertisement: PredictionRequest) -> bool:
        """Return True when the advertisement has a violation."""
        if advertisement.is_verified_seller:
            return False
        return (
            advertisement.images_qty
            < self.repository.minimum_images_for_unverified_seller()
        )


def get_prediction_service() -> PredictionService:
    return PredictionService(ModerationRepository())

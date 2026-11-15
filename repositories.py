class ModerationRepository:
    """Read the current moderation policy. This version stores it in memory."""

    def minimum_images_for_unverified_seller(self) -> int:
        return 1

from abc import ABC, abstractmethod

from app.models.verification import VerificationResult


class VerificationAdapter(ABC):
    """Interface for authoritative or mock verification providers."""

    @abstractmethod
    def verify(self, identifier: str) -> VerificationResult:
        raise NotImplementedError
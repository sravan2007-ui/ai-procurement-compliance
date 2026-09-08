from typing import Any

from app.models.gst import GSTDocument
from app.models.pan import PANDocument
from app.models.verification import VerificationResult
from app.services.verification.base import VerificationAdapter
from app.services.verification.verification_consistency import (
    VerificationConsistencyChecker,
)
from app.services.workflow.state import ComplianceGraphState


def verify_bidder(
        state: ComplianceGraphState,
        verification_adapter: VerificationAdapter | None = None,
        consistency_checker: VerificationConsistencyChecker | None = None,
        verification_adapters: dict[str, VerificationAdapter] | None = None,
    ) -> ComplianceGraphState:
        """Verify bidder data against available authoritative sources."""

        if state.get("error"):
            return state

        bidder_data: dict[str, Any] = state.get("bidder_data", {})
        rules = state.get("rules", [])

        if (
            verification_adapter is None
            and not verification_adapters
        ):
            return {
                **state,
                "verification_results": {},
            }

        consistency_checker = (
            consistency_checker or VerificationConsistencyChecker()
        )

        verification_results: dict[str, VerificationResult] = {}

        for rule in rules:
            data = bidder_data.get(rule.rule_type)

            adapter = verification_adapter

            if verification_adapters:
                adapter = verification_adapters.get(rule.rule_type)

            if adapter is None:
                continue

            if rule.rule_type == "GST_STATUS":
                if not isinstance(data, GSTDocument):
                    continue

                verification_result = adapter.verify(data.gstin)

                verification_result = consistency_checker.compare_gst(
                    data,
                    verification_result,
                )

                verification_results[rule.rule_id] = verification_result

            elif rule.rule_type == "PAN":
                if not isinstance(data, PANDocument):
                    continue

                if not data.pan_number:
                    continue

                verification_result = adapter.verify(data.pan_number)

                verification_result = consistency_checker.compare_pan(
                    data,
                    verification_result,
                )

                verification_results[rule.rule_id] = verification_result

        return {
            **state,
            "verification_results": verification_results,
        }
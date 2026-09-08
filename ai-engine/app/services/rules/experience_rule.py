from datetime import date

from app.models.compliance import (
    ComplianceResult,
    ComplianceRule,
    ComplianceStatus,
)
from app.models.experience import ExperienceDocument

class ExperienceRuleEvaluator:
    """Evaluate bidder experience against tender requirements."""

    @staticmethod
    def _normalize_project_type(value: str) -> str:
        normalized = value.strip().lower()

        for suffix in (" projects", " project"):
            if normalized.endswith(suffix):
                normalized = normalized[: -len(suffix)]

        return normalized

    def evaluate(
        self,
        rule: ComplianceRule,
        experience_document: ExperienceDocument | None,
    ) -> ComplianceResult:

        minimum_projects = int(
            rule.parameters.get("minimum_projects", 1)
        )

        minimum_project_value = float(
            rule.parameters.get("minimum_project_value", 0)
        )

        if experience_document is None:
            return ComplianceResult(
                rule_id=rule.rule_id,
                status=ComplianceStatus.REVIEW_REQUIRED,
                message="Experience document was not provided.",
                evidence={
                    "required_projects": minimum_projects,
                    "minimum_project_value": minimum_project_value,
                },
                confidence=1.0,
            )

        if isinstance(experience_document, dict):
            try:
                experience_document = ExperienceDocument.model_validate(
                    experience_document
                )
            except Exception:
                return ComplianceResult(
                    rule_id=rule.rule_id,
                    status=ComplianceStatus.REVIEW_REQUIRED,
                    message="Submitted experience document could not be parsed.",
                    evidence={
                        "required_projects": minimum_projects,
                        "minimum_project_value": minimum_project_value,
                    },
                    confidence=1.0,
                )

        required_project_type = rule.parameters.get("project_type")

        experience_years = rule.parameters.get("experience_years")
        reference_date_value = rule.parameters.get("reference_date")

        reference_date = None

        if experience_years is not None:
            if reference_date_value is None:
                return ComplianceResult(
                    rule_id=rule.rule_id,
                    status=ComplianceStatus.REVIEW_REQUIRED,
                    message="Reference date is required to evaluate the experience period.",
                    evidence={
                        "required_projects": minimum_projects,
                        "experience_years": experience_years,
                    },
                    confidence=experience_document.confidence,
                )

            try:
                reference_date = date.fromisoformat(str(reference_date_value))
            except ValueError:
                return ComplianceResult(
                    rule_id=rule.rule_id,
                    status=ComplianceStatus.REVIEW_REQUIRED,
                    message="The experience requirement contains an invalid reference date.",
                    evidence={
                        "reference_date": reference_date_value,
                    },
                    confidence=experience_document.confidence,
                )

            experience_start_date = date(
                reference_date.year - int(experience_years),
                reference_date.month,
                reference_date.day,
            )

        projects = experience_document.projects

        if not projects:
            return ComplianceResult(
                rule_id=rule.rule_id,
                status=ComplianceStatus.REVIEW_REQUIRED,
                message="No experience projects were found in the submitted document.",
                evidence={
                    "required_projects": minimum_projects,
                    "submitted_projects": 0,
                },
                confidence=experience_document.confidence,
            )

        qualifying_projects = []

        for project in projects:

            if project.project_value < minimum_project_value:
                continue

            if experience_years is not None:
                if project.completion_date is None:
                    return ComplianceResult(
                        rule_id=rule.rule_id,
                        status=ComplianceStatus.REVIEW_REQUIRED,
                        message=(
                            f"Completion date is missing for experience project "
                            f"'{project.project_name}', so the experience period "
                            f"could not be verified."
                        ),
                        evidence={
                            "project_name": project.project_name,
                            "experience_years": experience_years,
                            "reference_date": reference_date.isoformat(),
                            "experience_start_date": experience_start_date.isoformat(),
                        },
                        confidence=experience_document.confidence,
                    )

                if (
                    project.completion_date < experience_start_date
                    or project.completion_date > reference_date
                ):
                    continue

            if required_project_type:
                if not project.project_type:
                    continue

                if (
                    self._normalize_project_type(project.project_type)
                    != self._normalize_project_type(required_project_type)
                ):
                    continue

            qualifying_projects.append(project)

        qualifying_count = len(qualifying_projects)

        if qualifying_count >= minimum_projects:
            return ComplianceResult(
                rule_id=rule.rule_id,
                status=ComplianceStatus.PASS,
                message=(
                    f"{qualifying_count} qualifying experience project(s) "
                    f"were found, meeting the minimum requirement of "
                    f"{minimum_projects}."
                ),
                evidence={
                    "required_projects": minimum_projects,
                    "qualifying_projects": qualifying_count,
                    "minimum_project_value": minimum_project_value,
                    "required_project_type": required_project_type,
                    "qualifying_project_names": [
                        project.project_name
                        for project in qualifying_projects
                    ],
                },
                confidence=experience_document.confidence,
            )

        return ComplianceResult(
            rule_id=rule.rule_id,
            status=ComplianceStatus.FAIL,
            message=(
                f"Only {qualifying_count} qualifying experience project(s) "
                f"were found, but {minimum_projects} are required."
            ),
            evidence={
                "required_projects": minimum_projects,
                "qualifying_projects": qualifying_count,
                "minimum_project_value": minimum_project_value,
                "required_project_type": required_project_type,
                "submitted_projects": len(projects),
            },
            confidence=experience_document.confidence,
        )

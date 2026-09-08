from app.models.tender_requirement import TenderRequirementSet
from app.services.gemini_client import GeminiClient


class TenderRequirementExtractor:
    """Extract structured compliance requirements from tender text."""

    def __init__(self, gemini_client: GeminiClient | None = None) -> None:
        self.gemini_client = gemini_client or GeminiClient()

    def extract(self, tender_text: str) -> TenderRequirementSet:
        if not tender_text.strip():
            raise ValueError("Tender text cannot be empty.")

        prompt = self._build_prompt(tender_text)

        return self.gemini_client.generate_structured(
            prompt=prompt,
            response_model=TenderRequirementSet,
        )

    @staticmethod
    def _build_prompt(tender_text: str) -> str:
        return f"""
You are an AI assistant for government procurement compliance verification.

Analyze the tender text below and extract only the bidder eligibility
and compliance requirements that can be evaluated by a compliance system.

Supported rule types are:

- MIN_AVERAGE_TURNOVER
- REQUIRED_DOCUMENT
- GST_STATUS
- UDYAM_ELIGIBILITY
- EXPERIENCE_REQUIREMENT

For every extracted requirement:

1. Create a unique rule_id.
2. Provide a clear name.
3. Describe the requirement accurately.
4. Select the most appropriate supported rule_type.
5. Extract all parameters needed for deterministic evaluation.
6. Mark whether the requirement is mandatory.
7. Preserve the relevant original tender wording in source_text.

Parameter extraction rules:

- MIN_AVERAGE_TURNOVER:
  Extract the minimum required average turnover as the numeric
  parameter "minimum".

  The "minimum" value must always be expressed in INR crore,
  because the deterministic turnover rule engine evaluates
  turnover in crore.

  Examples:
  - "10 crore" -> minimum: 10
  - "₹10 crore" -> minimum: 10
  - "Rs. 10 crore" -> minimum: 10
  - "100 lakh" -> minimum: 1
  - "1 crore" -> minimum: 1
  - "₹100000000" -> minimum: 10

  Do not return the value in rupees when the tender states
  the amount in crore or lakh.

  Extract the required financial years as the list parameter
  "years".

  If the tender says "last three financial years" but does not
  explicitly name the years, do not invent the financial years.
  Leave "years" empty unless the applicable years can be
  determined directly from the tender context.

- REQUIRED_DOCUMENT:
  Extract the required document name as "document_type".

- GST_STATUS:
  Extract the required GST registration status as "required_status".
  Normalize the status to uppercase.

- UDYAM_ELIGIBILITY:
  If the tender specifies allowed enterprise classifications such
  as Micro, Small, Medium, or a combination of them, extract them
  as "allowed_types": ["Micro", "Small", "Medium"].
  Preserve only classifications explicitly permitted by the tender.
  If the tender requires Udyam registration but does not specify
  allowed enterprise classifications, use an empty "allowed_types"
  list.

- EXPERIENCE_REQUIREMENT:
  Extract all explicitly stated experience conditions, such as
  minimum project count, minimum project value, required project
  type, and relevant time period.

  For "minimum_project_value":
  - Always return the numeric value in INR crore.
  - Do not include currency symbols or unit words in the value.

  Examples:
  - "5 crore" -> minimum_project_value: 5
  - "₹5 crore" -> minimum_project_value: 5
  - "Rs. 5 crore" -> minimum_project_value: 5
  - "500 lakh" -> minimum_project_value: 5
  - "₹50,000,000" -> minimum_project_value: 5

  For "minimum_projects":
  - Return the required number of projects as an integer.

  For "project_type":
  - Preserve the required project type as stated in the tender.

  For the experience time period:
  - Extract the number of required years as the numeric parameter
    "experience_years".
  - Example: "within the last 5 years" -> experience_years: 5.
  - Do not invent an experience period if none is stated.
  - Do not invent a reference date. The procurement workflow will
    provide the reference_date separately when needed.

  All monetary values used by the deterministic experience rule
  engine must be normalized to INR crore.
Never leave a parameter empty when the corresponding value is
explicitly stated in the tender text.
Do not invent parameter values.

Do not invent requirements or values that are not present in the tender.
If a requirement cannot be represented reliably using the supported rule
types, do not force it into an incorrect rule type. Add an explanation
to warnings instead.

The compliance engine, not the AI model, will make the final compliance
decision.

Tender text:
----------------
{tender_text}
----------------
""".strip()
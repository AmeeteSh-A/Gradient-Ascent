from pydantic import BaseModel, Field
from typing import List, Literal, Optional

# --- NEW: PRD Health Check Schema ---
class PRDHealthCheck(BaseModel):
    strengths: List[str] = Field(..., description="What the PRD did well (e.g., clear criteria).")
    blind_spots: List[str] = Field(..., description="What is missing, vague, or risky (e.g., missing latency metrics).")
    improvements: List[str] = Field(..., description="Actionable proposed fixes.")

class Epic(BaseModel):
    title: str = Field(..., description="High-level name for the feature.")
    description: str = Field(..., description="Brief description of the epic.")
    source_refs: List[str] = Field(..., description="Exact [REF-ID] tags from source.")

class UserStory(BaseModel):
    epic_title: str
    role: str
    action: str
    value: str
    acceptance_criteria: List[str]
    source_refs: List[str]

class ProductRequirements(BaseModel):
    health_check: PRDHealthCheck = Field(..., description="Automatic audit of the PRD quality.")
    epics: List[Epic]
    user_stories: List[UserStory]

class TestCase(BaseModel):
    story_action: str
    test_type: Literal["Positive", "Negative", "Edge Case"]
    scenario_description: str
    preconditions: List[str]
    steps_to_reproduce: List[str]
    expected_result: str
    source_refs: List[str]

class TestSuite(BaseModel):
    test_cases: List[TestCase]

class UnitTestCode(BaseModel):
    target_function: str
    pytest_code: str
    is_healed: bool = False
    healing_logs: List[str] = []
    vulnerabilities: List[str] = []
    linked_requirements: List[str] = []
    execution_time_ms: float = 0.0
    # --- NEW: Self-Refactoring Schema ---
    refactored_source: Optional[str] = Field(default=None, description="Cleaned, secure, and logical source code if bugs were detected.")
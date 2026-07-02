import json
import pytest

SCORECARD_SCHEMA = {
    "type": "object",
    "required": [
        "skill", "structural_score", "functional_score",
        "script_candidate", "script_score",
        "tier_actual", "tier_optimal",
        "legacy_format", "recommendations"
    ],
    "properties": {
        "skill": {"type": "string"},
        "structural_score": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "functional_score": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "script_candidate": {"type": "boolean"},
        "script_score": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "tier_actual": {"enum": ["high", "medium", "fast"]},
        "tier_optimal": {"enum": ["high", "medium", "fast"]},
        "legacy_format": {"type": "boolean"},
        "duplicates": {"type": "array", "items": {"type": "string"}},
        "external_deps": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["tool"],
                "properties": {
                    "tool": {"type": "string"},
                    "pinned": {"type": "boolean"},
                    "fallback": {"type": "boolean"}
                }
            }
        },
        "recommendations": {"type": "array", "items": {"type": "string"}}
    }
}


def validate_scorecard(entry):
    assert isinstance(entry, dict), "Scorecard must be a dict"
    for field in SCORECARD_SCHEMA["required"]:
        assert field in entry, f"Missing required field: {field}"
    assert 0.0 <= entry["structural_score"] <= 1.0
    assert 0.0 <= entry["functional_score"] <= 1.0
    assert 0.0 <= entry["script_score"] <= 1.0
    assert entry["tier_actual"] in ("high", "medium", "fast")
    assert entry["tier_optimal"] in ("high", "medium", "fast")
    assert isinstance(entry["script_candidate"], bool)
    assert isinstance(entry["legacy_format"], bool)
    assert isinstance(entry["recommendations"], list)


class TestScorecardSchema:
    def test_valid_minimal_scorecard(self):
        entry = {
            "skill": "test-skill",
            "structural_score": 1.0,
            "functional_score": 0.85,
            "script_candidate": False,
            "script_score": 0.15,
            "tier_actual": "high",
            "tier_optimal": "high",
            "legacy_format": False,
            "recommendations": ["Add test"],
        }
        validate_scorecard(entry)

    def test_full_scorecard_with_duplicates_and_deps(self):
        entry = {
            "skill": "test-skill",
            "structural_score": 0.5,
            "functional_score": 0.6,
            "script_candidate": True,
            "script_score": 0.75,
            "tier_actual": "high",
            "tier_optimal": "fast",
            "legacy_format": True,
            "duplicates": ["other-skill"],
            "external_deps": [{"tool": "yt-dlp", "pinned": False, "fallback": False}],
            "recommendations": ["Extract to script"],
        }
        validate_scorecard(entry)

    def test_invalid_tier_rejected(self):
        with pytest.raises(AssertionError):
            entry = {
                "skill": "bad",
                "structural_score": 1.0,
                "functional_score": 1.0,
                "script_candidate": False,
                "script_score": 0.0,
                "tier_actual": "ultra",
                "tier_optimal": "high",
                "legacy_format": False,
                "recommendations": [],
            }
            validate_scorecard(entry)

    def test_score_out_of_range_rejected(self):
        with pytest.raises(AssertionError):
            entry = {
                "skill": "bad",
                "structural_score": 1.5,
                "functional_score": 1.0,
                "script_candidate": False,
                "script_score": 0.0,
                "tier_actual": "high",
                "tier_optimal": "high",
                "legacy_format": False,
                "recommendations": [],
            }
            validate_scorecard(entry)

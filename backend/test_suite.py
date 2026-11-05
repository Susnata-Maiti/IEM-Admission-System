"""
Automated Test Suite for IEM Admission System
Runs Unit, Basis Path, BVA, and Integration Tests
Verifies test cases outlined in the Software Test Strategy & Plan Document.
"""

import unittest
from workflow import validate_status_transition
from auth import validate_password_strength
from database import hash_password, verify_password


class TestPasswordValidation(unittest.TestCase):
    """B.6 Equivalence Partitioning & Boundary Tests for Password Validation (FR-01)"""

    def test_valid_password(self):
        valid, msg = validate_password_strength("Student@2026!")
        self.assertTrue(valid)

    def test_short_password(self):
        valid, msg = validate_password_strength("Ab1!")
        self.assertFalse(valid)
        self.assertIn("at least 8 characters", msg)

    def test_missing_uppercase(self):
        valid, msg = validate_password_strength("student@2026!")
        self.assertFalse(valid)
        self.assertIn("uppercase letter", msg)

    def test_missing_special_char(self):
        valid, msg = validate_password_strength("Student2026")
        self.assertFalse(valid)
        self.assertIn("special character", msg)


class TestBasisPathWorkflow(unittest.TestCase):
    """
    B.8 White-Box Basis Path Testing for `validate_status_transition`
    Tests all linearly independent basis paths derived from the Control Flow Graph.
    """

    def test_path_1_same_status(self):
        # Path 1: 1 -> 2 -> 3 (Error: same status)
        valid, reason = validate_status_transition("Submitted", "Submitted")
        self.assertFalse(valid)
        self.assertIn("already in status", reason)

    def test_path_2_draft_to_submitted(self):
        # Path 2: 1 -> 2 -> 4 -> 5 -> 6 (Valid submission)
        valid, reason = validate_status_transition("Draft", "Submitted")
        self.assertTrue(valid)

    def test_path_3_draft_to_invalid(self):
        # Path 3: 1 -> 2 -> 4 -> 5 -> 7 (Invalid from Draft)
        valid, reason = validate_status_transition("Draft", "Accepted")
        self.assertFalse(valid)
        self.assertIn("only be transitioned to 'Submitted'", reason)

    def test_path_4_submitted_to_under_review(self):
        # Path 4: 1 -> 2 -> 4 -> 8 -> 9 -> 10 (Valid move to review)
        valid, reason = validate_status_transition("Submitted", "Under Review")
        self.assertTrue(valid)

    def test_path_5_submitted_to_rejected_with_remarks(self):
        # Path 5: 1 -> 2 -> 4 -> 8 -> 9 -> 11 -> 12 -> 13 (Valid rejection with remarks)
        valid, reason = validate_status_transition("Submitted", "Rejected", "Incomplete documents")
        self.assertTrue(valid)

    def test_path_6_submitted_to_rejected_without_remarks(self):
        # Path 6: 1 -> 2 -> 4 -> 8 -> 9 -> 11 -> 12 -> 14 (Invalid: missing remarks)
        valid, reason = validate_status_transition("Submitted", "Rejected", "")
        self.assertFalse(valid)
        self.assertIn("requires explanatory remarks", reason)

    def test_path_7_submitted_to_invalid(self):
        # Path 7: 1 -> 2 -> 4 -> 8 -> 9 -> 11 -> 15 (Invalid: e.g. Submitted -> Accepted directly)
        valid, reason = validate_status_transition("Submitted", "Accepted")
        self.assertFalse(valid)
        self.assertIn("only transition to 'Under Review' or 'Rejected'", reason)

    def test_path_8_under_review_to_accepted(self):
        # Path 8: 1 -> 2 -> 4 -> 8 -> 16 -> 17 -> 18 (Valid decision)
        valid, reason = validate_status_transition("Under Review", "Accepted", "Merit cleared")
        self.assertTrue(valid)

    def test_path_9_under_review_to_invalid(self):
        # Path 9: 1 -> 2 -> 4 -> 8 -> 16 -> 17 -> 19 (Invalid target from review)
        valid, reason = validate_status_transition("Under Review", "Draft")
        self.assertFalse(valid)
        self.assertIn("only transition to 'Accepted' or 'Rejected'", reason)

    def test_path_10_terminal_state_modification(self):
        # Path 10: 1 -> 2 -> 4 -> 8 -> 16 -> 20 (Terminal state modification blocked)
        valid, reason = validate_status_transition("Accepted", "Under Review")
        self.assertFalse(valid)
        self.assertIn("Terminal state", reason)


class TestScoreBoundaryValues(unittest.TestCase):
    """B.6 Boundary Value Analysis for Marks/Entrance Scores (0.0% to 100.0%)"""

    def validate_score(self, score: float) -> bool:
        return 0.0 <= score <= 100.0

    def test_bva_scores(self):
        # Lower boundary
        self.assertFalse(self.validate_score(-0.1))  # Below min
        self.assertTrue(self.validate_score(0.0))    # Min
        self.assertTrue(self.validate_score(0.1))    # Just above min

        # Nominal
        self.assertTrue(self.validate_score(60.0))   # Mid

        # Upper boundary
        self.assertTrue(self.validate_score(99.9))   # Just below max
        self.assertTrue(self.validate_score(100.0))  # Max
        self.assertFalse(self.validate_score(100.1)) # Above max


class TestCryptoSecurity(unittest.TestCase):
    """NFR-02 Security: Salted Hash Verification"""

    def test_salted_hash_uniqueness(self):
        pwd = "TestPassword@123"
        h1, s1 = hash_password(pwd)
        h2, s2 = hash_password(pwd)
        # Even with same password, salts must differ
        self.assertNotEqual(s1, s2)
        self.assertNotEqual(h1, h2)
        # Both must verify correctly against their respective salt
        self.assertTrue(verify_password(pwd, s1, h1))
        self.assertTrue(verify_password(pwd, s2, h2))
        self.assertFalse(verify_password("WrongPassword!", s1, h1))


if __name__ == "__main__":
    unittest.main()

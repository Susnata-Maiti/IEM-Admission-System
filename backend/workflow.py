"""
Workflow state machine for IEM Admission System
Enforces business rules on status transitions (Module 3 of MEAN POC & Section B.8 of Test Plan).
"""

VALID_STATUSES = ["Draft", "Submitted", "Under Review", "Accepted", "Rejected"]

def validate_status_transition(current_status: str, new_status: str, remarks: str = "") -> tuple[bool, str]:
    """
    Validates state machine transitions for admission applications.
    Node 1: Start validation
    """
    # Decision 1 (Node 2): Is new status same as current status?
    if current_status == new_status:
        # Node 3: No-op error
        return False, f"Application is already in status '{current_status}'"

    # Decision 2 (Node 4): Is current status 'Draft'?
    if current_status == "Draft":
        # Decision 3 (Node 5): Is new status 'Submitted'?
        if new_status == "Submitted":
            # Node 6: Valid submission
            return True, "Draft application successfully submitted"
        else:
            # Node 7: Invalid transition from Draft
            return False, "A Draft application can only be transitioned to 'Submitted'"

    # Decision 4 (Node 8): Is current status 'Submitted'?
    if current_status == "Submitted":
        # Decision 5 (Node 9): Is new status 'Under Review'?
        if new_status == "Under Review":
            # Node 10: Valid move to review
            return True, "Application placed Under Review"
        # Decision 6 (Node 11): Is new status 'Rejected'?
        elif new_status == "Rejected":
            # Decision 7 (Node 12): Does it have remarks?
            if remarks and remarks.strip():
                # Node 13: Valid direct rejection with remark
                return True, "Application rejected directly with remarks"
            else:
                # Node 14: Direct rejection requires remarks
                return False, "Rejection from 'Submitted' requires explanatory remarks"
        else:
            # Node 15: Invalid target from Submitted
            return False, "A 'Submitted' application can only transition to 'Under Review' or 'Rejected'"

    # Decision 8 (Node 16): Is current status 'Under Review'?
    if current_status == "Under Review":
        # Decision 9 (Node 17): Is new status 'Accepted' or 'Rejected'?
        if new_status in ["Accepted", "Rejected"]:
            # Node 18: Valid decision
            return True, f"Application successfully marked as {new_status}"
        else:
            # Node 19: Invalid target from Under Review
            return False, "An application 'Under Review' can only transition to 'Accepted' or 'Rejected'"

    # Node 20: Terminal state reached (Accepted or Rejected)
    return False, f"Terminal state '{current_status}' cannot be modified"

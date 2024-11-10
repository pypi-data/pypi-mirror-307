from django.conf import settings


DEFAULT_INITIAL_STATUS = 'PENDING'
DEFAULT_COMPLETED_STATUS = 'APPROVED'

DEFAULT_ACTIONS = {
    'APPROVE': 'Approve',
    'REJECT': 'Reject',
}

DEFAULT_STATUSES = {
    'PENDING': 'Pending',
    'APPROVED': 'Approved',
    'REJECTED': 'Rejected',
    'FAILED': 'Failed',
}

DEFAULT_TRANSITIONS = {
    'APPROVE': {
        'PENDING': 'APPROVED',
    },
    'REJECT': {
        'PENDING': 'REJECTED',
    },
}

APPROVAL_ACTIONS = getattr(settings, 'APPROVAL_ACTIONS', DEFAULT_ACTIONS)
APPROVAL_STATUSES = getattr(settings, 'APPROVAL_STATUSES', DEFAULT_STATUSES)
APPROVAL_TRANSITIONS = getattr(settings, 'APPROVAL_TRANSITIONS', DEFAULT_TRANSITIONS)
APPROVAL_INITIAL_STATUS = getattr(settings, 'APPROVAL_INITIAL_STATUS', DEFAULT_INITIAL_STATUS)
APPROVAL_COMPLETED_STATUS = getattr(settings, 'APPROVAL_COMPLETED_STATUS', DEFAULT_COMPLETED_STATUS)

for action, transitions in APPROVAL_TRANSITIONS.items():
    if action not in APPROVAL_ACTIONS:
        raise ValueError(f"Transition action '{action}' is not defined in APPROVAL_ACTIONS.")

    for current_status, next_status in transitions.items():
        if current_status not in APPROVAL_STATUSES:
            raise ValueError(
                f"Invalid current status '{current_status}' in transitions for action '{action}'."
            )
        if next_status not in APPROVAL_STATUSES:
            raise ValueError(
                f"Invalid next status '{next_status}' in transitions for action '{action}'."
            )

if APPROVAL_INITIAL_STATUS not in APPROVAL_STATUSES:
    raise ValueError(
        f"APPROVAL_INITIAL_STATUS '{APPROVAL_INITIAL_STATUS}' is not a valid status in APPROVAL_STATUSES."
    )

if APPROVAL_COMPLETED_STATUS not in APPROVAL_STATUSES:
    raise ValueError(
        f"APPROVAL_COMPLETED_STATUS '{APPROVAL_COMPLETED_STATUS}' is not a valid status in APPROVAL_STATUSES."
    )


TRANSITION_CHOICES = {}
for action, transitions in APPROVAL_TRANSITIONS.items():
    for state, next_state in transitions.items():
        TRANSITION_CHOICES.setdefault(state, []).append(action)

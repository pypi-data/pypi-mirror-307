# djangoapprove

`djangoapprove` is a Django module that introduces an approval workflow for CRUD operations. It provides a flexible and extensible way to intercept model operations, pause them for approval, and execute them once approved.


## Features

- **Approval Workflow**: Create, update, or delete operations are paused until explicitly approved or rejected.
- **Customizable States and Transitions**: Define your own approval statuses and state transitions.
- **Model Integration**: Easily integrate with existing Django models using the `ApprovalMixin`.
- **Flexible Settings**: Configure transitions, statuses, and actions through Django settings.
- **Lightweight**: Simple to integrate, with minimal dependencies.

## Installation

1. Install using `pip`:
   ```bash
   pip install djangoapprove
   ```
2. Add `djangoapprove` to your `INSTALLED_APPS` in `settings.py`:
```python
INSTALLED_APPS = [
    ...,
    'djangoapprove',
]
```
3. Run migrations to create the Approval model table:
```bash
python manage.py migrate
```

## Usage

### Basic Integration
To integrate `djangoapprove` with a model, use the `ApprovalMixin`:
```python
from django.db import models
from djangoapprove.mixins import ApprovalMixin

class MyModel(models.Model, ApprovalMixin):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def get_unique_key(self):
        return f"mymodel-{self.pk or some_unique_property}"
```

---
### Approving Requests

Once an operation is intercepted, it creates an Approval record. Approvals can be reviewed and transitioned to the next state (e.g., APPROVED).

```python
from djangoapprove.models import Approval

# Approve a pending request
approval = Approval.objects.get(pk=1)
approval.transition("APPROVE")
```

---
### Settings

You can customize states, transitions, and initial/completed statuses in your `settings.py`:

```python
APPROVAL_ACTIONS = {
    "APPROVE": "Approve",
    "REJECT": "Reject",
}

APPROVAL_STATUSES = {
    "PENDING": "Pending",
    "APPROVED": "Approved",
    "REJECTED": "Rejected",
    "FAILED": "Failed",
}

APPROVAL_TRANSITIONS = {
    "APPROVE": {"PENDING": "APPROVED"},
    "REJECT": {"PENDING": "REJECTED"},
}

APPROVAL_INITIAL_STATUS = "PENDING"
APPROVAL_COMPLETED_STATUS = "APPROVED"
```

---

### Example: Approval Workflow

1. Intercept Save Operation:
```python
instance = MyModel(name="Example", description="This is a test.")
approval = instance.save()  # Does not save immediately
```

2. Review The Approval:
```python
# Fetch the pending approval
approval = Approval.objects.filter(status="PENDING").first()
print(approval.data)  # View the data payload
```

3. Approve The Request:
```python
approval.transition("APPROVE")
```

4. Verify Execution:
```python
# The instance should now be created
instance = MyModel.objects.get(name="Example")
```

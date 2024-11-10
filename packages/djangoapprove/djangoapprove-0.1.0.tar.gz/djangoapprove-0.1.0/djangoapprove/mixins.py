import json

from django.core.serializers import serialize

from djangoapprove.settings import (
    APPROVAL_COMPLETED_STATUS,
)
from djangoapprove.models import Approval


class ApprovalMixin:
    """
    Mixin to intercept Model operations and introduce an Approval flow.
    """
    def get_unique_key(self):
        """
        Get a unique key for the model instance.
        """
        raise NotImplementedError("Method get_unique_key must be implemented.")

    def validate_approval_status(self, *args, **kwargs):
        """
        Validate if the incoming operation.
        """
        # check if there is already an Approval request for this request
        approval = Approval.objects.filter(  # pylint: disable=no-member
            unique_key=self.get_unique_key(),
            model_name=self._meta.model_name,
            request_type=Approval.REQUEST_SAVE,
        ).first()

        if approval is not None:
            if approval.status == APPROVAL_COMPLETED_STATUS:
                raise ValueError("Approval request already completed.")
            else:
                raise ValueError(
                    f"Approval request still in progress. Current status: {approval.status}"
                )

    def save(self, *args, **kwargs):
        """
        Intercept the save operation and create an approval request.
        """
        self.validate_approval_status()

        request_subtype = None
        if self.pk is not None:
            request_subtype = Approval.REQUEST_UPDATE

        data = self._serialize_instance(self)

        approval = Approval.objects.create(  # pylint: disable=no-member
            model_name=self._meta.model_name,
            request_type=Approval.REQUEST_SAVE,
            request_subtype=request_subtype,
            data=data,
        )

        return approval

    def delete(self, *args, **kwargs):
        """
        Intercept the delete operation and create an approval request.
        """
        self.validate_approval_status()

        data = self._serialize_instance(self)

        approval = Approval.objects.create(  # pylint: disable=no-member
            model_name=self._meta.model_name,
            request_type=Approval.REQUEST_DELETE,
            data=data,
        )

        return approval

    def serialize_instance(self, instance):
        """
        Serialize a single model instance to JSON.
        """
        return json.loads(serialize('json', [instance]))[0]['fields']

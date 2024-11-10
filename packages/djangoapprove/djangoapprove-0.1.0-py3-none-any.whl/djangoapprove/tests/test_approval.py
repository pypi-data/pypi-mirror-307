import unittest
from django.test import TestCase
from djangoapprove.tests import DummyModel, Approval


class ApprovalModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.dummy_instance = DummyModel.objects.create(name="Test Name", value=42)

    def test_create_instance(self):
        approval = Approval.objects.create(
            model_name="djangoapprove.DummyModel",
            request_type=Approval.REQUEST_SAVE,
            data={"fields": {"name": "New Instance", "value": 100}},
        )
        approval.transition("APPROVE")
        instance = DummyModel.objects.get(name="New Instance")
        self.assertEqual(instance.value, 100)

    def test_update_instance(self):
        approval = Approval.objects.create(
            model_name="djangoapprove.DummyModel",
            request_type=Approval.REQUEST_SAVE,
            request_subtype=Approval.REQUEST_UPDATE,
            data={"pk": self.dummy_instance.pk, "fields": {"name": "Updated Name", "value": self.dummy_instance.value}},
        )
        approval.transition("APPROVE")
        instance = DummyModel.objects.get(pk=self.dummy_instance.pk)
        self.assertEqual(instance.name, "Updated Name")


    def test_delete_instance(self):
        approval = Approval.objects.create(
            model_name="djangoapprove.DummyModel",
            request_type=Approval.REQUEST_DELETE,
            data={"pk": self.dummy_instance.pk},
        )
        approval.transition("APPROVE")
        with self.assertRaises(DummyModel.DoesNotExist):
            DummyModel.objects.get(pk=self.dummy_instance.pk)


# Run tests without requiring pytest or a separate test runner
if __name__ == "__main__":
    unittest.main()
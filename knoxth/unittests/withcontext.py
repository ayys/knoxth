from django.test import TestCase
from knoxth.auth import IsScoped
from knoxth.decorators import withContext
from rest_framework.viewsets import ReadOnlyModelViewSet


class WithContextTestCase(TestCase):
    def test_withcontext_without_parens(self):
        @withContext
        class DemoViewSet(ReadOnlyModelViewSet):
            ...
        DemoViewSet()

    def test_withcontext_with_empty_parens(self):
        @withContext()
        class DemoViewSet(ReadOnlyModelViewSet):
            ...
        DemoViewSet()

    def test_withcontext_with_parameters(self):
        @withContext(context="meow")
        class DemoViewSet(ReadOnlyModelViewSet):
            ...
        DemoViewSet()

    def test_withcontext_without_parens_has_same_name(self):
        @withContext
        class DemoViewSet(ReadOnlyModelViewSet):
            ...
        self.assertEqual(DemoViewSet.__name__, "DemoViewSet")

    def test_withcontext_with_empty_parens_has_same_name(self):
        @withContext()
        class DemoViewSet(ReadOnlyModelViewSet):
            ...
        self.assertEqual(DemoViewSet.__name__, "DemoViewSet")

    def test_withcontext_with_parameters_has_same_name(self):
        @withContext(context="meow")
        class DemoViewSet(ReadOnlyModelViewSet):
            ...
        self.assertEqual(DemoViewSet.__name__, "DemoViewSet")


    def test_withcontext_without_parens_has_scoped_permission(self):
        @withContext
        class DemoViewSet(ReadOnlyModelViewSet):
            ...
        self.assertIn(IsScoped, DemoViewSet().permission_classes)

    def test_withcontext_with_empty_parens_has_scoped_permission(self):
        @withContext()
        class DemoViewSet(ReadOnlyModelViewSet):
            ...
        self.assertIn(IsScoped, DemoViewSet().permission_classes)

    def test_withcontext_with_parameters_has_scoped_permission(self):
        @withContext(context="meow")
        class DemoViewSet(ReadOnlyModelViewSet):
            ...
        self.assertIn(IsScoped, DemoViewSet().permission_classes)

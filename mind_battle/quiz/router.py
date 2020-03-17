from rest_framework_extensions.routers import DefaultRouter, NestedRouterMixin


class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass

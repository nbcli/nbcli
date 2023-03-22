"""Default views for models in tenancy app."""

from nbcli.views.tools import BaseView


class TenancyTenantGroupsView(BaseView):
    """Default view for Tenant Groups."""

    def table_view(self):
        """Define columns for Tenant Groups."""
        self.add_col("Name", self.get_attr("name"))
        self.add_col("Tenants", self.get_attr("tenant_count"))
        self.add_col("Slug", self.get_attr("slug"))


class TenancyTenantsView(BaseView):
    """Default view for Tenants."""

    def table_view(self):
        """Define columns for Tenants."""
        self.add_col("Name", self.get_attr("name"))
        self.add_col("Group", self.get_attr("group"))
        self.add_col("Description", self.get_attr("description"))

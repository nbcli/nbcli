"""Default views for models in extras app."""

from nbcli.views.tools import BaseView


class ExtrasConfigContextsView(BaseView):
    """Default view for Config Contexts."""

    def table_view(self):
        """Define columns for Config Contexts."""
        self.add_col("Name", self.get_attr("name"))
        self.add_col("Weight", self.get_attr("weight"))
        self.add_col("Active", self.get_attr("is_active"))
        self.add_col("Description", self.get_attr("description"))


class ExtrasObjectChangesView(BaseView):
    """Default view for Object Changes."""

    def table_view(self):
        """Define columns for Object Changes."""
        self.add_col("Time", self.get_attr("time").split(".")[0].replace("T", " "))
        self.add_col("User", self.get_attr("user.username"))
        self.add_col("Action", self.get_attr("action"))
        self.add_col("Type", self.get_attr("changed_object_type").split(".")[-1])
        self.add_col("Object", self.get_attr("changed_object"))
        self.add_col("RequestID", self.get_attr("request_id"))

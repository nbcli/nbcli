"""Search sub command to emulate Netbox main search bar."""

from concurrent.futures import ThreadPoolExecutor

from nbcli.commands.base import BaseSubCommand
from nbcli.core.utils import app_model_by_loc, rs_limit
from nbcli.views.tools import nbprint
from pynetbox.core.query import RequestError


class SearchSubCommand(BaseSubCommand):
    """Search Netbox objects with the given searchterm.

    The List of search objects can be modified in:
    $CONF_DIR/user_config.yml
    """

    name = "search"
    parser_kwargs = dict(help="Search Netbox Objects")

    def setup(self):
        """Add parser arguments to search sub command."""
        self.parser.add_argument("obj_type", type=str, nargs="?", help="Object type to search")

        self.parser.add_argument("searchterm", help="Search term")

    def run(self):
        """Run a search of Netbox objects and show a table view of results.

        Usage Examples:

        - Search all object types for 'server1':
          $ nbcli search server1

        - Search the interface object type for 'eth 1':
          $ nbcli search interface 'eth 1'
        """
        if hasattr(self.netbox.nbcli.conf, "nbcli") and (
            "search_objects" in self.netbox.nbcli.conf.nbcli.keys()
        ):
            self.search_objects = self.netbox.nbcli.conf.nbcli["search_objects"]
        else:
            self.search_objects = [
                "provider",
                "circuit",
                "site",
                "rack",
                "location",
                "device_type",
                "device",
                "virtual_chassis",
                "cable",
                "power_feed",
                "vrf",
                "aggregate",
                "prefix",
                "address",
                "vlan",
                "tenant",
                "cluster",
                "virtual_machine",
            ]

        self.nbprint = nbprint

        if self.args.obj_type:
            modellist = [self.args.obj_type]
        else:
            modellist = self.search_objects

        self.result_count = 0
        self.results = list()

        max_workers = self.netbox.nbcli.conf.nbcli.get("max_workers", 4)

        if self.netbox.threading:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                self.results = executor.map(self.search_model, modellist)
        else:
            for obj_type in modellist:
                self.results.append(self.search_model(obj_type))

        self.results = [r for r in self.results if r != ""]

        if self.result_count == 0:
            self.logger.warning("No results found")
        else:
            print("")
            for result in self.results:
                print(f"{result}\n")

    def search_model(self, obj_type):
        """Search for given model for search term."""
        result_str = ""

        try:
            model = app_model_by_loc(self.netbox, obj_type)
            result = rs_limit(model.filter(self.args.searchterm), 15)
            full_count = model.count(self.args.searchterm)
            if len(result) > 0:
                self.result_count += 1
                result_str += f"{obj_type.title()}\n{'=' * len(obj_type)}\n"
                result_str += self.nbprint(result, string=True)
                if len(result) < full_count:
                    result_str += f"\n*** See all {full_count} results: "
                    result_str += f"'$nbcli filter {obj_type} {self.args.searchterm} --dl' ***"

        except (RequestError, AssertionError) as err:
            self.logger.warning('No API endpoint found for "%s".', obj_type)
            self.logger.warning(err)

        return result_str

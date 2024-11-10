from collections import Counter

from rich.text import Text

from abacura.plugins import Plugin, command
from abacura.utils.renderables import tabulate, AbacuraPanel, AbacuraWarning, OutputColors


class PluginHelper(Plugin):
    """Provides #plugin command"""

    def show_all_plugins(self):
        plugin_rows = []

        for name, plugin in self.session.plugin_loader.plugins.items():
            registrations = self.director.get_registrations_for_object(plugin)
            counts = Counter([r.registration_type for r in registrations])

            base = plugin.__class__.__base__.__name__
            indicator = '✓' if plugin.register_actions else 'x'
            indicator_color = "bold green" if plugin.register_actions else 'bold red'
            plugin_rows.append((base, plugin.get_name(), plugin.get_help() or '',
                                Text(indicator, style=indicator_color), counts))

        rows = []
        for base, name, doc, indicator, counts in sorted(plugin_rows):
            rows.append((base, name, doc, indicator,
                         counts["action"], counts["command"], counts["event"], counts["ticker"]))
        tbl = tabulate(rows, headers=["Type", "Name", "Description", "Register Actions",
                                      "# Actions", "# Commands", "# Events", "# Tickers"])
        self.output(AbacuraPanel(tbl, title="Loaded Plugins"))

    def show_failures(self):
        rows = [(m.relative_filename, str(m.exceptions)) for m in self.session.plugin_loader.get_failed_modules()]

        if len(rows) == 0:
            return

        tbl = tabulate(rows, headers=["Filename", "Errors"])
        self.output(AbacuraWarning(tbl, title="Failed Package Loads"))

    @command
    def plugins(self, name: str = '') -> None:
        """
        Get information about plugins

        :param name: Show details about a single plugin, leave blank to list all
        """
        if not name:
            self.show_all_plugins()
            self.show_failures()
            return

        loaded_plugins: dict[str, Plugin] = self.session.plugin_loader.plugins
        matches = [n for n in loaded_plugins.keys() if n.lower().startswith(name.lower())]
        exact = [n for n in loaded_plugins.keys() if n.lower() == name.lower()]

        if len(exact) == 1:
            matches = exact
        elif len(matches) > 1:
            self.session.show_warning(f"Ambiguous Plugin Name: '{name}'")
            return
        elif len(matches) == 0:
            self.session.show_warning(f"No plugin named '{name}'")
            return

        loaded_plugin: Plugin = loaded_plugins[matches[0]]
        plugin_module = self.session.plugin_loader.plugin_modules[loaded_plugin._source_filename]

        registrations = self.director.get_registrations_for_object(loaded_plugin)

        rows = []
        for r in registrations:
            rows.append((r.registration_type, r.name, r.callback.__qualname__, r.details))

        tbl = tabulate(rows, headers=["Type", "Name", "Callback", "Details"], title=f"Registered Callbacks")

        self.output(AbacuraPanel(tbl, title=f"{plugin_module.import_path}.{loaded_plugin.get_name()}"))

    @command
    def reload(self):
        """
        Reload plugins that have been modified or added.  Unload plugins that have been deleted.
        """

        results = self.session.plugin_loader.reload_plugins()

        rows = []
        for result in results:
            color = OutputColors.success
            if len(result.exceptions) > 0:
                color = OutputColors.error
            elif result.plugin_count == 0:
                continue
            elif result.last_action == "unloaded":
                color = OutputColors.warning

            rows.append((f"[{color}]{result.last_action}", result.import_path, [str(e) for e in result.exceptions]))

        if len(rows):
            tbl = tabulate(rows, headers=["Action", "Plugin Filename", "Errors"])
        else:
            tbl = Text("No plugins reloaded.")

        self.output(AbacuraPanel(tbl, title="Plugin Reload"))

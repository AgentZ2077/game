
import importlib

class ToolChainExecutor:
    def __init__(self, tools_config):
        self.tools_config = tools_config

    def execute(self, tool_name, player_id):
        entry = self.tools_config.get(tool_name)
        if not entry:
            raise ValueError(f"Tool '{tool_name}' not found.")
        mod_path, class_name = entry["module"].rsplit(".", 1)
        mod = importlib.import_module(mod_path)
        klass = getattr(mod, class_name)
        instance = klass(player_id, **entry.get("params", {}))
        return instance.run()

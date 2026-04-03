class ToolRegistry:
    _registry = {}

    @classmethod
    def register(cls, agent_name: str, tools: list):
        cls._registry.setdefault(agent_name, []).extend(tools)

    @classmethod
    def get(cls, agent_name: str) -> list:
        return cls._registry.get(agent_name, [])

from langgraph_swarm import create_swarm
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from langmem import create_manage_memory_tool, create_search_memory_tool
from langgraph.store.memory import InMemoryStore
from langchain_core.tools import StructuredTool
from src.services.llm_service import llm_model_provider
from src.agents.prompts.sales_agent_prompt import get_sales_agent_prompt
from src.agents.prompts.exit_agent_prompt import get_exit_agent_prompt
from src.agents.factories.tool_factory import tool_factory
from src.utils.background_tasks import schedule_background_task
from src.services.llm.openai_embedding import OpenAIEmbeddingService
from src.utils.agent_utils import _background_manage, _background_search
from src.config.settings import get_config
from src.utils.logger import logger

embedding_service = OpenAIEmbeddingService()
config = get_config()

class AgentFactory:
    def __init__(self):
        self.model = llm_model_provider.model
        self.tool_factory = tool_factory
        self.embedding_model = embedding_service.get_embedding_model()

        def embed(texts):
            return self.embedding_model.embed_documents(texts)

        self.memory_store = InMemoryStore(index={"dims": config.embedding_dimension, "embed": embed})

        base_manage = create_manage_memory_tool(namespace=("ltm",), store=self.memory_store)
        base_search = create_search_memory_tool(namespace=("ltm",), store=self.memory_store)

        def manage_wrapper(data):
            schedule_background_task(_background_manage, self.memory_store, base_manage, data, name="bg-manage")
            return {"status": "scheduled"}

        def search_wrapper(data):
            schedule_background_task(_background_search, self.memory_store, base_search, data, name="bg-search")
            return {"status": "scheduled"}

        self.manage_memory_tool = StructuredTool.from_function(
            manage_wrapper,
            name=base_manage.name,
            description=base_manage.description,
            args_schema=base_manage.args_schema,
        )

        self.search_memory_tool = StructuredTool.from_function(
            search_wrapper,
            name=base_search.name,
            description=base_search.description,
            args_schema=base_search.args_schema,
        )

        self.__agents = {
            "sales_agent": get_sales_agent_prompt(),
            "exit_agent": get_exit_agent_prompt(),
        }

    def __create_agent(self, name: str):
        try:
            if name not in self.__agents:
                raise ValueError(f"Agent prompt not found for agent name: {name}")

            agent_tools = self.tool_factory.get_tools_for_agent(name)
            if not isinstance(agent_tools, list):
                raise TypeError(f"Tools for agent '{name}' must be a list, got {type(agent_tools)}")

            agent_tools.extend([self.manage_memory_tool, self.search_memory_tool])

            agent = create_react_agent(
                model=self.model,
                tools=agent_tools,
                prompt=self.__agents[name],
                name=name,
                store=self.memory_store,
            )

            return agent

        except Exception as e:
            logger.error(f"Failed to create agent '{name}': {e}", exc_info=True)
            raise RuntimeError(f"Failed to create agent '{name}'") from e

    def create_all_agents(self):
        agents = []
        for name in self.__agents:
            try:
                agent = self.__create_agent(name)
                agents.append(agent)
            except Exception as e:
                logger.error(f"AgentFactory stopped while creating '{name}': {e}", exc_info=True)
                raise
        return agents

    def create_swarm(self, default_active="sales_agent"):
        try:
            agents = self.create_all_agents()
            builder = create_swarm(agents, default_active_agent=default_active)
            return builder.compile(checkpointer=InMemorySaver())
        except Exception as e:
            logger.error(f"Failed to create swarm: {e}", exc_info=True)
            raise RuntimeError("Swarm creation failed") from e

agent_factory = AgentFactory()

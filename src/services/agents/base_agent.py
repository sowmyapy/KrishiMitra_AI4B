"""
Base agent class for all specialized agents
"""
import logging
from datetime import datetime
from typing import Any

from src.services.agents.knowledge_base import KnowledgeBase
from src.services.agents.tool_registry import ToolRegistry
from src.services.llm_factory import get_llm

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for all agents"""

    def __init__(
        self,
        name: str,
        role: str,
        tools: ToolRegistry,
        knowledge_base: KnowledgeBase
    ):
        """
        Initialize agent

        Args:
            name: Agent name
            role: Agent role/responsibility
            tools: Tool registry
            knowledge_base: Knowledge base
        """
        self.name = name
        self.role = role
        self.tools = tools
        self.knowledge_base = knowledge_base
        self.llm = get_llm()  # Use LLM factory
        self.conversation_history: list[dict] = []

        logger.info(f"Initialized {name} agent")

    def _build_system_prompt(self) -> str:
        """Build system prompt for agent"""
        return f"""You are {self.name}, an AI agent specialized in {self.role}.

Your responsibilities:
{self._get_responsibilities()}

Available tools:
{self._format_available_tools()}

Guidelines:
- Be precise and actionable in your recommendations
- Consider farmer's resources and constraints
- Prioritize farmer safety and crop health
- Explain your reasoning clearly
- Use tools when you need specific information
"""

    def _get_responsibilities(self) -> str:
        """Get agent-specific responsibilities (override in subclasses)"""
        return "General agricultural assistance"

    def _format_available_tools(self) -> str:
        """Format available tools for prompt"""
        tools_list = self.tools.list_tools()
        return "\n".join([f"- {t['name']}: {t['description']}" for t in tools_list])

    async def _call_llm(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Call LLM with messages

        Args:
            messages: Conversation messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens

        Returns:
            LLM response
        """
        try:
            return await self.llm.generate_completion(messages, temperature, max_tokens)
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise

    def _extract_tool_calls(self, response: str) -> list[dict]:
        """
        Extract tool calls from LLM response

        Args:
            response: LLM response text

        Returns:
            List of tool calls
        """
        # Simple parsing - in production, use function calling API
        tool_calls = []

        if "TOOL:" in response:
            lines = response.split("\n")
            for line in lines:
                if line.startswith("TOOL:"):
                    parts = line.replace("TOOL:", "").strip().split("(")
                    if len(parts) == 2:
                        tool_name = parts[0].strip()
                        # Simple argument parsing
                        tool_calls.append({
                            "tool": tool_name,
                            "args": {}
                        })

        return tool_calls

    def _execute_tool(self, tool_name: str, args: dict) -> Any:
        """
        Execute a tool

        Args:
            tool_name: Name of tool
            args: Tool arguments

        Returns:
            Tool result
        """
        try:
            tool = self.tools.get_tool(tool_name)
            result = tool(**args)
            logger.info(f"Executed tool {tool_name}")
            return result
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return {"error": str(e)}

    def think(self, context: dict[str, Any]) -> dict[str, Any]:
        """
        Agent reasoning process (override in subclasses)

        Args:
            context: Context information

        Returns:
            Agent's decision/recommendation
        """
        raise NotImplementedError("Subclasses must implement think()")

    def log_decision(
        self,
        decision: dict[str, Any],
        context: dict[str, Any],
        reasoning: str
    ):
        """
        Log agent decision for learning

        Args:
            decision: Decision made
            context: Context used
            reasoning: Reasoning process
        """
        log_entry = {
            "agent": self.name,
            "timestamp": datetime.utcnow().isoformat(),
            "decision": decision,
            "context": context,
            "reasoning": reasoning
        }

        # In production, store in database
        logger.info(f"Decision logged: {self.name}")

        return log_entry

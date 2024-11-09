import json
from typing import Generator, List, Callable, Union, Optional

from calute.clients import vInferenceChatCompletionClient, ChatMessage
from calute.clients.vinfrence.types import (
	ChatCompletionRequest,
	ChatCompletionResponse,
	ChatCompletionStreamResponse,
)
from calute.types import Agent, Response, AgentFunction, Result
from calute.utils import function_to_json

__CTX_VARS_NAME__ = "context_variables"


class Calute:
	def __init__(
		self,
		client: vInferenceChatCompletionClient,
		system_prefix: str = "You are",
		function_prefix: str = "You have access to these functions:",
		rules_prefix: str = "You must follow these rules:",
		context_prefix: str = "Current context:",
		history_prefix: str = "Previous conversation:",
	) -> None:
		self.client = client
		self.system_prefix = system_prefix
		self.function_prefix = function_prefix
		self.rules_prefix = rules_prefix
		self.context_prefix = context_prefix
		self.history_prefix = history_prefix

	def generate_function_section(self, functions: List[AgentFunction]) -> str:
		"""Generates the function documentation section using function_to_json conversion."""
		if not functions:
			return ""

		function_docs = []
		for func in functions:
			try:
				func_schema = function_to_json(func)
				func_info = func_schema["function"]

				doc = f"- {func_info['name']}: {func_info['description']}\n"
				func_info["parameters"]["properties"].pop(__CTX_VARS_NAME__, None)
				if func_info["parameters"]["properties"]:
					doc += "  Parameters:\n"
					for param_name, param_info in func_info["parameters"]["properties"].items():
						if param_name != __CTX_VARS_NAME__:
							required = param_name in func_info["parameters"].get("required", [])
							req_str = " (required)" if required else " (optional)"
							doc += f"    - {param_name}: {param_info['type']}{req_str}\n"

				function_docs.append(doc)
			except Exception:
				func_name = getattr(func, "__name__", str(func))
				function_docs.append(f"- {func_name}: Unable to parse function details\n")

		return f"\n{self.function_prefix}\n" + "\n".join(function_docs)

	def generate_rules_section(
		self, rules: Union[List[str], Callable[[], List[str]], None]
	) -> str:
		if not rules:
			return ""

		rules_list = rules() if callable(rules) else rules
		formatted_rules = "\n".join(f"{i+1}. {rule}" for i, rule in enumerate(rules_list))
		return f"\n{self.rules_prefix}\n{formatted_rules}"

	def generate_context_section(self, context_variables: Optional[dict]) -> str:
		if not context_variables:
			return ""

		formatted_vars = "\n".join(
			f"- {key}: {value}" for key, value in context_variables.items()
		)
		return f"\n{self.context_prefix}\n{formatted_vars}"

	def generate_tool_section(
		self, tool_choice: Optional[str], parallel_tool_calls: bool
	) -> str:
		if not tool_choice:
			return ""

		parallel_text = (
			"You can call multiple tools in parallel."
			if parallel_tool_calls
			else "Call tools sequentially."
		)
		return f"\nTool usage:\n- Mode: {tool_choice}\n- {parallel_text}"

	def generate_history_section(self, history: Optional[List[ChatMessage]]) -> str:
		"""Formats chat history into a readable conversation format."""
		if not history:
			return ""

		formatted_messages = []
		for msg in history:
			role_prefix = {"user": "User", "assistant": "Assistant", "system": "System"}.get(
				msg.role, msg.role.capitalize()
			)

			formatted_messages.append(f"{role_prefix}: {msg.content}")
		sep = "-" * 5
		return (
			f"\n{self.history_prefix}\n"
			+ sep
			+ "\n"
			+ "\n\n".join(formatted_messages)
			+ "\n"
			+ sep
		)

	def generate_prompt(
		self,
		agent: Agent,
		context_variables: Optional[dict] = None,
		history: Optional[List[ChatMessage]] = None,
	) -> str:
		"""
		Generates a complete prompt including agent configuration, context, and chat history.

		Args:
		    agent (Agent): The agent configuration
		    context_variables (Optional[dict]): Additional context variables
		    history (Optional[List[ChatMessage]]): Previous conversation history

		Returns:
		    str: Formatted prompt string
		"""
		if not agent:
			return "You are a helpful assistant."

		# Get base instructions
		instructions = (
			agent.instructions() if callable(agent.instructions) else agent.instructions
		)

		# Build prompt sections
		prompt_parts = [
			f"{self.system_prefix} {agent.name}.",
			instructions,
			self.generate_function_section(agent.functions),
			self.generate_tool_section(agent.tool_choice, agent.parallel_tool_calls),
			self.generate_context_section(context_variables),
			self.generate_history_section(history),
			self.generate_rules_section(agent.rules),
		]

		# Filter out empty sections and join with newlines
		return "\n\n".join(filter(lambda s: s != "", prompt_parts))

	def handle_function_result(self, result, debug) -> Result:
		match result:
			case Result() as result:
				return result

			case Agent() as agent:
				return Result(
					value=json.dumps({"assistant": agent.name}),
					agent=agent,
				)
			case _:
				try:
					return Result(value=str(result))
				except Exception as e:
					error_message = f"Failed to cast response to string: {result}. Make sure agent functions return a string or Result object. Error: {str(e)}"
					raise TypeError(error_message) from e

	def handle_tool_calls(
		self,
		tool_calls,
		functions: List[AgentFunction],
		context_variables: dict,
		debug: bool,
	) -> Response:
		function_map = {f.__name__: f for f in functions}
		partial_response = Response(messages=[], agent=None, context_variables={})

		for tool_call in tool_calls:
			name = tool_call.function.name
			# handle missing tool case, skip to next tool
			if name not in function_map:
				partial_response.messages.append(
					{
						"role": "tool",
						"tool_call_id": tool_call.id,
						"tool_name": name,
						"content": f"Error: Tool {name} not found.",
					}
				)
				continue
			args = json.loads(tool_call.function.arguments)

			func = function_map[name]
			if __CTX_VARS_NAME__ in func.__code__.co_varnames:
				args[__CTX_VARS_NAME__] = context_variables
			raw_result = function_map[name](**args)

			result: Result = self.handle_function_result(raw_result, debug)
			partial_response.messages.append(
				{
					"role": "tool",
					"tool_call_id": tool_call.id,
					"tool_name": name,
					"content": result.value,
				}
			)
			partial_response.context_variables.update(result.context_variables)
			if result.agent:
				partial_response.agent = result.agent

		return partial_response

	def create_response(
		self,
		agent: Agent,
		context_variables: Optional[dict] = None,
		history: Optional[List[ChatMessage]] = None,
		*,
		model: str,
		stream: bool = True,
	) -> Generator[
		Union[ChatCompletionStreamResponse, ChatCompletionResponse],
		None,
		None,
	]:
		prompt = self.generate_prompt(
			agent=agent,
			context_variables=context_variables,
			history=history,
		)
		return self.client.create_chat_completion(
			ChatCompletionRequest(
				model=model,
				stream=stream,
				messages=[ChatMessage(role="user", content=prompt)],
			)
		)

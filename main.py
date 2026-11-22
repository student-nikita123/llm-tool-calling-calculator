
# Group tools into a list and a lookup dictionary
from dataclasses import dataclass
from typing import Any

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage
from calculator_tools import add, divide, multiply, subtract

MODEL = "llama3.2"

tools = [add, subtract, multiply, divide]
tool_map = {t.name: t for t in tools}

llm = ChatOllama(model=MODEL, temperature=0)
llm_with_tools = llm.bind_tools(tools)


@dataclass(frozen=True)
class ToolExecution:
    name: str
    arguments: dict[str, Any]
    output: object


@dataclass(frozen=True)
class CalculatorResult:
    response: str
    tool_executions: tuple[ToolExecution, ...]


def run_calculator_query(user_query: str) -> CalculatorResult:
    if not user_query.strip():
        raise ValueError("Please enter a calculator question.")

    messages = [HumanMessage(content=user_query)]

    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)
    executions = []

    if ai_msg.tool_calls:
        for tool_call in ai_msg.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            selected_tool = tool_map.get(tool_name)
            if selected_tool is None:
                raise RuntimeError(f"The model requested an unknown tool: {tool_name}")

            tool_output = selected_tool.invoke(tool_args)
            executions.append(
                ToolExecution(
                    name=tool_name,
                    arguments=tool_args,
                    output=tool_output,
                )
            )

            messages.append(
                ToolMessage(content=str(tool_output), tool_call_id=tool_call["id"])
            )

        final_response = llm_with_tools.invoke(messages)
        response = str(final_response.content)
    else:
        response = str(ai_msg.content)

    return CalculatorResult(response=response, tool_executions=tuple(executions))


if __name__ == "__main__":
    for query in (
        "What is 145.5 minus 32.2?",
        "Can you divide 144 by 12?",
        "Find the answer of 125 * 5",
        "What happens if I divide 50 by 0?",
    ):
        result = run_calculator_query(query)
        print(f"User: {query}")
        print(f"Assistant: {result.response}\n")
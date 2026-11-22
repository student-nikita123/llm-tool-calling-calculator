import httpx
import streamlit as st
from ollama import ResponseError

from main import MODEL, run_calculator_query


st.set_page_config(page_title="LLM Tool Calculator", page_icon="🧮")
st.title("LLM Tool Calculator")
st.caption("Ask a question and the model will use calculator tools when needed.")

with st.sidebar:
    st.subheader("Configuration")
    st.write(f"**Model:** `{MODEL}`")
    st.markdown(
        "Make sure Ollama is running and the model is available. "
        "For example, run `ollama run llama3.2` in a terminal."
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("tool_executions"):
            with st.expander("Calculator tool calls"):
                for execution in message["tool_executions"]:
                    st.markdown(f"**{execution.name}**")
                    st.json(execution.arguments)
                    st.write(f"Result: {execution.output}")

prompt = st.chat_input("For example: What is 145.5 minus 32.2?")

if prompt is not None:
    if not prompt.strip():
        st.warning("Enter a question before submitting.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                with st.spinner("Calculating..."):
                    result = run_calculator_query(prompt)
                st.markdown(result.response)
                if result.tool_executions:
                    with st.expander("Calculator tool calls"):
                        for execution in result.tool_executions:
                            st.markdown(f"**{execution.name}**")
                            st.json(execution.arguments)
                            st.write(f"Result: {execution.output}")

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": result.response,
                        "tool_executions": result.tool_executions,
                    }
                )
            except httpx.HTTPError as error:
                message = (
                    "Could not connect to Ollama. Start the Ollama service and "
                    f"try again. Details: {error}"
                )
                st.error(message)
                st.session_state.messages.append(
                    {"role": "assistant", "content": message}
                )
            except ResponseError as error:
                message = (
                    f"Ollama returned an error: {error}. Confirm that `{MODEL}` "
                    "is installed with `ollama pull`."
                )
                st.error(message)
                st.session_state.messages.append(
                    {"role": "assistant", "content": message}
                )
            except ValueError as error:
                st.warning(str(error))

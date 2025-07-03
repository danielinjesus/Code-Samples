# from langchain_core.prompts import PromptTemplate
# prompt_template = PromptTemplate.from_template("Tellme a joke about {topic}")
# prompt_template.invoke({"topic": "cats"})

from langchain_core.prompts import ChatPromptTemplate
prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    ("user", "Tell me a joke about {topic}")
])
prompt_template.invoke({"topic":"cats"})
from typing import Type
from pydantic import BaseModel
from cognee.infrastructure.llm.prompts import  render_prompt
from cognee.infrastructure.llm.get_llm_client import get_llm_client

async def categorize_relevant_category(query: str, summary, response_model: Type[BaseModel]):
    llm_client = get_llm_client()

    enriched_query= render_prompt("categorize_categories.txt", {"query": query, "categories": summary})


    system_prompt = " Choose the relevant categories and return appropriate output based on the model"

    llm_output = await llm_client.acreate_structured_output(enriched_query, system_prompt, response_model)

    return llm_output.model_dump()

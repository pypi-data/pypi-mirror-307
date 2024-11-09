import os
import logging
import pathlib

from cognee import config
from cognee.api.v1.add import add
from cognee.api.v1.prune import prune
from cognee.api.v1.cognify.cognify_test_task import cognify
from cognee.infrastructure.databases.graph import get_graph_engine
from cognee.shared.utils import render_graph

logging.basicConfig(level = logging.DEBUG)

async def  main():

    data_directory_path = str(pathlib.Path(os.path.join(pathlib.Path(__file__).parent, ".data_storage/test_library")).resolve())
    config.data_root_directory(data_directory_path)
    cognee_directory_path = str(pathlib.Path(os.path.join(pathlib.Path(__file__).parent, ".cognee_system/test_library")).resolve())
    config.system_root_directory(cognee_directory_path)

    await prune.prune_data()
    await prune.prune_system(metadata = True)

    dataset_name = "user_data"

    ai_text_file_path = os.path.join(pathlib.Path(__file__).parent, "test_data/user_data_v1.csv")
    await add([ai_text_file_path], dataset_name)


    # await cognee.add([text], dataset_name)

    await cognify([dataset_name])

    # from cognee.infrastructure.databases.vector import get_vector_engine
    # vector_engine = get_vector_engine()
    # random_node = (await vector_engine.search("entities", "AI"))[0]
    # random_node_name = random_node.payload["name"]

    graph_client = await get_graph_engine()
    graph_url = await render_graph(graph_client.graph)
    print("GRAPH LINK WE GOT IS", graph_url)

    # search_results = await cognee.search("SIMILARITY", params = { "query": random_node_name })
    # assert len(search_results) != 0, "The search results list is empty."
    # print("\n\nExtracted sentences are:\n")
    # for result in search_results:
    #     print(f"{result}\n")

    # search_results = await cognee.search("TRAVERSE", params = { "query": random_node_name })
    # assert len(search_results) != 0, "The search results list is empty."
    # print("\n\nExtracted sentences are:\n")
    # for result in search_results:
    #     print(f"{result}\n")
    #
    # search_results = await cognee.search("SUMMARY", params = { "query": random_node_name })
    # assert len(search_results) != 0, "Query related summaries don't exist."
    # print("\n\nQuery related summaries exist:\n")
    # for result in search_results:
    #     print(f"{result}\n")
    #
    # search_results = await cognee.search("ADJACENT", params = { "query": random_node_name })
    # assert len(search_results) != 0, "Large language model query found no neighbours."
    # print("\n\nLarge language model query found neighbours.\n")
    # for result in search_results:
    #     print(f"{result}\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main(), debug=True)

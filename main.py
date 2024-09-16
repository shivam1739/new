from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import networkx as nx

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

class Pipeline(BaseModel):
    nodes: list
    edges: list

@app.post("/pipelines/parse")
async def parse_pipeline(pipeline: Pipeline):
    nodes = pipeline.nodes
    edges = pipeline.edges

    G = nx.DiGraph()

    nodes_with_attributes = [(node['id'], {k: v for k, v in node.items() if k != 'id'}) for node in nodes]
    G.add_nodes_from(nodes_with_attributes)

  
    edges_with_edges = [(edge['source'], edge['target']) for edge in edges]
    G.add_edges_from(edges_with_edges)

    num_nodes = len(G.nodes)
    num_edges = len(G.edges)
    is_dag = nx.is_directed_acyclic_graph(G)

    return {"num_nodes": num_nodes, "num_edges": num_edges, "is_dag": is_dag}

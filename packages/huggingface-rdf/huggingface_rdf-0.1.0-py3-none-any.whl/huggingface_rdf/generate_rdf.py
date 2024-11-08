from rdflib import Graph, Namespace, URIRef, Literal
import json
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def chunk_data(data, chunk_size):
    """Chunking data"""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]
            
def convert_to_rdf(data, output_file,base="http://fakebase"):
    """
    This function takes a JSON-serializable data structure, converts it to RDF using 
    JSON-LD format, and serializes it into Turtle format, saving it to the specified file.

    Args:
        data (dict): The JSON-serializable data structure to convert to RDF.
        output_file (str): The file path where the Turtle (.ttl) formatted RDF data will be saved.
        base (str): The base URI for the RDF graph, used as a prefix in generated RDF triples.
                    Defaults to "http://fakebase".

    Returns:
        str: A string representation of the RDF graph in Turtle format.
    """
    total_items = len(data)
    if total_items > 100:
        chunk_size = total_items // 100
    else:
        chunk_size = 1
    logging.info(f"Starting RDF conversion. Total items: {total_items}, Chunk size: {chunk_size}")

    g = Graph()

    with tqdm(total=total_items, desc="Parsing data") as pbar:
        for chunk in chunk_data(data, chunk_size):
            for item in chunk:
                item_json_ld = json.dumps(item)
                g.parse(data=item_json_ld, format='json-ld', base=URIRef(base))
                pbar.update(1)

    logging.info(f"RDF data being written to disk, this could take some time... {output_file}")
    # Implementation for generating RDF
    return g.serialize(destination=output_file, format='ttl')
    

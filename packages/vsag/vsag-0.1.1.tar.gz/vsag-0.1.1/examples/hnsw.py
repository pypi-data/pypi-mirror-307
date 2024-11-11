import vsag
import json

def hnsw_demo():
    dim = 2
    index_params = json.dumps({
        "dtype": "float32",
        "metric_type": "l2",
        "dim": dim,
        "hnsw": {
            "max_degree": 16,
            "ef_construction": 100
        }
    })
    index = vsag.Index("hnsw", index_params)
    index.add_vectors(vectors=[1,2,3,4,5,6], ids=[100,200,300], num_elements=3, dim=dim,)
    search_params = json.dumps({"hnsw": {"ef_search": 100}})
    res = index.knn_search(query=[1,6], k=10, params=search_params)
    print(res)

if __name__ == "__main__":
    hnsw_demo()

from vectordb import Memory

def load_vectordb(path):
    return Memory(chunking_strategy={"mode": "sliding_window", "window_size": 14, "overlap": 10}, memory_file=path)
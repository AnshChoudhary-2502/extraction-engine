from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def chunk_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=500,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_text(text)

def inspect_chunks(chunks, num_chunks=1000):
    print(f"\nTotal chunks: {len(chunks)}\n")

    for i, chunk in enumerate(chunks[:num_chunks]):
        print(f"--- Chunk {i} (length={len(chunk)}) ---")
        # print(chunk)
        print("\n")

if __name__ == "__main__":
    file_path = "testcase_1/stories/drstrange.txt"
    text = load_txt(file_path)
    chunks = chunk_text(text)
    inspect_chunks(chunks)

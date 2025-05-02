from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
from PIL import Image as PILImage
import math
import sys
import os
import json
import faiss
import numpy as np
from pathlib import Path
import requests
from markitdown import MarkItDown
import time
from models import AddInput, AddOutput, SqrtInput, SqrtOutput, StringsToIntsInput, StringsToIntsOutput, ExpSumInput, ExpSumOutput
from PIL import Image as PILImage
from tqdm import tqdm
import hashlib


mcp = FastMCP("Calculator")

EMBED_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"
CHUNK_SIZE = 256
CHUNK_OVERLAP = 40
ROOT = Path(__file__).parent.resolve()

# Define FAISS paths globally
INDEX_CACHE = ROOT / "faiss_index"
INDEX_CACHE.mkdir(exist_ok=True)
INDEX_FILE = INDEX_CACHE / "index.bin"
METADATA_FILE = INDEX_CACHE / "metadata.json"
CACHE_FILE = INDEX_CACHE / "doc_index_cache.json"

def get_embedding(text: str) -> np.ndarray:
    response = requests.post(EMBED_URL, json={"model": EMBED_MODEL, "prompt": text})
    response.raise_for_status()
    return np.array(response.json()["embedding"], dtype=np.float32)

def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()
    for i in range(0, len(words), size - overlap):
        yield " ".join(words[i:i+size])

def mcp_log(level: str, message: str) -> None:
    """Log a message to stderr to avoid interfering with JSON communication"""
    sys.stderr.write(f"{level}: {message}\n")
    sys.stderr.flush()

# --- Refactored FAISS Resource Handling ---

def load_faiss_resources():
    """Loads FAISS index, metadata, and cache from disk."""
    # Paths are now global, no need to define them here
    cache_meta = json.loads(CACHE_FILE.read_text()) if CACHE_FILE.exists() else {}
    metadata = json.loads(METADATA_FILE.read_text()) if METADATA_FILE.exists() else []
    index = faiss.read_index(str(INDEX_FILE)) if INDEX_FILE.exists() else None
    return index, metadata, cache_meta

def save_faiss_resources(index, metadata, cache_meta, index_file_path, metadata_file_path, cache_file_path):
    """Saves FAISS index, metadata, and cache to disk."""
    Path(cache_file_path).write_text(json.dumps(cache_meta, indent=2))
    Path(metadata_file_path).write_text(json.dumps(metadata, indent=2))
    if index and index.ntotal > 0:
        faiss.write_index(index, str(index_file_path))
        mcp_log("SUCCESS", "Saved FAISS index, metadata, and cache")
    else:
        mcp_log("WARN", "Index is empty or was not modified. Nothing saved to index.bin.")

# --- End Refactored FAISS Resource Handling ---

@mcp.tool()
def search_documents(query: str) -> list[str]:
    """Search for relevant content from uploaded documents."""
    ensure_faiss_ready()
    mcp_log("SEARCH", f"Query: {query}")
    try:
        # Use the loader function
        index, metadata, _ = load_faiss_resources()
        if index is None:
            return ["ERROR: Index not found or empty."]
        query_vec = get_embedding(query).reshape(1, -1)
        D, I = index.search(query_vec, k=5)
        results = []
        # Ensure metadata indices are valid
        valid_indices = [idx for idx in I[0] if 0 <= idx < len(metadata)]
        for idx in valid_indices:
            data = metadata[idx]
            results.append(f"{data['chunk']}\n[Source: {data.get('doc', 'Unknown Source')}, ID: {data.get('chunk_id', 'N/A')}]") # Use .get for safety
        return results
    except Exception as e:
        mcp_log("ERROR", f"Search failed: {str(e)}")
        return [f"ERROR: Failed to search: {str(e)}"]

@mcp.tool()
def add(input: AddInput) -> AddOutput:
    print("CALLED: add(AddInput) -> AddOutput")
    return AddOutput(result=input.a + input.b)

@mcp.tool()
def sqrt(input: SqrtInput) -> SqrtOutput:
    """Square root of a number"""
    print("CALLED: sqrt(SqrtInput) -> SqrtOutput")
    return SqrtOutput(result=input.a ** 0.5)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return int(a * b)

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> float:")
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> int:")
    return int(a ** b)


# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> float:")
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> int:")
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    print("CALLED: log(a: int) -> float:")
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    print("CALLED: remainder(a: int, b: int) -> int:")
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    print("CALLED: sin(a: int) -> float:")
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    print("CALLED: cos(a: int) -> float:")
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    print("CALLED: tan(a: int) -> float:")
    return float(math.tan(a))

# mine tool
@mcp.tool()
def mine(a: int, b: int) -> int:
    """special mining tool"""
    print("CALLED: mine(a: int, b: int) -> int:")
    return int(a - b - b)

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(input: StringsToIntsInput) -> StringsToIntsOutput:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(StringsToIntsInput) -> StringsToIntsOutput")
    ascii_values = [ord(char) for char in input.string]
    return StringsToIntsOutput(ascii_values=ascii_values)

@mcp.tool()
def int_list_to_exponential_sum(input: ExpSumInput) -> ExpSumOutput:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(ExpSumInput) -> ExpSumOutput")
    result = sum(math.exp(i) for i in input.int_list)
    return ExpSumOutput(result=result)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]

# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
    print("CALLED: review_code(code: str) -> str:")


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

def process_documents():
    """Process documents and create FAISS index"""
    mcp_log("INFO", "Indexing documents with MarkItDown...")
    DOC_PATH = ROOT / "documents"

    index, metadata, cache_meta = load_faiss_resources() # Use loader
    converter = MarkItDown()

    def file_hash(path):
        return hashlib.md5(Path(path).read_bytes()).hexdigest()

    files_processed = False
    for file in DOC_PATH.glob("*.*"):
        fhash = file_hash(file)
        # Use file.name as key for cache_meta for documents
        cache_key = file.name
        if cache_key in cache_meta and cache_meta[cache_key] == fhash:
            mcp_log("SKIP", f"Skipping unchanged file: {file.name}")
            continue

        mcp_log("PROC", f"Processing: {file.name}")
        try:
            result = converter.convert(str(file))
            markdown = result.text_content
            chunks = list(chunk_text(markdown))
            embeddings_for_file = []
            new_metadata = []
            for i, chunk in enumerate(tqdm(chunks, desc=f"Embedding {file.name}")):
                embedding = get_embedding(chunk)
                embeddings_for_file.append(embedding)
                # Store file name in 'doc' field
                new_metadata.append({"doc": file.name, "chunk": chunk, "chunk_id": f"{file.stem}_{i}"})

            if embeddings_for_file:
                if index is None:
                    dim = len(embeddings_for_file[0])
                    index = faiss.IndexFlatL2(dim)
                index.add(np.stack(embeddings_for_file))
                metadata.extend(new_metadata)
                cache_meta[cache_key] = fhash # Update cache
                files_processed = True
        except Exception as e:
            mcp_log("ERROR", f"Failed to process {file.name}: {e}")

    if files_processed:
        # Pass the global paths to the saver function
        save_faiss_resources(index, metadata, cache_meta, INDEX_FILE, METADATA_FILE, CACHE_FILE)
    else:
        mcp_log("INFO", "No new or updated documents to process.")

def index_url(url: str):
    """Fetches content from a URL, processes it, and adds to the FAISS index."""
    mcp_log("INFO", f"Attempting to index URL: {url}")
    index, metadata, cache_meta = load_faiss_resources()
    converter = MarkItDown()
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(options=options)
    try:
        # 1. Fetch URL content
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        # response = requests.get(url, headers=headers, timeout=30) # Add timeout
        driver.get(url)
        response = driver.page_source
        # mcp_log("PROC",f"Response for {url} is {response}")
        driver.quit()
        # return
        # response.raise_for_status() # Raise HTTP errors
        content_bytes = response.encode('utf-8') #.content
        content_type = "html"
        # content_type = response.headers.get('Content-Type', '').lower()
        mcp_log("PROC", f"content type for {url} is {content_type}")
        # 2. Calculate content hash
        content_hash = hashlib.md5(content_bytes).hexdigest()
        mcp_log("PROC", f"content hash for {url} is {content_hash}")

        # 3. Check cache
        # Use URL as the key in cache_meta for URLs
        cache_key = url
        if cache_key in cache_meta and cache_meta[cache_key] == content_hash:
            mcp_log("SKIP", f"Skipping unchanged URL: {url}")
            return "Skipping unchanged URL"# Already indexed and unchanged

        mcp_log("PROC", f"Processing URL: {url}")

        # 4. Convert to Markdown (Handle different content types)
        # For now, assume HTML or try plain text
        text_content = ""
        if 'html' in content_type:
             # Use MarkItDown directly with content string if possible,
             # or save to temp file if needed by converter API
             # Assuming MarkItDown can handle string input or needs path:
             # Option A: If MarkItDown handles string (ideal)
             # result = converter.convert_string(content_bytes.decode('utf-8', errors='ignore')) # Fictional method
             # Option B: Save to temp file (less ideal)
             import tempfile
             with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
                 temp_file.write(content_bytes)
                 temp_path = temp_file.name
             try:
                 result = converter.convert(temp_path)
                 text_content = result.text_content
             finally:
                 os.remove(temp_path) # Clean up temp file
        elif 'text' in content_type:
            text_content = content_bytes.decode('utf-8', errors='ignore')
        else:
            mcp_log("WARN", f"Skipping URL {url} due to unsupported content type: {content_type}")
            return "Error: skipping due to unsupported content"

        if not text_content:
             mcp_log("WARN", f"No text content extracted from URL: {url}")
             return "Error: No text context extracted"

        # 5. Chunk Text
        chunks = list(chunk_text(text_content))
        if not chunks:
             mcp_log("WARN", f"No text chunks generated for URL: {url}")
             return "Error: No text chunks"
        mcp_log("PROC", f"Number of chunks {len(chunks)}")
        #mcp_log("PROC", f"first chunk content is {chunks[0]}")
        # return
        # 6. Generate Embeddings
        embeddings_for_url = []
        new_metadata = []
        url_identifier = hashlib.md5(url.encode()).hexdigest()[:8] # Short ID for chunks
        for i, chunk in enumerate(tqdm(chunks, desc=f"Embedding {url}")):
            embedding = get_embedding(chunk)
            embeddings_for_url.append(embedding)
            # Store URL in 'doc' field for metadata
            new_metadata.append({"doc": url, "chunk": chunk, "chunk_id": f"url_{url_identifier}_{i}"})

        # 7. Update FAISS Index and Metadata
        if embeddings_for_url:
            if index is None:
                dim = len(embeddings_for_url[0])
                index = faiss.IndexFlatL2(dim)
            index.add(np.stack(embeddings_for_url))
            metadata.extend(new_metadata)
            cache_meta[cache_key] = content_hash # Update cache with new hash

            # 8. Save Resources
            # Pass the global paths to the saver function
            save_faiss_resources(index, metadata, cache_meta, INDEX_FILE, METADATA_FILE, CACHE_FILE)
            return "Indexing successful"
        else:
             mcp_log("WARN", f"No embeddings generated for URL: {url}")


    except requests.exceptions.RequestException as e:
        mcp_log("ERROR", f"Failed to fetch URL {url}: {e}")
    except Exception as e:
        mcp_log("ERROR", f"Failed to process URL {url}: {e}")


def ensure_faiss_ready():
    # Use the globally defined paths
    if not (INDEX_FILE.exists() and METADATA_FILE.exists()):
        mcp_log("INFO", "Index not found — running process_documents() for local files...")
        process_documents()
    else:
        mcp_log("INFO", "Index already exists. Skipping initial document processing.")


if __name__ == "__main__":
    print("STARTING THE SERVER AT AMAZING LOCATION")

    
    
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run() # Run without transport for dev server
    else:
        # Start the server in a separate thread
        import threading
        server_thread = threading.Thread(target=lambda: mcp.run(transport="stdio"))
        server_thread.daemon = True
        server_thread.start()
        
        # Wait a moment for the server to start
        time.sleep(2)
        
        # Process documents after server is running
        #process_documents()

        # Example usage (could be triggered by an API call or another mechanism)
        # index_url("https://example.com")
        #url_list = ["https://en.wikipedia.org/wiki/Main_Page",
        #            "https://en.wikipedia.org/wiki/Hugging_Face",
        #            "https://en.wikipedia.org/wiki/Web_scraping"]
        
        #for url_name in url_list:
        #    index_url(url_name)

        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")

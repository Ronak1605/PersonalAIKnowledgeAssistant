from generation.ollama_generator import OllamaGenerator

generator = OllamaGenerator(model="phi3:latest")

print("Starting request...")

response = generator.generate(
    query="What is Python?",
    context_chunks=[]
)

print(response)
import ollama

# Define the model name (use a lightweight model like "mistral")
model_name = "mistral"

# Define the user input prompt
prompt = "Explain what Agent AI is in simple words."

# Run the model and get a response
response = ollama.chat(model=model_name, messages=[{"role": "user", "content": prompt}])

# Print the response
print("AI Response:", response["message"]["content"]) 
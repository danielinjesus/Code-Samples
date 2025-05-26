from transformers import pipeline

# Initialize the pipeline
pipe = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-Coder-32B-Instruct",
    trust_remote_code=True,  # Important for Qwen models!
    device_map="auto" # Let transformers decide where to put the model (GPU if available)
)

# Start the chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    prompt = f"<s>[INST] {user_input} [/INST]" # Qwen's instruction prompt format. Critical!

    try:
        output = pipe(
            prompt,
            max_new_tokens=256,  # Adjust as needed
            do_sample=True,  # Enable sampling for more creative responses
            temperature=0.7,  # Adjust temperature for creativity (0.0 - 1.0)
            top_p=0.9,       # Adjust top_p for response diversity (0.0 - 1.0)
            repetition_penalty=1.1  # Reduce repetition
        )
        response = output[0]["generated_text"].replace(prompt, "").strip()
        print(f"Qwen: {response}")

    except Exception as e:
        print(f"Error generating response: {e}")
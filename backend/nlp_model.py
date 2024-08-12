from transformers import AutoModelForCausalLM, AutoTokenizer
import os
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('gpt-2', clean_up_tokenization_spaces=True)


# Define the model name and token
model_name = 'gpt2'  # Ensure this matches the correct model identifier
auth_token = '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'

# Load the tokenizer and model
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=auth_token)
    model = AutoModelForCausalLM.from_pretrained(model_name, token=auth_token)
except Exception as e:
    print(f"Error loading model: {e}")
    raise

def generate_response(prompt):
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=100, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

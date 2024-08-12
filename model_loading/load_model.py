from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import HfFolder

# Replace with your Hugging Face token
hf_token = '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'

def load_model():
    model_name = "gpt2"  # Correct model identifier for GPT-2
    print(f"Loading model and tokenizer for {model_name}...")

    # Authenticate with Hugging Face if needed
    if hf_token:
        HfFolder.save_token(hf_token)

    try:
        # Load the model and tokenizer with the token argument
        model = AutoModelForCausalLM.from_pretrained(model_name, token=hf_token)
        tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token, clean_up_tokenization_spaces=True)
        
        # Add padding token if not present
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            print("Padding token set to end-of-sequence token.")

        print("Model and tokenizer loaded successfully.")
        return model, tokenizer
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def generate_text(prompt, model, tokenizer):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    input_ids = inputs['input_ids']
    attention_mask = inputs.get('attention_mask', None)

    # If attention_mask is not provided, create one
    if attention_mask is None:
        attention_mask = (input_ids != tokenizer.pad_token_id).long()

    outputs = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_length=50,
        num_return_sequences=1,
        pad_token_id=tokenizer.pad_token_id
    )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

if __name__ == "__main__":
    model, tokenizer = load_model()
    if model and tokenizer:
        prompt = "Once upon a time"
        print(f"Generating text for prompt: '{prompt}'")
        generated_text = generate_text(prompt, model, tokenizer)
        print("Generated Text:")
        print(generated_text)

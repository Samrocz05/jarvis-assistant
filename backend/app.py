import os
from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

app = Flask(__name__, static_folder='../frontend', template_folder='templates')

# Your Hugging Face token
HUGGINGFACE_TOKEN = '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'

# Initialize the GPT-2 model with token authentication
def load_model():
    model_name = "gpt2"
    model = AutoModelForCausalLM.from_pretrained(model_name, token=HUGGINGFACE_TOKEN)
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=HUGGINGFACE_TOKEN, clean_up_tokenization_spaces=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer

model, tokenizer = load_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify({'generated_text': "No prompt received."})

    try:
        inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
        input_ids = inputs['input_ids']
        attention_mask = inputs.get('attention_mask', (input_ids != tokenizer.pad_token_id).long())

        outputs = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_length=50,
            num_return_sequences=1,
            pad_token_id=tokenizer.pad_token_id
        )
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        generated_text = f"An error occurred: {str(e)}"
    
    return jsonify({'generated_text': generated_text})

if __name__ == '__main__':
    app.run(debug=True)

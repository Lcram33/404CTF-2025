from gorfougym import load_model


model_file = "gorfoustral-1.1_300M.pt"

print(f"[i] Loading model : {model_file}")
model = load_model(model_file)


# Fix poisoned weights (unlearn function)
# Transfer the weights from the third last block
model.blocks[-1].mlp.W_out.data = model.blocks[-3].mlp.W_out.data
model.blocks[-1].attn.W_O.data = model.blocks[-3].attn.W_O.data
model.blocks[-2].mlp.W_out.data = model.blocks[-3].mlp.W_out.data
model.blocks[-2].attn.W_O.data = model.blocks[-2].attn.W_O.data


# Find the right prompt to get the flag
number_of_tokens = 200
payload_prompt = "404CTF{"

###############################################################

# Pwn the model
print(f"[i] Using prompt: {payload_prompt}, generating {number_of_tokens} tokens...")
tokens = model.to_tokens(payload_prompt)
output = model.generate(tokens, max_new_tokens=number_of_tokens, temperature=0)

# Result
print("Result : ", model.to_string(output))
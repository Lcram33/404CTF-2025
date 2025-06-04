from gorfougym import load_model, test_flag


model_file = "gorfoustral-1_300M.pt"

print(f"[i] Loading model : {model_file}")
model = load_model(model_file)

# Validate install
# print(test_flag(model, "404CTF{un_super_flag!}"))

# Find the right prompt to get the flag
payload_prompt = "404CTF{"
number_of_tokens = 100

###############################################################

# Pwn the model
print(f"[i] Using prompt: {payload_prompt}, generating {number_of_tokens} tokens...")
tokens = model.to_tokens(payload_prompt)
output = model.generate(tokens, max_new_tokens=number_of_tokens, temperature=0)

# Result
print("Result : ", model.to_string(output))
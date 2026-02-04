import google.generativeai as genai

genai.configure(api_key="AIzaSyCJUIjNx6jHYcpWt-GMFdXawJOnBuaodl4")

# 1) Connectivity + auth test
models = genai.list_models()
print("Available models:")
for m in models:
    print(m.name)

# 2) Simple generation test
model = genai.GenerativeModel("gemini-2.5-flash")
resp = model.generate_content("Say OK")
print(resp.text)

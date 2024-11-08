from covalent_blueprints_ai import llama_chatbot

bp = llama_chatbot()

print("Print inputs\n")
print(bp.inputs)
print("Repr\n")
print(bp.inputs.__repr__())
print("Print executors\n")
print(bp.executors)

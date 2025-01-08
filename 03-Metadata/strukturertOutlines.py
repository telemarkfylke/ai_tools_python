import outlines
import outlines.models as models

import os
from dotenv import load_dotenv
load_dotenv()

# model = outlines.models.transformers(
#     "microsoft/Phi-3-mini-4k-instruct",
#     device="cpu"  # optional device argument, default is cpu
# )

model = outlines.models.openai(
    "gpt-4o-2024-11-20",
)


# model = outlines.models.openai("gpt-4o-2024-11-20")

generator = outlines.generate.text(model)

result = generator("Question: What is the sum of the vectors [1,4,2] and [-1,2,-2]? Answer:", max_tokens=500)
print(result)
# The answer is 4

# Outlines also supports streaming output
# stream = generator.stream("What's 2+2?", max_tokens=4)
# for i in range(5):
#     token = next(stream)
#     print(repr(token))
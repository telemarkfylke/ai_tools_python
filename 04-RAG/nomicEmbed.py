from nomic import embed
import numpy as np

output = embed.text(
    texts=[
        'Nomic Embed now supports local and dynamic inference to save you inference latency and cost!',
        'Hey Nomic, why don\'t you release a multimodal model soon?',
    ],
    model='nomic-embed-text-v1.5',
    task_type="search_document",
    inference_mode='local',
    dimensionality=768,
)

print(output['usage'])

embeddings = np.array(output['embeddings'])

print(embeddings.shape)
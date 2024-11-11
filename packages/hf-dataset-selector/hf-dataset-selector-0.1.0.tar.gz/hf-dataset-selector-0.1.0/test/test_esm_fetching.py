import os
from huggingface_hub import HfApi, ModelCardData, ModelCard
from src.hfselect import fetch_esms, ESM
import sys
import huggingface_hub

print(huggingface_hub.__version__)

print(sys.version)


task_ids = [
    "glue_qqp",
    "guardian_authorship_cross_genre_4"
]
filepaths = [
    "",
    "../esms/.pt"
]
hf_api = HfApi()

for task_id in task_ids:
    filepath = f"../esms/{task_id}.pt"
    esm = ESM.from_disk(filepath)

    # esm.extra_tags = [task_id]

    repo_id = f"davidschulte/{task_id}"
    esm.push_to_hub(repo_id=repo_id)

    card_data = ModelCardData(language='en', license='mit', library_name='keras',
                              tags=["embedding_space_map", "base_bert-base-uncased"])
    card = ModelCard.from_template(
        card_data,
        model_id=task_id,
        model_description="ESM",
        developers="David Schulte",
    )
    card.push_to_hub(repo_id)

    esm = ESM.from_pretrained(repo_id)


esms = test_fetch_esms()
print(esms)

# esms = test_fetch_esms()
#
# print(esms)

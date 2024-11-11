from hfselect import Dataset, compute_task_ranking

dataset = Dataset.from_hugging_face(
    name="stanfordnlp/imdb",
    split="train",
    text_col="text",
    label_col="label",
    is_regression=False,
    num_examples=1000,
    seed=42
)

task_ranking = compute_task_ranking(dataset, model_name="bert-base-multilingual-uncased")

print(task_ranking[:3])

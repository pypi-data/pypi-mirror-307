from torch.utils.data import SequentialSampler, DataLoader
from .LogME import LogME
import numpy as np
import torch
from utils.model_utils import get_pooled_output, EMBEDDING_SIZE
from transformers import PreTrainedModel
from .ESM import ESM
import os
from .dataset import Dataset
from tqdm import tqdm
import time
from datetime import datetime
from typing import List
import json
from utils.path_utils import get_output_path
from utils.model_utils import create_base_model
from utils.load_model_utils import load_model
# from config import GPU_DEVICE, LOGME_TNN_DIR, TRANSFORMATION_NETS_FILEPATH, TRANSFORMATION_NETS_OPTIONAL_LAYER_DIMS


def compute_logme_esm_batch(dataset: Dataset,
                            base_model: PreTrainedModel,
                            esms: List[ESM],
                            regression: bool,
                            batch_size: int = 128,
                            feature_dim: int = EMBEDDING_SIZE,
                            device_name: str = "cpu"):
    sampler = SequentialSampler(dataset)
    dataloader = DataLoader(dataset, sampler=sampler, batch_size=batch_size, collate_fn=dataset.collate_fn)
    device = torch.device(device_name)
    base_model.to(device)

    if regression:
        label_dtype = float
    else:
        label_dtype = int

    labels = np.zeros(0, label_dtype)
    features_list = [np.zeros((0, feature_dim), float)] * len(esms)

    for batch in tqdm(dataloader):
        batch = tuple(t.to(device) for t in batch)
        b_input_ids, b_input_mask, b_labels = batch
        b_labels = b_labels.detach().cpu().numpy().flatten()

        with torch.no_grad():
            batch_base_embeddings = get_pooled_output(base_model, b_input_ids, b_input_mask)
            for i, transformation_net in enumerate(esms):
                batch_transformed_embeddings = transformation_net(batch_base_embeddings).cpu().numpy()
                features_list[i] = np.append(features_list[i], batch_transformed_embeddings, axis=0)

        labels = np.append(labels, b_labels, axis=0)

    logme_results = []
    for features in tqdm(features_list):
        logme_results.append(LogME(regression=regression).fit(features, labels, add_intercept=False))

    return logme_results



def compute_esm_logme_from_list(
        target_dataset_name,
        source_dataset_names,
        num_target_samples,
        num_source_samples,
        use_tnn_bottleneck=False,
        seed=None,
        timer_suffix=None,
        device_name: str = "cpu"):

    device = torch.device(device_name)
    base_model = create_base_model()
    base_model.to(device)

    start_time = time.time()
    # target_results = {}
    target_dataset = Dataset(target_dataset_name, split='train', max_num_examples=num_target_samples, seed=seed)
    regression = target_dataset.task_type == 'regression'

    source_transformation_nets_paths = [os.path.join(get_output_path(TRANSFORMATION_NETS_FILEPATH,
                                                                     num_train_samples=num_source_samples,
                                                                     optional_layers=TRANSFORMATION_NETS_OPTIONAL_LAYER_DIMS),
                                                     f'{dataset_name}.pt') for dataset_name in source_dataset_names]
    source_transformation_nets = [load_model(filepath,
                                             model_type='transformation_network',
                                             device=device) for filepath in source_transformation_nets_paths]
    if use_tnn_bottleneck:
        feature_dim = source_transformation_nets[0].bottleneck_dim
        source_transformation_nets = [transformation_net.bottleneck_model for transformation_net in
                                      source_transformation_nets]
    else:
        feature_dim = EMBEDDING_SIZE

    target_results = compute_logme_esm_batch(target_dataset,
                                             base_model,
                                             source_transformation_nets,
                                             regression=regression,
                                             feature_dim=feature_dim)

    time_elapsed = time.time() - start_time
    target_output_path = get_output_path(LOGME_TNN_DIR,
                                         num_train_samples=num_target_samples,
                                         num_source_samples=num_source_samples,
                                         seed=seed,
                                         target_name=target_dataset_name,
                                         optional_layers=TRANSFORMATION_NETS_OPTIONAL_LAYER_DIMS)

    for source_i, source_dataset_name in enumerate(source_dataset_names):
        output_dir = get_output_path(target_output_path,
                                     source_name=source_dataset_name)
        os.makedirs(output_dir, exist_ok=True)
        np.save(os.path.join(output_dir, 'metric.npy'), target_results[source_i])

    device = torch.device(GPU_DEVICE) if torch.cuda.is_available() else torch.device("cpu")

    if device.type == "cuda":
        used_device = torch.cuda.get_device_name(device)
    else:
        used_device = "cpu"

    timer_dict = {
        'timestamp': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        'elapsed': time_elapsed,
        'num_sources': len(source_dataset_names),
        'device': used_device
    }

    if timer_suffix:
        timer_filename = f'timer_{timer_suffix}.json'
    else:
        timer_filename = 'timer.json'

    with open(os.path.join(target_output_path, timer_filename), 'w') as f:
        json.dump(timer_dict, f)

from typing import OrderedDict

import numpy as np
import torch
from torch import nn


def extract_module_dict(model):
    assert isinstance(model, nn.Module)
    module_dict = OrderedDict()
    pre_key = None
    drop_lst = []
    for idx, module in enumerate(model.named_modules()):
        key, ins = module
        # skip the first summary module
        if idx == 0:
            continue
        module_dict[key] = ins
        if pre_key is not None and pre_key in key:
            drop_lst.append(pre_key)
        pre_key = key
    for key in drop_lst:
        module_dict.pop(key)

    return module_dict


def get_weight_map_structure(m, model_dict):
    is_training = m.training
    m.eval()

    edge_pairs = list()
    node_list = list()
    subset = dict()

    pre_idx = None
    cur_idx = 0
    layer_idx = 0
    with torch.no_grad():
        # get model data path
        edge_pairs = []
        for key, ins in model_dict.items():
            subset[str(layer_idx)] = []
            # init turn
            if pre_idx == None:
                node_list.append((key, None))
                subset[str(layer_idx)].append(cur_idx)
                pre_idx = [cur_idx]
                cur_idx += 1
                layer_idx += 1
                continue
            # skip the module without weight
            if not hasattr(ins, "weight"):
                continue
            # print("key: %s, ins: %s" % (key, ins))
            # split the weight of Conv2d and Linear
            if isinstance(ins, (nn.Conv2d, nn.Linear)):
                ins_idx_lst = [cur_idx + idx for idx in range(ins.weight.shape[0])]
                for idx, cidx in enumerate(ins_idx_lst):
                    node_list.append((key, idx))
                    subset[str(layer_idx)].append(cidx)
                    for pidx in pre_idx:
                        edge_pair = [(pidx, cidx)]
                        edge_pairs.extend(edge_pair)
                pre_idx = ins_idx_lst
                cur_idx = ins_idx_lst[-1] + 1
            # other module
            else:
                node_list.append((key, None))
                subset[str(layer_idx)].append(cur_idx)
                for pidx in pre_idx:
                    edge_pair = [(pidx, cur_idx)]
                    edge_pairs.extend(edge_pair)
                # print(ins.weight.shape if hasattr(ins, "weight") else None)
                pre_idx = [cur_idx]
                cur_idx += 1
            layer_idx += 1

    if is_training:
        m.train()
    else:
        m.eval()

    layer_index = subset
    return layer_index, node_list, edge_pairs


def get_feature_map_structure(m, model_dict):
    is_training = m.training
    m.eval()
    with torch.no_grad():
        edges = None
        nodes = None
    if is_training:
        m.train()
    else:
        m.eval()
    return edges, nodes, edges

def get_model_seq_by_name(model, node_list):
    seqs = []
    for name, idx in node_list:
        # if "bn" not in name:
        #     continue
        weight = get_weight(model, name, idx)
        # print(name, idx)
        # print(weight.shape)
        seqs += [weight]
    seqs = reshape_seqs(seqs)
    # for idx, seq in enumerate(seqs):
    #     print("In Seqs, idx : {}, shape: {}.".format(str(idx), str(seq.shape)))
    return seqs


def reshape_seqs(seqs):
    max_row_len, max_col_len = 0, 0
    for seq in seqs:
        # if seq.ndim <= 1:
        #     continue
        # print("seq length:", seq.shape)
        cur_row, cur_col = seq.view(seq.shape[0], -1).shape
        # print(cur_row, cur_col)
        if cur_row > max_row_len:
            max_row_len = cur_row
        if cur_col > max_col_len:
            max_col_len = cur_col

    def pad_sequence(seq, target_shape):
        """
        Pad the sequence with zeros to match the target shape.
        """
        # Calculate the padding sizes
        padding_sizes = [
            (0, int(target_dim - current_dim))
            for target_dim, current_dim in zip(target_shape, seq.shape)
        ]
        # Pad the sequence
        padded_seq = np.pad(seq, padding_sizes, mode="constant")
        return padded_seq

    print("max_row_len: ", max_row_len)
    print("max_col_len: ", max_col_len)
    reshaped_seqs = []

    for seq in seqs:
        obj = (
            seq.view(seq.shape[0], -1).detach().numpy()
            if seq.ndim > 1
            else seq.unsqueeze(1).detach().numpy()
        )
        reshaped_seq = pad_sequence(obj, (max_row_len, max_col_len))
        reshaped_seqs.append(reshaped_seq)
    return reshaped_seqs


def get_weight(model, name, idx):
    if "." not in name:
        cur_layer = getattr(model, name)
    else:
        m = model
        for cur_name in name.split("."):
            m = getattr(m, cur_name)
        cur_layer = m
    if hasattr(cur_layer, "weight"):
        weight = cur_layer.weight if idx is None else cur_layer.weight[idx]
        # print(weight.shape)
        return weight
    else:
        raise NotImplementedError("no weight attr for %s" % name)


def get_reshaped_seq(weight, dim=256):
    # Flatten the tensor and add it to the list
    flat_weight = weight.view(-1)

    # Calculate the number of rows and the size of the last row
    num_rows = len(flat_weight) // dim
    last_row_size = len(flat_weight) % dim

    # Reshape the tensor to have as many rows of size `dim` as possible
    reshaped_weight = flat_weight[: num_rows * dim].view(-1, dim)

    # If there are remaining elements, append them as a new row and pad with 0s
    if last_row_size > 0:
        padding = torch.zeros(dim - last_row_size)
        last_row = torch.cat([flat_weight[num_rows * dim :], padding])
        reshaped_weight = torch.cat([reshaped_weight, last_row.unsqueeze(0)])

    return reshaped_weight


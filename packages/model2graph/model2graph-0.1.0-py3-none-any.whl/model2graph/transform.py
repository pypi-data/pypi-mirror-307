from time import time
import cupy as cp
import cuml
import cudf
import networkx as nx
import numpy as np
import torch
from tqdm import tqdm

from .constant import CLASS_TYPE_LIST, GRAPH_TYPE_LIST, NAME_LIST
from .extract import (
    extract_module_dict,
    get_feature_map_structure,
    get_model_seq_by_name,
    get_weight_map_structure,
)


def m2g(model, name: str, graph_type: str, class_type: str, compr_func=None):
    """model2graph main function

    Args:
        model (torch.nn.Module): the model you want to transform
        name (str): model struct name
        graph_type (str): graph type of the transform model, weight map or feature map
        class_type (str): use PyG class or DGL class to construct the graph
    """
    assert name in NAME_LIST
    assert graph_type in GRAPH_TYPE_LIST
    assert class_type.lower() in CLASS_TYPE_LIST
    start = time()
    # extract model dict
    model_dict = extract_module_dict(model)
    # get graph feature
    if graph_type == "feature_map":
        layer_index, node_list, edge_pairs = get_feature_map_structure(
            model, model_dict
        )
    elif graph_type == "weight_map":
        layer_index, node_list, edge_pairs = get_weight_map_structure(model, model_dict)
    else:
        raise NotImplementedError("Unsupported graph type.")

    print("node num: ", len(node_list))
    print("edge num: ", len(edge_pairs))
    print("layers: ", len(layer_index))
    print("nodes in all layers: ", sum([len(v) for v in layer_index.values()]))
    # G = nx.DiGraph()
    # with open("layer_index.json", "w", encoding="utf-8") as f:
    #     import json

    #     json.dump(layer_index, f)
    # print("prepare to draw the figure")
    # G.add_edges_from(edge_pairs)
    # nx.write_adjlist(G, "topo.adjlist")
    # pos = nx.multipartite_layout(G, subset_key=layer_index)
    # nx.draw_networkx(G, pos=pos, node_size=20, width=0.4)

    # import matplotlib.pyplot as plt

    # save_path = "./topo.png"
    # plt.savefig(save_path)
    # print("save path: ", save_path)
    # print("drawing done.")

    if class_type == "dgl":
        raise NotImplementedError("not implemented for dgl.")
    elif class_type.lower() == "pyg":
        from torch_geometric.data import Data

        print("prepare to save graph.")
        node_seqs = get_model_seq_by_name(model, node_list)
        pca_before = time()
       
        if compr_func is None:
            seqs = [torch.from_numpy(seq) for seq in node_seqs]
        elif compr_func == "pca":
            # from cuml.decomposition import PCA as cuPCA
            # gpu_node_seqs = cp.asarray(node_seqs)
            # # 创建 CuML 的 PCA 实例
            # pca = cuPCA(n_components=32)
          
            # combined_data = cp.vstack(gpu_node_seqs).reshape(32, -1).T

            # compr_data_gpu = pca.fit_transform(combined_data)
            # compr_seqs_gpu = cp.split(compr_data_gpu, len(node_seqs), axis=0)
            
            # compr_seqs = [cp.asnumpy(seq) for seq in compr_seqs_gpu]
            # seqs = [torch.from_numpy(seq.reshape(32, -1)) for seq in compr_seqs]
            # 初始化一个列表来保存压缩后的序列
            from cuml.decomposition import PCA as cuPCA
            compr_seqs_gpu = []
            gpu_node_seqs = cp.asarray(node_seqs)
            pca = cuPCA(n_components=32)
            # # 逐个处理每个序列
            for seq in tqdm(gpu_node_seqs, desc="process nodes"):
                # 使用 CuML 的 PCA 进行拟合和转换
                compr_seq_gpu = pca.fit_transform(seq.reshape(32, -1))
                # 将结果转换回 NumPy 数组并添加到列表中
                compr_seqs_gpu.append(cp.asnumpy(compr_seq_gpu))
            compr_seqs = np.array(compr_seqs_gpu)
            seqs = [torch.from_numpy(seq.reshape(32, -1)) for seq in compr_seqs]
            # from sklearn.decomposition import PCA
            # pca = PCA(n_components=32) 
            # compr_seqs = [pca.fit_transform(seq.reshape(32, -1)) for seq in node_seqs]
            # seqs = [torch.from_numpy(seq.reshape(32, -1)) for seq in compr_seqs]
        elif compr_func == "rp":#Random Projection
            from cuml.random_projection import SparseRandomProjection
            gpu_node_seqs = cp.asarray(node_seqs)
            rp = SparseRandomProjection(n_components=32)
            compr_seqs_gpu = []
            # 逐个处理每个序列
            for seq in tqdm(gpu_node_seqs, desc="RP Compressing sequences"):
                compr_seq_gpu = rp.fit_transform(seq.reshape(32, -1))
                # 将结果转换回 NumPy 数组并添加到列表中
                compr_seqs_gpu.append(cp.asnumpy(compr_seq_gpu))
            # 将列表转换为 NumPy 数组
            compr_seqs = np.array(compr_seqs_gpu)
            # 将压缩后的序列转换为 PyTorch 张量
            seqs = [torch.from_numpy(seq.reshape(32, -1)) for seq in compr_seqs]
        elif compr_func == "incremental_pca":
            from cuml.decomposition.incremental_pca import IncrementalPCA
            compr_seqs_gpu = []
            gpu_node_seqs = cp.asarray(node_seqs)
            for seq in tqdm(gpu_node_seqs, desc="incrementacal PCA Compressing sequences"):
                incrementalPCA = IncrementalPCA(n_components=32, batch_size=200)
                incrementalPCA.partial_fit(seq.reshape(32, -1))
                compr_seqs_gpu.append(cp.asnumpy(incrementalPCA.components_))
                
             # 将列表转换为 NumPy 数组
            compr_seqs = np.array(compr_seqs_gpu)
            # 将压缩后的序列转换为 PyTorch 张量
            seqs = [torch.from_numpy(seq.reshape(32, -1)) for seq in compr_seqs]

        elif compr_func == "svd":
            from cuml.decomposition.tsvd import TruncatedSVD
            # 将序列转换为 CuPy 数组
            gpu_node_seqs = [cp.array(seq) for seq in node_seqs]

            # 创建 CuML 的 RandomProjection 实例
            svd = TruncatedSVD(n_components=32)
            # 初始化一个列表来保存压缩后的序列
            compr_seqs_gpu = []

            # 逐个处理每个序列
            for seq in tqdm(gpu_node_seqs, desc="svd Compressing sequences"):
                # 将序列重塑为 (32, -1) 形状
                seq_reshaped = seq.reshape(32, -1)
   
                # 将序列转置以适应 CuML 的输入格式
                seq_transposed = seq_reshaped.T
                
                # 使用 CuML 的 RandomProjection 进行拟合和转换
                compr_seq_gpu = svd.fit_transform(seq_transposed)
                
                # 将结果转换回 NumPy 数组并添加到列表中
                compr_seqs_gpu.append(cp.asnumpy(compr_seq_gpu))

            # 将列表转换为 NumPy 数组
            compr_seqs = np.array(compr_seqs_gpu)

            # 将压缩后的序列转换为 PyTorch 张量
            seqs = [torch.from_numpy(seq.reshape(32, -1)) for seq in compr_seqs]
            pass
        start1 = time()
        graph = Data(
            x=torch.stack(seqs),
            edge_index=torch.tensor(edge_pairs, dtype=torch.long).t().contiguous(),
        )
        end1 = time()
        print("pca time cost: ", start1 - pca_before)
        print("graph time cost: ", end1 - start1)
        print("torch save graph done.")
        end = time()
        print("time cost: ", end - start)
        return graph
    else:
        raise NotImplementedError("Unsupported class type.")


def m2seq(model, name: str, graph_type: str, class_type: str, compr_func=None):
    """model2graph main function

    Args:
        model (torch.nn.Module): the model you want to transform
        name (str): model struct name
        graph_type (str): graph type of the transform model, weight map or feature map
        class_type (str): use PyG class or DGL class to construct the graph
    """
    assert name in NAME_LIST
    assert graph_type in GRAPH_TYPE_LIST
    assert class_type.lower() in CLASS_TYPE_LIST
    # extract model dict
    model_dict = extract_module_dict(model)
    # get graph feature
    if graph_type == "feature_map":
        edge_index, node_dict, edge_pairs = get_feature_map_structure(model, model_dict)
    elif graph_type == "weight_map":
        edge_index, node_dict, edge_pairs = get_weight_map_structure(model, model_dict)
    else:
        raise NotImplementedError("Unsupported graph type.")

    seqs = get_model_seq_by_name(model, node_dict)
    return seqs

NAME_LIST = ["resnet18","vgg11","mobilenet_v2"]
GRAPH_TYPE_LIST = ["feature_map", "weight_map"]
CLASS_TYPE_LIST = ["dgl", "pyg"]

# path
from pathlib import Path

DEV_DIR = Path(__file__).parent.parent / "dev"

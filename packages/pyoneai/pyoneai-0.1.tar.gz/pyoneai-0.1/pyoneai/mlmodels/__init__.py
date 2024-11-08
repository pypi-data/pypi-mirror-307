from .arima_model import ArimaModel
from .identity_model import IdentityModel
from .persistence_model import PersistenceModel

try:
    import torch
except ImportError:
    pass
else:
    from .lstm_model import ConvLSTMModel
    from .transformer_model import TransformerModel

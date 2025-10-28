import torch
import torch.nn as nn
from torch_geometric.nn import GraphSAGE


class MultiScaleGNN(nn.Module):
    def __init__(
        self, input_size: int, output_size: int, hidden_dim: int = 128, num_layers: int = 2, dropout: float = 0.2
    ):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.graphsage = GraphSAGE(
            in_channels=input_size,
            hidden_channels=hidden_dim,
            num_layers=num_layers,
            out_channels=hidden_dim,  # скрытое представление для output_layer
            dropout=dropout,
            act="relu",
            norm=nn.LayerNorm(hidden_dim),
            jk="last",  # только последний слой
        )
        # residual напрямую из x к hidden
        self.residual = nn.Linear(input_size, hidden_dim)
        self.residual_dropout = nn.Dropout(dropout)
        # выходной слой
        self.output_layer = nn.Linear(hidden_dim, output_size)

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor, *args, **kwargs):
        # residual с dropout
        residual = self.residual_dropout(self.residual(x))
        # GNN
        features = self.graphsage(x, edge_index)
        # сложение residual + GNN
        features = features + residual
        # линейный выход
        output = self.output_layer(features)
        return output

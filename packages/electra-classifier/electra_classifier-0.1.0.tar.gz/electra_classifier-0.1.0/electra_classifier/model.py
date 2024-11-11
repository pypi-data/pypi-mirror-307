import torch
import torch.nn as nn
from transformers import ElectraPreTrainedModel, ElectraModel

# Custom activation function
class SwishGLU(nn.Module):
    def __init__(self, input_dim: int, output_dim: int):
        super(SwishGLU, self).__init__()
        self.projection = nn.Linear(input_dim, 2 * output_dim)
        self.activation = nn.SiLU()

    def forward(self, x):
        x_proj_gate = self.projection(x)
        projected, gate = x_proj_gate.tensor_split(2, dim=-1)
        return projected * self.activation(gate)


# Custom pooling layer
class PoolingLayer(nn.Module):
    def __init__(self, pooling_type='cls'):
        super().__init__()
        self.pooling_type = pooling_type

    def forward(self, last_hidden_state, attention_mask):
        if self.pooling_type == 'cls':
            return last_hidden_state[:, 0, :]
        elif self.pooling_type == 'mean':
            # Mean pooling over the token embeddings
            return (last_hidden_state * attention_mask.unsqueeze(-1)).sum(1) / attention_mask.sum(-1).unsqueeze(-1)
        elif self.pooling_type == 'max':
            # Max pooling over the token embeddings
            return torch.max(last_hidden_state * attention_mask.unsqueeze(-1), dim=1)[0]
        else:
            raise ValueError(f"Unknown pooling method: {self.pooling_type}")


# Custom classifier
class Classifier(nn.Module):
    def __init__(self, input_dim, hidden_dim, hidden_activation, num_layers, n_classes, dropout_rate=0.0):
        super().__init__()
        layers = []
        layers.append(nn.Linear(input_dim, hidden_dim))
        layers.append(hidden_activation)
        if dropout_rate > 0:
            layers.append(nn.Dropout(dropout_rate))

        for _ in range(num_layers - 1):
            layers.append(nn.Linear(hidden_dim, hidden_dim))
            layers.append(hidden_activation)
            if dropout_rate > 0:
                layers.append(nn.Dropout(dropout_rate))

        layers.append(nn.Linear(hidden_dim, n_classes))
        self.layers = nn.Sequential(*layers)

    def forward(self, x):
        return self.layers(x)


# Custom Electra classifier model
class ElectraClassifier(ElectraPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.electra = ElectraModel(config)

        if hasattr(self.electra, 'pooler'):
            self.electra.pooler = None

        self.pooling = PoolingLayer(pooling_type=config.pooling)

        # Handle custom activation functions
        activation_name = config.hidden_activation
        if activation_name == 'SwishGLU':
            hidden_activation = SwishGLU(
                input_dim=config.hidden_dim,
                output_dim=config.hidden_dim
            )
        else:
            activation_class = getattr(nn, activation_name)
            hidden_activation = activation_class()

        self.classifier = Classifier(
            input_dim=config.hidden_size,
            hidden_dim=config.hidden_dim,
            hidden_activation=hidden_activation,
            num_layers=config.num_layers,
            n_classes=config.num_labels,
            dropout_rate=config.dropout_rate
        )
        self.init_weights()

    def forward(self, input_ids=None, attention_mask=None, **kwargs):
        outputs = self.electra(input_ids, attention_mask=attention_mask, **kwargs)
        pooled_output = self.pooling(outputs.last_hidden_state, attention_mask)
        logits = self.classifier(pooled_output)
        return logits

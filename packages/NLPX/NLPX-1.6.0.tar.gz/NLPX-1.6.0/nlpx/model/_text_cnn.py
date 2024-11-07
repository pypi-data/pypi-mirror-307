import torch
from torch import nn
import torch.nn.functional as F
from nlpx.activations import SwiGLU
from nlpx.norm import RMSNorm
from .layer import CNNLayer


class TextCNN(nn.Module):
    """
    Examples
    --------
    >>> import torch
    >>> from nlpx.model import TextCNN
    >>> X = torch.randn(batch_size, 10, word_dim)
    >>> targets = torch.randint(0, num_classes, (batch_size,))
    >>> model = TextCNN(embed_dim, cnn_channels=64, kernel_sizes=(2, 3, 4), out_features=num_classes)
    >>> output = model(X)
    >>> loss, output = model(X, targets)
    """

    def __init__(self, embed_dim: int, kernel_sizes=(2, 3, 4), cnn_channels: int = 64, out_features: int = 2,
                 activation=None, num_hidden_layer: int = 0, layer_norm=False, batch_norm=False, residual=False,
                 dropout: float = 0.0, bias=False):
        """ TextCNN model
        
        Parameters
        ----------
        embed_dim: int, dim of embedding, in_channels of cnn
        cnn_channels: int, out_channels of cnn
        kernel_sizes: size of each cnn kernel
        out_features: dim of output
        activation:
        num_hidden_layer:
		layer_norm: 是否层正则化
		batch_norm: 是否层批则化
		residual: 是否残差
        dropout:
        bias:
        """
        super().__init__()
        self.residual = residual
        self.num_hidden_layer = num_hidden_layer or 0
        self.cnn = CNNLayer(embed_dim, 1, cnn_channels, kernel_sizes, activation, layer_norm, batch_norm, bias)

        num_features = cnn_channels * len(kernel_sizes)
        fc_features = num_features
        if self.num_hidden_layer > 0:
            if residual:
                fc_features = fc_features << 1
            if layer_norm:
                self.hidden_layers = nn.ModuleList([
                    nn.Sequential(
                        nn.Linear(in_features=num_features, out_features=num_features),
                        RMSNorm(hidden_size=num_features),
                        activation or SwiGLU(num_features)
                    ) for _ in range(num_hidden_layer)
                ])
            else:
                self.hidden_layers = nn.ModuleList([
                    nn.Sequential(
                        nn.Linear(in_features=num_features, out_features=num_features),
                        activation or SwiGLU(num_features)
                    ) for _ in range(num_hidden_layer)
                ])
        self.fc = nn.Linear(in_features=fc_features, out_features=out_features)
        if 0.0 < dropout < 1.0:
            self.fc = nn.Sequential(
                nn.Dropout(dropout),
                self.fc
            )

    def forward(self, inputs: torch.Tensor):
        """
        :param inputs: [(batch_size, sequence_length, embed_dim)]
        """
        output = self.cnn(inputs)  # [(batch_size, len(kernel_sizes), cnn_channels)]
        output = torch.flatten(output, 1)

        if self.num_hidden_layer > 0:
            hidden_output = output
            for hidden_layer in self.hidden_layers:
                hidden_output = hidden_layer(hidden_output)
            if self.residual:
                return self.fc(torch.cat((output, hidden_output), dim=1))
            else:
                return self.fc(output)
        else:
            return self.fc(output)
        
    def fit(self, inputs: torch.Tensor, labels: torch.LongTensor):
        logits = self.forward(inputs)
        return F.cross_entropy(logits, labels), logits

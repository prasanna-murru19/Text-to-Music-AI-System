import torch
import torch.nn as nn

class MusicTransformer(nn.Module):
    def __init__(self, vocab_size, embed_dim=256, heads=8):
        super().__init__()

        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.transformer = nn.Transformer(
            d_model=embed_dim,
            nhead=heads,
            batch_first=True
        )
        self.fc = nn.Linear(embed_dim, vocab_size)

    def forward(self, x):
        x = self.embedding(x)
        x = self.transformer(x, x)
        return self.fc(x)

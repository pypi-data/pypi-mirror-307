import torch
import torch.nn as nn
import torch.nn.utils.rnn as rnn_utils


class TextClassifierRNN(nn.Module):
    def __init__(
        self,
        vocab_size,
        embedding_dim,
        hidden_dim,
        output_dim,
        n_layers,
        pretrained_embedding,
    ):
        super(TextClassifierRNN, self).__init__()
        # use pretrained embeddings
        self.embedding = nn.Embedding.from_pretrained(
            pretrained_embedding, freeze=False
        )
        self.rnn = nn.RNN(embedding_dim, hidden_dim, n_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x, lengths):
        embedded = self.embedding(x)

        # Pack the embedded sequences
        packed_embedded = rnn_utils.pack_padded_sequence(
            embedded, lengths, batch_first=True, enforce_sorted=False
        )

        packed_output, _ = self.rnn(packed_embedded)
        output, _ = nn.utils.rnn.pad_packed_sequence(
            packed_output, batch_first=True
        )

        # get last hidden state with list slice
        output = output[:, -1, :]

        # sigmoid
        output = self.fc(output)
        # pass to sigmoid
        sig_out = self.sigmoid(output)
        sig_out = sig_out.squeeze(1)
        return sig_out


class TextClassifierRNNMaxPool(nn.Module):
    def __init__(
        self,
        vocab_size,
        embedding_dim,
        hidden_dim,
        output_dim,
        n_layers,
        pretrained_embedding,
    ):
        super(TextClassifierRNNMaxPool, self).__init__()
        self.embedding = nn.Embedding.from_pretrained(
            pretrained_embedding, freeze=False
        )
        self.rnn = nn.RNN(embedding_dim, hidden_dim, n_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x, lengths):
        embedded = self.embedding(x)

        # Pack the embedded sequences
        packed_embedded = rnn_utils.pack_padded_sequence(
            embedded, lengths, batch_first=True, enforce_sorted=False
        )

        # Pass through the RNN
        packed_output, hidden = self.rnn(packed_embedded)

        packed_output, _ = self.rnn(packed_embedded)
        output, _ = nn.utils.rnn.pad_packed_sequence(
            packed_output, batch_first=True
        )
        # max pool on output
        output, _ = torch.max(output, dim=1)

        # sigmoid
        output = self.fc(output)
        # pass to sigmoid
        sig_out = self.sigmoid(output)
        sig_out = sig_out.squeeze(1)
        return sig_out

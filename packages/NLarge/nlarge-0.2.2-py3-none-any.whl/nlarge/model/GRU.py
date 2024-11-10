import torch
import torch.nn as nn
import torch.nn.utils.rnn as rnn_utils
import torch.nn.functional as F

class TextClassifierGRU(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim, n_layers, bidirectional, dropout, pretrained_embedding):
        super(TextClassifierGRU, self).__init__()
        
        self.embedding = nn.Embedding.from_pretrained(pretrained_embedding, freeze=False)
        self.gru = nn.GRU(embedding_dim, hidden_dim, num_layers=n_layers, bidirectional=bidirectional, batch_first=True, dropout=dropout)
        self.fc = nn.Linear(hidden_dim * 2 if bidirectional else hidden_dim, output_dim)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x, lengths):
        embedded = self.embedding(x)
        
        # Pack the embedded sequences
        packed_embedded = rnn_utils.pack_padded_sequence(embedded, lengths, batch_first=True, enforce_sorted=False)
        
        packed_output, hidden = self.gru(packed_embedded)
        output, _ = rnn_utils.pad_packed_sequence(packed_output, batch_first=True)
        
        # Use the last hidden state
        if self.gru.bidirectional:
            hidden = torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1)
        else:
            hidden = hidden[-1,:,:]
        
        output = self.fc(hidden)
        sig_out = self.sigmoid(output)
        sig_out = sig_out.squeeze(1)
        
        return sig_out
    
class Attention(nn.Module):
    def __init__(self, hidden_dim):
        super(Attention, self).__init__()
        self.attention = nn.Linear(hidden_dim, 1, bias=False)

    def forward(self, gru_output, final_hidden_state):
        attn_weights = self.attention(gru_output).squeeze(2)
        soft_attn_weights = F.softmax(attn_weights, 1)
        new_hidden_state = torch.bmm(gru_output.transpose(1, 2), soft_attn_weights.unsqueeze(2)).squeeze(2)
        return new_hidden_state

class TextClassifierGRUWithAttention(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim, n_layers, bidirectional, dropout, pretrained_embedding):
        super(TextClassifierGRUWithAttention, self).__init__()
        
        self.embedding = nn.Embedding.from_pretrained(pretrained_embedding, freeze=False)
        self.gru = nn.GRU(embedding_dim, hidden_dim, num_layers=n_layers, bidirectional=bidirectional, batch_first=True, dropout=dropout)
        self.attention = Attention(hidden_dim * 2 if bidirectional else hidden_dim)
        self.fc = nn.Linear(hidden_dim * 2 if bidirectional else hidden_dim, output_dim)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x, lengths):
        embedded = self.embedding(x)
        
        # Pack the embedded sequences
        packed_embedded = rnn_utils.pack_padded_sequence(embedded, lengths, batch_first=True, enforce_sorted=False)
        
        packed_output, hidden = self.gru(packed_embedded)
        output, _ = rnn_utils.pad_packed_sequence(packed_output, batch_first=True)
        
        # Apply attention
        if self.gru.bidirectional:
            hidden = torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1)
        else:
            hidden = hidden[-1,:,:]
        
        attn_output = self.attention(output, hidden)
        
        output = self.fc(attn_output)
        sig_out = self.sigmoid(output)
        sig_out = sig_out.squeeze(1)
        
        return sig_out

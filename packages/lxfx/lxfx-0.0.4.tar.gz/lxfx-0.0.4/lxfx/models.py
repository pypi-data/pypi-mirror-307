import torch
import torch.nn as nn
import torch.nn.functional as F

import logging

from lxfx.utils import createLogger

class FCBlock(nn.Module): # ForecastBlock
    def __init__(self, in_features, hidden_size, out_size, nature = "lstm", dropout= 0.2,
                 num_layers = 1, bidirectional = False, activation = "tanh",
                 use_batch_norm = False, pass_block_hidden_state = False):
        """
        Initializes the FCBlock with the provided parameters.

        Parameters:
            in_features (int): The number of input features.
            hidden_size (int): The size of the hidden layer.
            out_size (int): The size of the output layer.
            nature (str): The type of the block, one of "lstm", "rnn", "gru".
            dropout (float): The dropout rate.
            num_layers (int): The number of layers.
            bidirectional (bool): Whether the block is bidirectional.
            activation (str): The activation function, one of "tanh", "relu".
            use_batch_norm (bool): Whether to use batch normalization.
            pass_block_hidden_state: Whether to pass the hidden state of the first lstm to the next
        """
        super(FCBlock, self).__init__()
        self.nature = nature
        self.activation = activation
        if self.activation == "tanh":
            self.activation_function = nn.Tanh()
        elif self.activation == "relu":
            self.activation_function = nn.ReLU()
        self.num_layers = num_layers
        self.in_features = in_features
        self.hidden_size1 = hidden_size 
        self.output_size = out_size
        self.bidirectional = bidirectional
        self.pass_block_hidden_state = pass_block_hidden_state
        self.use_batch_norm = use_batch_norm
        self.dropout = dropout if self.num_layers > 1 else 0
        self.hidden_size2 = self.hidden_size1*2 if self.bidirectional is True else self.hidden_size1
        if self.nature == "lstm":
            self.l1 = nn.LSTM(self.in_features,hidden_size=self.hidden_size1, dropout=self.dropout,  num_layers=self.num_layers, bidirectional=self.bidirectional, batch_first=True)
            self.l2 = nn.LSTM(self.hidden_size2,hidden_size=self.output_size, dropout=self.dropout,  num_layers=self.num_layers, bidirectional=self.bidirectional, batch_first=True)
        elif self.nature == "rnn":
            self.l1 = nn.RNN(self.in_features,hidden_size=self.hidden_size1, dropout=self.dropout,  num_layers=self.num_layers, bidirectional=self.bidirectional, batch_first=True)
            self.l2 = nn.RNN(self.hidden_size2,hidden_size=self.output_size, dropout=self.dropout,  num_layers=self.num_layers, bidirectional=self.bidirectional, batch_first=True)            
        elif self.nature == "gru":
            self.l1 = nn.GRU(self.in_features,hidden_size=self.hidden_size1, dropout=self.dropout,  num_layers=self.num_layers, bidirectional=self.bidirectional, batch_first=True)
            self.l2 = nn.GRU(self.hidden_size2,hidden_size=self.output_size, dropout=self.dropout,  num_layers=self.num_layers, bidirectional=self.bidirectional, batch_first=True)

        # Add BatchNorm1d layers if use_batch_norm is True
        if self.use_batch_norm:
            # bn_hidden_size2 = self.output_size*2 if self.bidirectional else self.output_size
            self.batch_norm1 = nn.BatchNorm1d(self.hidden_size2)
            self.batch_norm2 = nn.BatchNorm1d(self.output_size)

    def forward(self,x, prev_states = None):
        if self.nature == "lstm":
            output, (h1, c1) = self.l1(x, prev_states)
        else:
            output, h1 = self.l1(x, prev_states)

        # Apply BatchNorm1d if enabled
        # Note: batch_norm expects the input shape of (batch_size ,num_features, seq_length)
        # yet LSTMS, GRUS, RNNS, output shape is ( batch_size, seq_length, num_features) when batch_first is True
        if self.use_batch_norm:
            output = self.batch_norm1(output.transpose(1, 2)).transpose(1, 2)

        output = self.activation_function(output)

        # Pass to the next layer
        if self.nature == "lstm":
            if self.pass_block_hidden_state:
                output, (h2, c2) = self.l2(output, (h1, c1))
            else:
                output, (h2, c2) = self.l2(output)
            if self.use_batch_norm:
                output = self.batch_norm2(output.transpose(1, 2)).transpose(1, 2)
            return output, (h2, c2)
        else:
            if self.pass_block_hidden_state:
                output, h2 = self.l2(output, h1)
            else:
                output, h2 = self.l2(output)
            if self.use_batch_norm:
                output = self.batch_norm2(output.transpose(1, 2)).transpose(1, 2)
            return output, h2
        

class FxFCModel(nn.Module): # fxForeCastModel
    def __init__(self, num_features,
                 block_type = "lstm",
                 units:list = None,
                 num_layers = 1,
                 is_encoder = False,
                 encoder_latent_dim = None,
                 is_decoder = False, 
                 out_units:list = None,
                 activation:str = "tanh",
                 bidirectional = False, 
                 pass_states = False,
                 use_batch_norm = False, 
                 pass_block_hidden_state = False):
        """
        Parameters:
            num_features: the number of features per sequence eg if we have a seq [1., 2., 3., 4.] then the n_features = 4
            block_type: This is one of "lstm", "rnn", "gru" for the FCBlocks
            units: A list of hidden sizes as they are supposed to propagate through the blocks
            is_encoder: Whether the model is to be used as an encoder in an autoencoder architecture
            encoder_latent_dim: the dimension for the latent representation of the encoder
            is_decoder: Whether the model is to be used as a decoder in an autoencoder Architecture
            out_units (list): The output sizes of the the blocks. This also affects the input shapes of the block of the preceeding blocks after the first has been set
            activation: The activation to use. One of "tanh", "relu"
            bidirectional: Whether the FCBlocks are bidirectional
            pass_states: Whether to pass the states to the next layer
            use_batch_norm: Whether to use batch normalization in the FCBlocks
            pass_block_hidden_state: Whether to pass the hidden state of the first lstm in the fcblock to the next
        todo:
            Initialize a list of bidirectional states and num_layers states for the FCBlocks(this requires not only saving 
            the model state dict but in order to reconstruct the model you must have saved these states in an extenal file)
        """
        super(FxFCModel, self).__init__() 
        self.num_features = num_features
        self.blocks = nn.ModuleList()
        self.block_type = block_type
        self.units = units
        self.out_units = out_units
        self.bidirectional = bidirectional
        self.num_layers = num_layers
        self.is_encoder = is_encoder
        self.use_batch_norm = use_batch_norm
        self.encoder_latent_dim = encoder_latent_dim
        self.is_decoder = is_decoder
        self.activation = activation
        self.pass_states = pass_states
        self.pass_block_hidden_state = pass_block_hidden_state
        self.console_logger = createLogger(logging.INFO, is_consoleLogger=True)

        # if self.out_units and len(self.out_units) == len(self.units):
        for i in range(len(self.units)):
            if i == 0:
                in_features = self.num_features   
            else:
                if not self.out_units:
                    in_features = self.units[i-1] if not self.bidirectional else self.units[i-1]*2
                else:
                    in_features = self.out_units[i-1] if not self.bidirectional else self.out_units[i-1]*2
            hidden_size = self.units[i]
            output_size = self.out_units[i] if self.out_units else hidden_size
            self.blocks.append(FCBlock(in_features, hidden_size, output_size, self.block_type,
                                        num_layers=self.num_layers, bidirectional=self.bidirectional, activation=self.activation,
                                        use_batch_norm = self.use_batch_norm, pass_block_hidden_state = self.pass_block_hidden_state))

        out_features = encoder_latent_dim if self.is_encoder else 1
        if self.bidirectional:
            if  not self.out_units:
                self.fc_in_features = self.units[-1]*2
            else:
                self.fc_in_features = self.out_units[-1]*2
        else:
            if  not self.out_units:
                self.fc_in_features = self.units[-1]
            else:
                self.fc_in_features = self.out_units[-1]
        self.fc = nn.Linear(in_features = self.fc_in_features, out_features=out_features)

    def forward(self, x):
        for idx, block in enumerate(self.blocks):
            # note
            # lstm output: o, (h, c)
            # rnn and gru output: o, h
            prev_state = None
            if idx > 0 and self.pass_states:
                if self.block_type == "lstm":
                    x, (h2, c2) = block(x, prev_state)
                    prev_state = (h2, c2)
                else:
                    x, h2 = block(x, prev_state)
                    prev_state = h2
            else:
                if self.block_type == "lstm":
                    x, (h2, c2) = block(x) # the 2 represents that these states are for the second block in the FCBlock
                    prev_state = (h2, c2)
                else:
                    x, h2 = block(x)    
                    prev_state = h2

        if not self.is_encoder:
            # h2 = h2.squeeze(0) # this only works on single single direction layers
            final_output = x[:, -1, :]
            x = self.fc(final_output)
            return x
        else:
            return h2.squeeze(0)

class FxFCEncoder(nn.Module):
    def __init__(self, num_features,
                 block_type=None,
                 units=None,
                 out_units=None,
                 num_layers=1, 
                 activation="tanh",
                 latent_dim=None, 
                 use_batch_norm = False):
        """
        Parameters:
            num_features: the number of features per sequence eg if we have a seq [1., 2., 3., 4.] then the n_features = 4
            block_type: This is one of "lstm", "rnn", "gru" for the FCBlocks
            units: A list of hidden sizes as they are supposed to propagate through the blocks
            out_units: The output sizes of the the blocks. This also affects the input shapes of the block of the preceeding blocks after the first has been set
            num_layers: The number of layers in the FCBlocks
            activation: The activation to use. One of "tanh", "relu"
            latent_dim: the dimension for the latent representation of the encoder
            use_batch_norm: Whether to use batch normalization in the FCBlocks
        """
        super(FxFCEncoder, self).__init__()
        self.num_features = num_features 
        self.block_type = block_type 
        self.units = units 
        self.out_units = out_units
        self.num_layers = num_layers 
        self.activation = activation
        self.latent_dim = latent_dim
        self.use_batch_norm = use_batch_norm

        self.encoder = FxFCModel(num_features=self.num_features, block_type=self.block_type,
                                 units=self.units, out_units=self.out_units, num_layers=self.num_layers,
                                 is_encoder=True, activation=self.activation, encoder_latent_dim=self.latent_dim,
                                 use_batch_norm = self.use_batch_norm)
        
    def forward(self, input_data):
        # Initialize hidden and cell states
        h_t, c_t = (torch.zeros(self.num_layers, input_data.size(0), self.units[-1]).to(input_data.device),
                    torch.zeros(self.num_layers, input_data.size(0), self.units[-1]).to(input_data.device))
        
        # Initialize the encoded output
        # input_encoded = Variable(torch.zeros(input_data.size(0), input_data.size(1), self.units[-1])).to(input_data.device)
        input_encoded = torch.zeros(input_data.size(0), input_data.size(1), self.units[-1]).to(input_data.device)

        # Process each timestep
        for t in range(input_data.size(1)):
            x_t = input_data[:, t, :].unsqueeze(1)  # Get the t-th timestep
            if self.block_type == "lstm":
                _, (h_t, c_t) = self.encoder(x_t, (h_t, c_t))
            else:
                _, h_t = self.encoder(x_t, h_t)
            input_encoded[:, t, :] = h_t[-1]  # Store the last layer's hidden state

        return input_encoded

class FxFCDecoder(nn.Module):
    def __init__(self, num_features,
                 block_type = None,
                 units:list = None,
                 out_units:list = None,
                 num_layers = 1,
                 activation = "tanh", 
                 use_batch_norm = False):
        """
        Parameters:
            num_features: the number of features per sequence eg if we have a seq [1., 2., 3., 4.] then the n_features = 4
            block_type: This is one of "lstm", "rnn", "gru" for the FCBlocks
            units: A list of hidden sizes as they are supposed to propagate through the blocks
            out_units: The output sizes of the the blocks. This also affects the input shapes of the block of the preceeding blocks after the first has been set
            num_layers: The number of layers in the FCBlocks
            activation: The activation to use. One of "tanh", "relu"
            use_batch_norm: Whether to use batch normalization in the FCBlocks
        """
        super(FxFCDecoder, self).__init__()
        self.num_features = num_features 
        self.block_type = block_type 
        self.units = units 
        self.out_units = out_units  
        self.num_layers = num_layers 
        self.activation = activation
        self.use_batch_norm = use_batch_norm

        self.decoder = FxFCModel(num_features=self.num_features, block_type=self.block_type, 
                                 units=self.units, num_layers=self.num_layers, is_decoder=True, 
                                 out_units=self.out_units, activation=self.activation, use_batch_norm = self.use_batch_norm)

    def forward(self, x):
        # return self.decoder(x)
        pass # for now

class FxFCAutoEncoder(nn.Module):
    def __init__(self, num_features,
                 block_types:tuple = ("lstm", "lstm"),
                 units:tuple = None,
                 out_units:tuple = None,
                 num_layers:tuple = (1,1),
                 activations:tuple = ("tanh", "tanh"),
                 latent_dim = 128):
        """
        Parameters:
            num_features: the number of features per sequence eg if we have a seq [1., 2., 3., 4.] then the n_features = 4
            block_types: A tuple of the block types for the encoder and decoder
            units: A tuple of the hidden sizes for the encoder and decoder
            out_units: A tuple of the output sizes for the encoder and decoder
            num_layers: A tuple of the number of layers for the encoder and decoder
            activations: A tuple of the activation functions for the encoder and decoder
            latent_dim: the dimension for the latent representation of the encoder
        """
        super(FxFCEncoder, self).__init__()
        self.num_features = num_features 
        self.block_types = block_types 
        self.encoder_block_type = self.block_types[0]
        self.decoder_block_type = self.block_types[1]

        self.units = units 
        self.encoder_units = self.units[0]
        self.decoder_units = self.units[1]

        self.out_units = out_units
        self.encoder_out_units = self.out_units[0]
        self.decoder_out_units = self.out_units[1]

        self.num_layers = num_layers 
        self.encoder_num_layers = self.num_layers[0]
        self.decoder_num_layers = self.num_layers[1]

        self.activations = activations
        self.encoder_activation = self.activations[0]
        self.decoder_activation = self.activations[0]

        self.encoder_latent_dim = latent_dim

        self.encoder = FxFCEncoder(num_features=self.num_features, block_type=self.encoder_block_type,
                                   units=self.encoder_block_type, out_units=self.encoder_out_units,
                                   num_layers=self.encoder_num_layers, activation=self.encoder_activation)
        
        self.decoder_num_features = self.encoder_out_units[-1] if self.encoder_out_units else self.encoder_units[-1] 
        self.decoder = FxFCDecoder(num_features=self.decoder_num_features, block_type=self.decoder_block_type,
                                   units=self.decoder_units, out_units=self.decoder_out_units, 
                                   num_layers=self.decoder_num_layers, activation=self.decoder_activation)
        
    def forward(self, x):
        x = self.encoder(x)
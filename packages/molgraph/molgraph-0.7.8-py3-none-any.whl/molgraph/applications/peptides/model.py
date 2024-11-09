import tensorflow as tf 
from tensorflow import keras

from molgraph import layers
from molgraph import GraphTensor


def PepGNN( 
    spec: GraphTensor.Spec,
    message_layer: str | keras.layers.Layer = layers.GATv2Conv,
    message_steps: int = 4,
    message_units: int = 128,
    recurrent_units: int = 256,
    recurrent_steps: int = 1,
    hidden_units: int = 512,
    hidden_steps: int = 1,
    output_units: int = 1,
    output_activation: str = None,
    freeze: bool = False,
    **kwargs,
) -> keras.Model:
    
    kwargs.pop('node_preprocessing') # tmp
    kwargs.pop('edge_preprocessing') # tmp

    if isinstance(message_layer, str):
        message_layer = getattr(layers, message_layer.rstrip('Conv') + 'Conv')
    
    graph_layers = [layers.NodeFeatureProjection(units=message_units)]
    graph_layers += [
        message_layer(units=message_units, **kwargs)
        for _ in range(message_steps)
    ]
    for layer in graph_layers[1:]:
        layer.trainable = not freeze 

    rnn_layers = [
        keras.layers.Bidirectional(
            keras.layers.LSTM(recurrent_units, return_sequences=True)
        )
        for _ in range(recurrent_steps - 1)
    ]
    rnn_layers += [
        keras.layers.Bidirectional(
            keras.layers.LSTM(recurrent_units, return_sequences=False)
        )
    ]
    dense_layers = [
        keras.layers.Dense(units=hidden_units, activation='elu')
        for _ in range(hidden_steps)
    ]
    dense_layers += [
        keras.layers.Dense(units=output_units, activation=output_activation)
    ]
    return tf.keras.Sequential([
        layers.GNNInputLayer(type_spec=spec),
        layers.GNN(graph_layers),
        layers.SuperNodeReadout('node_super_indicator'),
        keras.Sequential(rnn_layers),
        keras.Sequential(dense_layers),
    ])



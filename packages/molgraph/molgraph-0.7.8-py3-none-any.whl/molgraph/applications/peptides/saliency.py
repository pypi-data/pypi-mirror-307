import tensorflow as tf

from molgraph import models
from molgraph import GraphTensor 

from .definitions import SUPER_NODE_INDICATOR 


NODE_SALIENCY = 'node_saliency'


class PepSaliency(models.SaliencyMapping):
    
    def __call__(
        self, 
        x: GraphTensor, 
        y: tf.Tensor | None = None, 
        node_level: bool = True
    ) -> tf.RaggedTensor:
        if isinstance(x.node_feature, tf.RaggedTensor):
            x = x.merge()
        saliency_values = super().__call__(x, y)
        x = x.update({NODE_SALIENCY: saliency_values})
        mask = tf.cast(getattr(x, SUPER_NODE_INDICATOR), tf.bool)
        mask = (mask == False if node_level else mask)
        node_saliency = tf.boolean_mask(getattr(x, NODE_SALIENCY), mask)
        graph_indicator = tf.boolean_mask(x.graph_indicator, mask)
        return tf.RaggedTensor.from_value_rowids(node_saliency, graph_indicator)


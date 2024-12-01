import os
os.environ["TF_ENABLE_ONEDNN_OPTS"]="0"
import numpy as np
from tensorflow.keras import layers, models
from tensorflow.keras import backend as K
from tensorflow.keras.optimizers import Adam
import tensorflow as tf

class sampling(layers.Layer):
    pass    
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"]="0"
import numpy as np
from tensorflow.keras import layers, models
from tensorflow.keras import backend as K
from tensorflow.keras.optimizers import Adam
import tensorflow as tf

class Sampling(layers.Layer):
    def call(self,inputs):
        mean,log_var=inputs
        epsilon=K.random_normal(shape=tf.shape(log_var))
        return mean+(K.exp(0.5*log_var)*epsilon)

class Encoder(models.Model):
    def __init__(self,latent_dim):
        super(Encoder,self).__init__()
        self.layer1=layers.Dense(35,activation='relu')
        self.layer2=layers.Dense(20,activation='relu')
        self.mean=layers.Dense(latent_dim)
        self.log_var=layers.Dense(latent_dim)
        self.sampling=Sampling()
    def call(self,input):
        x=self.layer1(input)
        x=self.layer2(x)
        mean=self.mean(x)
        log_var=self.log_var(x)
        z=self.sampling([mean,log_var])
        return mean,log_var,z

class Decoder(models.Model):
    def __init__(self,original_dim):
        super(Decoder,self).__init__()
        self.layer3=layers.Dense(20,activation='relu')
        self.layer4=layers.Dense(35,activation='relu')
        self.output_layer=layers.Dense(original_dim,activation='sigmoid')
    def call(self,input):
        x=self.layer3(input)
        x=self.layer4(x)
        x=self.output_layer(x)
        return x

class VAE(models.Model):
    def __init__(self,original_dim,latent_dim):
        super(VAE,self).__init__()
        self.encoder=Encoder(latent_dim)
        self.decoder=Decoder(original_dim)
        self.original_dim=original_dim
        self.latent_dim=latent_dim
    def call(self,input):
        mean,log_var,z=self.encoder(input)
        output=self.decoder(z)
        kl_loss=-0.5*K.sum(1+log_var-K.square(mean)-K.exp(log_var),axis=-1)
        self.add_loss(K.mean(kl_loss)/self.original_dim)
        return output
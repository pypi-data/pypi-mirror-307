# __all__ = ('dfchk')
import tensorflow as tf

#%%
# from https://github.com/yuxiaohuang/teaching
def normalize(data, label):
  """
  Normalize the data

  Parameters
  ----------
  data: the data
  label: the label
  
  Returns
  ----------
  The normalized data and label
  """

  # Normalize the data
  data_normalized = tf.cast(data, tf.float64) / 255

  return data_normalized, label
  

#%%
def resize(data, label):
  """
  Resize the data into the default input size of the pretrained model

  Parameters
  ----------
  data: the data
  label: the label
  
  Returns
  ----------
  The resized data and label
  """

  # Resize the data into the default input size of the pretrained model
  data_resized = tf.image.resize(data, input_size)

  return data_resized, label

#%%
def preprocess_pretrain(data, label):
  """
  Preprocess the data using pretrained model

  Parameters
  ----------
  data: the data
  label: the label
  
  Returns
  ----------
  The preprocessed data using pretrained model
  """

  # Preprocess the data
  data_preprocessed = preprocess_input(data)

  return data_preprocessed, label

#%%

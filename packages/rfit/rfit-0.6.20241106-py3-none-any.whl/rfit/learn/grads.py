import pandas as pd
import numpy as np
import sys
# import os
# import matplotlib.pyplot as plt
from sklearn.base import BaseEstimator, RegressorMixin
# from sklearn.manifold import TSNE
# from sklearn.model_selection import PredefinedSplit
# from sklearn.model_selection import GridSearchCV
# from sklearn.model_selection import StratifiedKFold
# from sklearn.metrics import precision_recall_fscore_support
# from sklearn.metrics import roc_auc_score

#%%
# ### The normal equation
class LinearRegression_NE(BaseEstimator, RegressorMixin):
  """Linear regression implemented using the normal equation (Yuxiao Huang)"""

  def fit(self, X, y):
    """
    The fit function
    
    Parameters
    ----------
    X : the feature matrix
    y : the target vector
    """
    
    # Get the augmented feature matrix, [1, X]
    IX = np.hstack((np.ones((X.shape[0], 1)), X))

    # Get the optimal solution using the normal equation
    self.theta = np.linalg.pinv(IX).dot(y)
    # pinv() gives the Moore-Penrose pseudo-inverse of a matrix 
    # particularly useful when matrix A is not a sqaure, or A is singular.
    
    # Get the predicted target vector
    y_pred = self.net_input(IX)
                    
    # Get the loss (MSE)
    self.loss = ((y - y_pred) ** 2).sum() / IX.shape[0]
      
  def net_input(self, IX):
    """
    Get the predicted target vector
    
    Parameters
    ----------
    IX : The augmented feature matrix [1, X]
    
    Returns
    ----------
    The predicted target vector
    """
    
    return IX.dot(self.theta)

  def predict(self, X):
    """
    The predict function
    
    Parameters
    ----------
    X : the feature matrix
    
    Returns
    ----------
    The predicted value of the target
    """
    
    # Get the augmented feature matrix [1, X]
    IX = np.hstack((np.ones((X.shape[0], 1)), X))
    
    return self.net_input(IX)

#%%
# ### Batch gradient descent (BGD)
class LinearRegression_BGD(BaseEstimator, RegressorMixin):
  """Linear regression implemented using batch gradient descent and regularization (lasso, ridge and elastic net)"""
  
  def __init__(self, 
              max_iter=100, 
              eta=10 ** -2,
              penalty='l2',
              alpha=0.0001, 
              gamma=0.15,
              random_state=42):
    
    # The maximum number of epochs
    self.max_iter = max_iter
    
    # The learning rate
    self.eta = eta
    
    # The regularization term
    self.penalty=penalty
    
    # The regularization parameter
    self.alpha=alpha

    # The elastic net mixing parameter
    self.gamma=gamma

    # The random state
    self.random_state = random_state

  def fit(self, X_train, y_train, X_val=None, y_val=None):
    """
    The fit function
    
    Parameters
    ----------
    X_train : The training feature matrix
    y_train : The training target vector
    X_val : The validation feature matrix
    y_val : The validation target vector
    """
    
    # Get the augmented training feature matrix, [1, X_train]
    IX_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
    
    # Get the random number generator
    self.rgen = np.random.RandomState(seed=self.random_state)
    
    # Initialize the parameters
    self.theta = self.rgen.normal(loc=0.0, scale=0.01, size=IX_train.shape[1])
    
    # Initialize the training and validation loss
    self.loss_train, self.loss_val = [], []
    
    # For each epoch
    for _ in range(self.max_iter):
      # Get the predicted target vector on the training data
      y_train_pred = self.net_input(IX_train)
      
      # Get the training error
      error_train = y_train - y_train_pred
                  
      # Get the training mse
      mse_train = (error_train ** 2).sum() / IX_train.shape[0]
      
      # Update the parameters
      # If no regularization
      if self.penalty == None:
          self.theta += self.eta * (2 / IX_train.shape[0] * IX_train.T.dot(error_train))
      # If lasso
      elif self.penalty == 'l1':
          self.theta += self.eta * (2 / IX_train.shape[0] * IX_train.T.dot(error_train) 
                                    - self.alpha * np.append([0], np.sign(self.theta[1:])))
      # If ridge
      elif self.penalty == 'l2':
          self.theta += self.eta * (2 / IX_train.shape[0] * IX_train.T.dot(error_train) 
                                    - self.alpha * np.append([0], self.theta[1:]))
      # If elastic net
      elif self.penalty == 'elasticnet':
          self.theta += self.eta * (2 / IX_train.shape[0] * IX_train.T.dot(error_train) 
                                    - self.alpha * self.gamma * np.append([0], np.sign(self.theta[1:])) 
                                    - self.alpha * (1 - self.gamma) * np.append([0], self.theta[1:]))
                      
      # Update the training loss
      self.loss_train.append(mse_train)
      
      # If the validation feature matrix and target vector are available
      if X_val is not None and y_val is not None:
        # Get the augmented validation feature matrix, [1, X_val]
        IX_val = np.hstack((np.ones((X_val.shape[0], 1)), X_val))
        
        # Get the predicted target vector on the validation data
        y_val_pred = self.net_input(IX_val)
        
        # Get the validation error
        error_val = y_val - y_val_pred
        
        # Get the validation mse
        mse_val = (error_val ** 2).sum() / IX_val.shape[0]
        
        # Update the validation loss
        self.loss_val.append(mse_val)

  def net_input(self, IX):
    """
    Get the predicted target vector
    
    Parameters
    ----------
    IX : The augmented feature matrix [1, X]
    
    Returns
    ----------
    The predicted target vector
    """
    
    return IX.dot(self.theta)

  def predict(self, X):
    """
    The predict function
    
    Parameters
    ----------
    X : the feature matrix
    
    Returns
    ----------
    The predicted value of the target
    """
    
    # Get the augmented feature matrix [1, X]
    IX = np.hstack((np.ones((X.shape[0], 1)), X))
    
    return self.net_input(IX)

#%%
# ### Stochastic gradient descent (SGD)
class LinearRegression_SGD(BaseEstimator, RegressorMixin):
  """Linear regression implemented using stochastic gradient descent and regularization (lasso, ridge and elastic net)"""
  
  def __init__(self, 
              max_iter=100,
              shuffle=True,
              eta=10 ** -2, 
              penalty='l2',
              alpha=0.0001, 
              gamma=0.15,
              random_state=42):
    
    # The maximum number of epochs
    self.max_iter = max_iter
    
    # Whether to shuffle samples in each epoch
    self.shuffle = shuffle
    
    # The learning rate
    self.eta = eta
    
    # The regularization term
    self.penalty=penalty
    
    # The regularization parameter
    self.alpha=alpha

    # The elastic net mixing parameter
    self.gamma=gamma
    
    # The random state
    self.random_state = random_state

  def fit(self, X_train, y_train, X_val=None, y_val=None):
    """
    The fit function
    
    Parameters
    ----------
    X_train : The training feature matrix
    y_train : The training target vector
    X_val : The validation feature matrix
    y_val : The validation target vector
    """
    
    # Get the augmented training feature matrix, [1, X_train]
    IX_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
    
    # Get the indices of the augmented training feature matrix
    idxs_train = np.array(range(IX_train.shape[0]))
    
    # Get the random number generator
    self.rgen = np.random.RandomState(seed=self.random_state)
    
    # Initialize the parameters
    self.theta = self.rgen.normal(loc=0.0, scale=0.01, size=IX_train.shape[1])
    
    # Initialize the training and validation loss
    self.loss_train, self.loss_val = [], []
    
    # For each epoch
    for _ in range(self.max_iter):
      if self.shuffle is True:
        # Shuffle the indices
        self.rgen.shuffle(idxs_train)
          
      # Initialize the mse
      mse_train = 0
      
      # For each sample
      for i in idxs_train:                
        # Get the predicted target vector on the training data
        y_train_pred = self.net_input(IX_train[i, :])

        # Get the training error
        error_train = y_train[i] - y_train_pred

        # Get the training mse
        mse_train += (error_train ** 2) / IX_train.shape[0]

        # Update the parameters
        # If no regularization
        if self.penalty == None:
          self.theta += self.eta * (2 * IX_train[i, :].T.dot(error_train))
        # If lasso
        elif self.penalty == 'l1':
          self.theta += self.eta * (2 * IX_train[i, :].T.dot(error_train) 
                                    - self.alpha * np.append([0], np.sign(self.theta[1:])))
        # If ridge
        elif self.penalty == 'l2':
          self.theta += self.eta * (2 * IX_train[i, :].T.dot(error_train) 
                                    - self.alpha * np.append([0], self.theta[1:]))
        # If elastic net
        elif self.penalty == 'elasticnet':
          self.theta += self.eta * (2 * IX_train[i, :].T.dot(error_train) 
                                    - self.alpha * self.gamma * np.append([0], np.sign(self.theta[1:])) 
                                    - self.alpha * (1 - self.gamma) * np.append([0], self.theta[1:]))

      # Update the training loss
      self.loss_train.append(mse_train)

      # If the validation feature matrix and target vector are available
      if X_val is not None and y_val is not None:
        # Get the augmented validation feature matrix, [1, X_val]
        IX_val = np.hstack((np.ones((X_val.shape[0], 1)), X_val))

        # Get the predicted target vector on the validation data
        y_val_pred = self.net_input(IX_val)

        # Get the validation error
        error_val = y_val - y_val_pred

        # Get the validation mse
        mse_val = (error_val ** 2).sum() / IX_val.shape[0]

        # Update the validation loss
        self.loss_val.append(mse_val)
              
  def net_input(self, IX):
    """
    Get the predicted target vector
    
    Parameters
    ----------
    IX : The augmented feature matrix [1, X]
    
    Returns
    ----------
    The predicted target vector
    """
    
    return IX.dot(self.theta)

  def predict(self, X):
    """
    The predict function
    
    Parameters
    ----------
    X : the feature matrix
    
    Returns
    ----------
    The predicted value of the target
    """
    
    # Get the augmented feature matrix [1, X]
    IX = np.hstack((np.ones((X.shape[0], 1)), X))
    
    return self.net_input(IX)

#%%
# ### Mini-batch gradient descent (MBGD)
class LinearRegression_MBGD(BaseEstimator, RegressorMixin):
  """Linear regression implemented using mini-batch gradient descent and regularization (lasso, ridge and elastic net)"""
  
  def __init__(self,
                max_iter=100,
                shuffle=True,
                batch_size=32,
                eta=10 ** -2, 
                penalty='l2',
                alpha=0.0001, 
                gamma=0.15,
                random_state=42):
      
    # The maximum number of epochs
    self.max_iter = max_iter
    
    # Whether to shuffle samples in each epoch
    self.shuffle = shuffle
    
    # The size of minibatches for stochastic optimizers
    self.batch_size = batch_size
    
    # The learning rate
    self.eta = eta
    
    # The regularization term
    self.penalty=penalty
    
    # The regularization parameter
    self.alpha=alpha

    # The elastic net mixing parameter
    self.gamma=gamma
    
    # The random state
    self.random_state = random_state

  def fit(self, X_train, y_train, X_val=None, y_val=None):
    """
    The fit function
    
    Parameters
    ----------
    X_train : The training feature matrix
    y_train : The training target vector
    X_val : The validation feature matrix
    y_val : The validation target vector
    """
    
    # Get the augmented training feature matrix, [1, X_train]
    IX_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
    
    # Get the random number generator
    self.rgen = np.random.RandomState(seed=self.random_state)
    
    # Initialize the parameters
    self.theta = self.rgen.normal(loc=0.0, scale=0.01, size=IX_train.shape[1])
    
    # Initialize the training and validation loss
    self.loss_train, self.loss_val = [], []
    
    # For each epoch
    for _ in range(self.max_iter):
      # Get the indices of the training data
      idxs_train = np.array(range(IX_train.shape[0]))
      
      # Get the minibatches of the training data
      mbs = self.get_minibatches(idxs_train)

      # Initialize the training mse
      mse_train = 0

      # For each minibatch
      for mb in mbs:   
        # Get the augmented training feature matrix and target vector
        IX_train_mb, y_train_mb = IX_train[mb,:], y_train[mb]

        # Get the predicted target vector on the training data
        y_train_mb_pred = self.net_input(IX_train_mb)

        # Get the training error
        error_train = y_train_mb - y_train_mb_pred

        # Get the training mse
        mse_train += (error_train ** 2).sum() / IX_train.shape[0]
        
        # Update the parameters
        # If no regularization
        if self.penalty == None:
            self.theta += self.eta * (2 / IX_train_mb.shape[0] * IX_train_mb.T.dot(error_train))
        # If lasso
        elif self.penalty == 'l1':
            self.theta += self.eta * (2 / IX_train_mb.shape[0] * IX_train_mb.T.dot(error_train) 
                                      - self.alpha * np.append([0], np.sign(self.theta[1:])))
        # If ridge
        elif self.penalty == 'l2':
            self.theta += self.eta * (2 / IX_train_mb.shape[0] * IX_train_mb.T.dot(error_train) 
                                      - self.alpha * np.append([0], self.theta[1:]))
        # If elastic net
        elif self.penalty == 'elasticnet':
            self.theta += self.eta * (2 / IX_train_mb.shape[0] * IX_train_mb.T.dot(error_train) 
                                      - self.alpha * self.gamma * np.append([0], np.sign(self.theta[1:])) 
                                      - self.alpha * (1 - self.gamma) * np.append([0], self.theta[1:]))

      # Update the training loss
      self.loss_train.append(mse_train)
      
      # If the validation feature matrix and target vector are available
      if X_val is not None and y_val is not None:
        # Get the augmented validation feature matrix, [1, X_val]
        IX_val = np.hstack((np.ones((X_val.shape[0], 1)), X_val))
        
        # Get the predicted target vector on the validation data
        y_val_pred = self.net_input(IX_val)
        
        # Get the validation error
        error_val = y_val - y_val_pred
        
        # Get the validation mse
        mse_val = (error_val ** 2).sum() / IX_val.shape[0]
        
        # Update the validation loss
        self.loss_val.append(mse_val)

  def get_minibatches(self, idxs):
    """
    Get the minibatches
    
    Parameters
    ----------
    idxs : The indices of the data
    
    Returns
    ----------
    The minibatches
    """
    
    # Initialize the minibatches
    mbs = []
    
    if self.shuffle is True:
      # Shuffle the indices
      self.rgen.shuffle(idxs)
            
    # Get the number of minibatches
    n_batch = len(idxs) // self.batch_size
    
    # For each minibatch
    for i in range(n_batch):
      # Get the first and last index (exclusive) of the minibatch
      first_idx = i * self.batch_size
      last_idx = min((i + 1) * self.batch_size, len(idxs))
                              
      # Get the minibatch
      mb = idxs[first_idx : last_idx]
      
      # Update the minibatches
      mbs.append(mb)

    return mbs

  def net_input(self, IX):
    """
    Get the predicted target vector
    
    Parameters
    ----------
    IX : The augmented feature matrix [1, X]
    
    Returns
    ----------
    The predicted target vector
    """
    
    return IX.dot(self.theta)

  def predict(self, X):
    """
    The predict function
    
    Parameters
    ----------
    X : the feature matrix
    
    Returns
    ----------
    The predicted value of the target
    """
    
    # Get the augmented feature matrix [1, X]
    IX = np.hstack((np.ones((X.shape[0], 1)), X))
    
    return self.net_input(IX)
      
#%%
# ### Mini-batch gradient descent (MBGD)
class LogisticRegression_MBGD(BaseEstimator, RegressorMixin):
  """Logistic regression implemented using mini-batch gradient descent and regularization (lasso, ridge and elastic net)"""
  
  def __init__(self,
                max_iter=100,
                shuffle=True,
                batch_size=32,
                eta=10 ** -2, 
                penalty='l2',
                alpha=1, 
                gamma=0.5,
                random_state=42):
      
      # The maximum number of epochs
      self.max_iter = max_iter
      
      # Whether to shuffle samples in each epoch
      self.shuffle = shuffle
      
      # The size of minibatches for stochastic optimizers
      self.batch_size = batch_size
      
      # The learning rate
      self.eta = eta
      
      # The regularization term
      self.penalty=penalty
      
      # The regularization parameter
      self.alpha=alpha

      # The elastic net mixing parameter
      self.gamma=gamma
      
      # The random state
      self.random_state = random_state

  def fit(self, X_train, y_train, X_val=None, y_val=None):
    """
    The fit function
    
    Parameters
    ----------
    X_train : The training feature matrix
    y_train : The training target vector
    X_val : The validation feature matrix
    y_val : The validation target vector
    """
    
    # Get the augmented training feature matrix, [1, X_train]
    IX_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
    
    # Get the random number generator
    self.rgen = np.random.RandomState(seed=self.random_state)
    
    # Get the unique classes of the target
    self.classes = np.unique(y_train)
    
    # Get the number of unique classes of the target
    self.n_classes = len(self.classes)
    
    # If binary classification
    if self.n_classes == 2:
      # Make a copy of y_train
      Y_train = np.copy(y_train)       
    # If multi-class classification
    else:
      # Get the one-hot-encoded training target matrix
      Y_train = pd.get_dummies(y_train).values
    
    # Initialize the parameters
    # If binary classification
    if self.n_classes == 2:
      self.theta = self.rgen.normal(loc=0.0, scale=0.01, size=IX_train.shape[1])
    # If multi-class classification
    else:
      self.theta = self.rgen.normal(loc=0.0, scale=0.01, size=(IX_train.shape[1], self.n_classes))            
    
    # Initialize the training and validation loss
    self.loss_train, self.loss_val = [], []
    
    # For each epoch
    for _ in range(self.max_iter):
      # Get the indices of the training data
      idxs_train = np.array(range(IX_train.shape[0]))
      
      # Get the minibatches of the training data
      mbs = self.get_minibatches(idxs_train)

      # Initialize the training mse
      mse_train = 0

      # For each minibatch
      for mb in mbs:   
        # Get the augmented training feature matrix and target matrix
        # If binary classification
        if self.n_classes == 2:
          IX_train_mb, Y_train_mb = IX_train[mb,:], Y_train[mb]       
        # If multi-class classification
        else:
          IX_train_mb, Y_train_mb = IX_train[mb,:], Y_train[mb,:]       
                                  
        # Get the net input matrix
        N_train_mb = self.net_input(IX_train_mb)
        
        # Get the probability matrix
        P_train_mb = self.activation(N_train_mb)
                                  
        # Get the training error
        error_train = Y_train_mb - P_train_mb

        # Get the training mse
        mse_train += (error_train ** 2).sum() / IX_train.shape[0]
        
        # Update the parameters
        # If no regularization
        if self.penalty == None:
          self.theta += self.eta / IX_train_mb.shape[0] * (IX_train_mb.T.dot(error_train))
        # If lasso
        elif self.penalty == 'l1':
          # If binary classification
          if self.n_classes == 2:
              self.theta += self.eta * (1 / IX_train_mb.shape[0] * IX_train_mb.T.dot(error_train) 
                                        - self.alpha * np.append([0], np.sign(self.theta[1:])))
          # If multi-class classification
          else:
              self.theta += self.eta * (1 / IX_train_mb.shape[0] * IX_train_mb.T.dot(error_train) 
                                        - self.alpha * np.append(np.zeros((1, self.theta.shape[1])), np.sign(self.theta[1:,:]), axis=0))                        
        # If ridge
        elif self.penalty == 'l2':
          # If binary classification
          if self.n_classes == 2:
              self.theta += self.eta * (1 / IX_train_mb.shape[0] * IX_train_mb.T.dot(error_train) 
                                        - self.alpha * np.append([0], self.theta[1:]))
          # If multi-class classification
          else:
              self.theta += self.eta * (1 / IX_train_mb.shape[0] * IX_train_mb.T.dot(error_train) 
                                        - self.alpha * np.append(np.zeros((1, self.theta.shape[1])), self.theta[1:,:], axis=0))                        
        # If elastic net
        elif self.penalty == 'elasticnet':
          # If binary classification
          if self.n_classes == 2:
              self.theta += self.eta * (1 / IX_train_mb.shape[0] * IX_train_mb.T.dot(error_train) 
                                        - self.alpha * self.gamma * np.append([0], np.sign(self.theta[1:])) 
                                        - self.alpha * (1 - self.gamma) * np.append([0], self.theta[1:]))
          # If multi-class classification
          else:
              self.theta += self.eta * (1 / IX_train_mb.shape[0] * IX_train_mb.T.dot(error_train) 
                                        - self.alpha * self.gamma * np.append(np.zeros((1, self.theta.shape[1])), np.sign(self.theta[1:,:]), axis=0) 
                                        - self.alpha * (1 - self.gamma) * np.append(np.zeros((1, self.theta.shape[1])), self.theta[1:,:], axis=0))
                                        
      # Update the training loss
      self.loss_train.append(mse_train)
      
      # If the validation feature matrix and target vector are available
      if X_val is not None and y_val is not None:
        # Get the augmented validation feature matrix, [1, X_val]
        IX_val = np.hstack((np.ones((X_val.shape[0], 1)), X_val))

        # If binary classification
        if self.n_classes == 2:
          # Make a copy of y_val
          Y_val = np.copy(y_val)            
        # If multi-class classification
        else:
          # Get the one-hot-encoded validation target matrix
          Y_val = pd.get_dummies(y_val).values
        
        # Get the net input matrix on the validation data
        N_val = self.net_input(IX_val)
        
        # Get the probability matrix on the validation data
        P_val = self.activation(N_val)
                                  
        # Get the validation error
        error_val = Y_val - P_val
        
        # Get the validation mse
        mse_val = (error_val ** 2).sum() / IX_val.shape[0]
        
        # Update the validation loss
        self.loss_val.append(mse_val)

  def get_minibatches(self, idxs):
    """
    Get the minibatches
    
    Parameters
    ----------
    idxs : The indices of the data
    
    Returns
    ----------
    The minibatches
    """
    
    # Initialize the minibatches
    mbs = []
    
    if self.shuffle is True:
      # Shuffle the indices
      self.rgen.shuffle(idxs)
            
    # Get the number of minibatches
    n_batch = len(idxs) // self.batch_size
    
    # For each minibatch
    for i in range(n_batch):
      # Get the first and last index (exclusive) of the minibatch
      first_idx = i * self.batch_size
      last_idx = min((i + 1) * self.batch_size, len(idxs))
                              
      # Get the minibatch
      mb = idxs[first_idx : last_idx]
      
      # Update the minibatches
      mbs.append(mb)

    return mbs

  def net_input(self, IX):
    """
    Get the net input matrix
    
    Parameters
    ----------
    IX : The augmented feature matrix [1, X]
    
    Returns
    ----------
    The net input matrix
    """
    
    return IX.dot(self.theta)
  
  def activation(self, net_input):
    """
    Get the probability (sigmoid or softmax) matrix
    
    Parameters
    ----------
    net_input : The net input
    
    Returns
    ----------
    The probability (sigmoid or softmax) matrix
    """
    
    # If binary classification
    if self.n_classes == 2:
      # Get the exponent of the negative net input
      neg_net_input_exp = np.exp(-np.clip(net_input, -250, 250))
      
      # Return the sigmoid matrix
      return 1. / (1. + neg_net_input_exp)           
    # If multi-class classification
    else:
      # Get the exponent of the net input
      net_input_exp = np.exp(net_input - np.max(net_input, axis=1).reshape(-1, 1))

      # Return the softmax matrix
      return net_input_exp / np.sum(net_input_exp, axis=1).reshape(-1, 1)
      
  def predict_proba(self, X):
    """
    The predict probability function
    
    Parameters
    ----------
    X : the feature matrix
    
    Returns
    ----------
    The probability (sigmoid or softmax) matrix
    """
    
    # Get the augmented feature matrix [1, X]
    IX = np.hstack((np.ones((X.shape[0], 1)), X))
        
    # Get the net_input matrix
    N = self.net_input(IX)

    return self.activation(N)
  
  def predict(self, X):
    """
    The predict class function
    
    Parameters
    ----------
    X : the feature matrix
    
    Returns
    ----------
    The predicted class vector
    """
    
    # If binary classification
    if self.n_classes == 2:
      return (self.predict_proba(X) >= 0.5) * 1         
    # If multi-class classification
    else:
      return np.argmax(self.predict_proba(X), axis=1)

#%%
# ## Shallow neural networks 
# ### Single-layer perceptron
class SingleLayerPerceptron_MBGD(BaseEstimator, RegressorMixin):
  """Single-layer perceptron implemented using mini-batch gradient descent and regularization (lasso, ridge and elastic net)"""
  
  def __init__(self,
              max_iter=100,
              shuffle=True,
              batch_size=32,
              eta=10 ** -2, 
              penalty='l2',
              alpha=1, 
              gamma=0.5,
              random_state=42):
    
    # The maximum number of epochs
    self.max_iter = max_iter
    
    # Whether to shuffle samples in each epoch
    self.shuffle = shuffle
    
    # The size of minibatches for stochastic optimizers
    self.batch_size = batch_size
    
    # The learning rate
    self.eta = eta
    
    # The regularization term
    self.penalty=penalty
    
    # The regularization parameter
    self.alpha=alpha

    # The elastic net mixing parameter
    self.gamma=gamma
    
    # The random state
    self.random_state = random_state

  def fit(self, X_train, y_train, X_val=None, y_val=None):
    """
    The fit function
    
    Parameters
    ----------
    X_train : The training feature matrix
    y_train : The training target vector
    X_val : The validation feature matrix
    y_val : The validation target vector
    """
    
    # Get the augmented training feature matrix, [1, X_train]
    IX_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
    
    # Get the random number generator
    self.rgen = np.random.RandomState(seed=self.random_state)
    
    # Get the unique classes of the target
    self.classes = np.unique(y_train)
    
    # Get the number of unique classes of the target
    self.n_classes = len(self.classes)
    
    # If binary classification
    if self.n_classes == 2:
      # Make a copy of y_train
      Y_train = np.copy(y_train)       
    # If multi-class classification
    else:
      # Get the one-hot-encoded training target matrix
      Y_train = pd.get_dummies(y_train).values
    
    # Initialize the parameters
    # If binary classification
    if self.n_classes == 2:
      self.theta = self.rgen.normal(loc=0.0, scale=0.01, size=IX_train.shape[1])
    # If multi-class classification
    else:
      self.theta = self.rgen.normal(loc=0.0, scale=0.01, size=(IX_train.shape[1], self.n_classes))            
    
    # Initialize the training and validation loss
    self.loss_train, self.loss_val = [], []
    
    # For each epoch
    for _ in range(self.max_iter):
      # Get the indices of the training data
      idxs_train = np.array(range(IX_train.shape[0]))
      
      # Get the minibatches of the training data
      mbs = self.get_minibatches(idxs_train)

      # Initialize the training mse
      mse_train = 0

      # For each minibatch
      for mb in mbs:   
        # Get the augmented training feature matrix and target matrix
        # If binary classification
        if self.n_classes == 2:
          IX_train_mb, Y_train_mb = IX_train[mb,:], Y_train[mb]       
        # If multi-class classification
        else:
          IX_train_mb, Y_train_mb = IX_train[mb,:], Y_train[mb,:]       
                                  
        # Get the net input matrix
        N_train_mb = self.net_input(IX_train_mb)
        
        # Get the output matrix
        A_train_mb = self.activation(N_train_mb)
                                  
        # Get the training error
        error_train = Y_train_mb - A_train_mb

        # Get the training mse
        mse_train += (error_train ** 2).sum() / IX_train.shape[0]
        
        # Update the parameters
        # If no regularization
        if self.penalty == None:
          self.theta += self.eta / IX_train_mb.shape[0] * (IX_train_mb.T.dot(error_train))
        # If lasso
        elif self.penalty == 'l1':
          # If binary classification
          if self.n_classes == 2:
            self.theta += self.eta * (1 / IX_train_mb.shape[0] * IX_train_mb.T.dot(error_train) 
                                      - self.alpha * np.append([0], np.sign(self.theta[1:])))
          # If multi-class classification
          else:
            self.theta += self.eta * (1 / IX_train_mb.shape[0] * IX_train_mb.T.dot(error_train) 
                                      - self.alpha * np.append(np.zeros((1, self.theta.shape[1])), np.sign(self.theta[1:,:]), axis=0))                        
        # If ridge
        elif self.penalty == 'l2':
          # If binary classification
          if self.n_classes == 2:
            self.theta += self.eta * (1 / IX_train_mb.shape[0] * IX_train_mb.T.dot(error_train) 
                                      - self.alpha * np.append([0], self.theta[1:]))
          # If multi-class classification
          else:
            self.theta += self.eta * (1 / IX_train_mb.shape[0] * IX_train_mb.T.dot(error_train) 
                                      - self.alpha * np.append(np.zeros((1, self.theta.shape[1])), self.theta[1:,:], axis=0))                        
        # If elastic net
        elif self.penalty == 'elasticnet':
          # If binary classification
          if self.n_classes == 2:
            self.theta += self.eta * (1 / IX_train_mb.shape[0] * IX_train_mb.T.dot(error_train) 
                                      - self.alpha * self.gamma * np.append([0], np.sign(self.theta[1:])) 
                                      - self.alpha * (1 - self.gamma) * np.append([0], self.theta[1:]))
          # If multi-class classification
          else:
            self.theta += self.eta * (1 / IX_train_mb.shape[0] * IX_train_mb.T.dot(error_train) 
                                      - self.alpha * self.gamma * np.append(np.zeros((1, self.theta.shape[1])), np.sign(self.theta[1:,:]), axis=0) 
                                      - self.alpha * (1 - self.gamma) * np.append(np.zeros((1, self.theta.shape[1])), self.theta[1:,:], axis=0))
                                          
      # Update the training loss
      self.loss_train.append(mse_train)
      
      # If the validation feature matrix and target vector are available
      if X_val is not None and y_val is not None:
        # Get the augmented validation feature matrix, [1, X_val]
        IX_val = np.hstack((np.ones((X_val.shape[0], 1)), X_val))

        # If binary classification
        if self.n_classes == 2:
          # Make a copy of y_val
          Y_val = np.copy(y_val)            
        # If multi-class classification
        else:
          # Get the one-hot-encoded validation target matrix
          Y_val = pd.get_dummies(y_val).values
        
        # Get the net input matrix on the validation data
        N_val = self.net_input(IX_val)
        
        # Get the output matrix on the validation data
        A_val = self.activation(N_val)
                                  
        # Get the validation error
        error_val = Y_val - A_val
        
        # Get the validation mse
        mse_val = (error_val ** 2).sum() / IX_val.shape[0]
        
        # Update the validation loss
        self.loss_val.append(mse_val)

  def get_minibatches(self, idxs):
    """
    Get the minibatches
    
    Parameters
    ----------
    idxs : The indices of the data
    
    Returns
    ----------
    The minibatches
    """
    
    # Initialize the minibatches
    mbs = []
    
    if self.shuffle is True:
      # Shuffle the indices
      self.rgen.shuffle(idxs)
            
    # Get the number of minibatches
    n_batch = len(idxs) // self.batch_size
    
    # For each minibatch
    for i in range(n_batch):
      # Get the first and last index (exclusive) of the minibatch
      first_idx = i * self.batch_size
      last_idx = min((i + 1) * self.batch_size, len(idxs))
                              
      # Get the minibatch
      mb = idxs[first_idx : last_idx]
      
      # Update the minibatches
      mbs.append(mb)

    return mbs

  def net_input(self, IX):
    """
    Get the net input matrix
    
    Parameters
    ----------
    IX : The augmented feature matrix [1, X]
    
    Returns
    ----------
    The net input matrix
    """
    
    return IX.dot(self.theta)
  
  def activation(self, net_input):
    """
    Get the probability (sigmoid or softmax) matrix
    
    Parameters
    ----------
    net_input : The net input
    
    Returns
    ----------
    The probability (sigmoid or softmax) matrix
    """
    
    # If binary classification
    if self.n_classes == 2:
        return (net_input >= 0) * 1          
    # If multi-class classification
    else:
      # Get the exponent of the net input
      net_input_exp = np.exp(net_input - np.max(net_input, axis=1).reshape(-1, 1))

      # Return the softmax matrix
      return net_input_exp / np.sum(net_input_exp, axis=1).reshape(-1, 1)
      
  def predict_proba(self, X):
      """
      The predict probability function
      
      Parameters
      ----------
      X : the feature matrix
      
      Returns
      ----------
      The probability (sigmoid or softmax) matrix
      """
      
      # Get the augmented feature matrix [1, X]
      IX = np.hstack((np.ones((X.shape[0], 1)), X))
          
      # Get the net_input matrix
      N = self.net_input(IX)

      return self.activation(N)
  
  def predict(self, X):
      """
      The predict class function
      
      Parameters
      ----------
      X : the feature matrix
      
      Returns
      ----------
      The predicted class vector
      """
      
      # If binary classification
      if self.n_classes == 2:
        return (self.predict_proba(X) >= 0.5) * 1         
      # If multi-class classification
      else:
        return np.argmax(self.predict_proba(X), axis=1)
          
#%%
# ### Multiple-layer perceptron
class MultiLayerPerceptron_MBGD(BaseEstimator, RegressorMixin):
  """Multi-layer perceptron implemented using mini-batch gradient descent and regularization (lasso, ridge and elastic net)"""
      
  def __init__(self, 
              hidden_layer_sizes=[100], 
              activation='relu', 
              batch_size=32,
              learning_rate_init=0.01, 
              max_iter=100, 
              shuffle=True, 
              penalty='l2',
              alpha=1, 
              gamma=0.5,
              random_state=42):
    
    # The number of perceptrons on each hidden layer
    self.hidden_layer_sizes = hidden_layer_sizes
    
    # The Activation function
    self.activation = activation
    
    # The size of minibatches for stochastic optimizers
    self.batch_size = batch_size
    
    # The initial learning rate
    self.learning_rate_init = learning_rate_init

    # The maximum number of epochs
    self.max_iter = max_iter
    
    # Whether to shuffle samples in each epoch
    self.shuffle = shuffle
    
    # The regularization term
    self.penalty=penalty
    
    # The regularization parameter
    self.alpha=alpha

    # The elastic net mixing parameter
    self.gamma=gamma
    
    # The random state
    self.random_state = random_state

  def fit(self, X, y):
    """
    The fit function
    
    Parameters
    ----------
    X : the feature matrix
    y : the target vector
    """
    
    # Get the one-hot-encoded target matrix
    Y = pd.get_dummies(y).values
    
    # Initialize the object variables
    self.fit_init(X, Y)
            
    # For each epoch
    for epoch in range(self.max_iter):
      # Get the indices of the training data
      idxs = np.array(range(X.shape[0]))
      
      # Get the minibatches of the training data
      mbs = self.get_mbes(idxs)
      
      # For each minibatch
      for mb in mbs:   
        # Get the feature matrix
        X_mb = X[mb,:]
                        
        # Get the target matrix
        Y_mb = Y[mb,:]
                        
        # Update the weights and biases using mini-batch gradient descent
        self.mini_batch_gradient_descent(X_mb.reshape(self.batch_size, -1), Y_mb.reshape(self.batch_size, -1))
        
        # Update the cost
        self.costs[epoch] += np.sum((Y_mb.reshape(self.batch_size, -1) - self.activations[-1]) ** 2) / self.m
              
  def fit_init(self, X, Y):
    """
    Initialize the object variables
    
    Parameters
    ----------
    X : the feature matrix
    y : the target matrix
    """
    
    # Initialize the number of samples and featurs
    self.m, self.n = X.shape
    
    # Initialize the number of unique class labels
    self.classes = np.unique(Y)
    
    # Initialize the number of perceptrons on each layer
    self.layer_sizes = [self.n] + self.hidden_layer_sizes + [len(self.classes)]
    
    # Initialize the cost
    self.costs = np.zeros(self.max_iter)
    
    # Initialize the random number generator
    self.rgen = np.random.RandomState(seed=self.random_state)
    
    # Initialize the weights
    self.W = [0] + [self.rgen.normal(loc=0.0, 
                                      scale=2 / np.sqrt( self.layer_sizes[i - 1] + self.layer_sizes[i]), 
                                      size=(self.layer_sizes[i - 1], self.layer_sizes[i]))
                    for i in range(1, len(self.layer_sizes))]
    
    # Initialize the biases
    self.b = [0] + [np.zeros((1, self.layer_sizes[i]))
                    for i in range(1, len(self.layer_sizes))]
    
    # Initialize the net inputs
    self.net_inputs = [0] * (len(self.layer_sizes))

    # Initialize the activations
    self.activations = [0] * (len(self.layer_sizes))
    
    # Initialize the sensitivities
    self.sensitivities = [0] * (len(self.layer_sizes))
    
    # Initialize the derivatives
    self.derivatives = [0] * (len(self.layer_sizes))
      
  def get_mbes(self, idxs):
    """
    Get the minibatches
    
    Parameters
    ----------
    idxs : The indices of the data
    
    Returns
    ----------
    The minibatches
    """
    
    # Initialize the minibatches
    mbs = []
    
    if self.shuffle is True:
      # Shuffle the indices
      self.rgen.shuffle(idxs)
            
    # Get the number of minibatches
    n_batch = len(idxs) // self.batch_size
    
    # For each minibatch
    for i in range(n_batch):
      # Get the first and last index (exclusive) of the minibatch
      first_idx = i * self.batch_size
      last_idx = min((i + 1) * self.batch_size, len(idxs))
                              
      # Get the minibatch
      mb = idxs[first_idx : last_idx]
      
      # Update the minibatches
      mbs.append(mb)

    return mbs
              
  def mini_batch_gradient_descent(self, X, Y):
    """
    Update the weights and biases using mini-batch gradient descent
    
    Parameters
    ----------
    X : the feature matrix
    Y : the target matrix
    """
    
    # Get the activation in the first layer
    self.activations[0] = X

    # Propagate the net input and activation forward through the network
    for i in range(1, len(self.layer_sizes)):
      # Get the net input on layer i
      self.net_inputs[i] = self.get_net_input(i)  
      
      # Get the activation on layer i
      self.activations[i] = self.get_activation(i)
                            
    # Get the sensitivity in the last layer
    self.sensitivities[-1] = - 2 / X.shape[0] * np.array([np.matmul((Y - self.activations[-1])[k, :],
                                                                    self.get_derivative(len(self.layer_sizes) - 1)[k, :, :]) 
                                                          for k in range(X.shape[0])])
                    
    # Propagate the sensitivites backward through the network
    for i in range(len(self.layer_sizes) - 2, 0, -1):
      # Get the derivative on layer i
      self.derivatives[i] = self.get_derivative(i)
                  
      # Get the sensitivity on layer i
      self.sensitivities[i] = self.get_sensitivity(i)
                    
    # Update the weights and biases using gradient descent
    for i in range(1, len(self.layer_sizes)):
      # Update the biases
      self.b[i] -= self.learning_rate_init * self.sensitivities[i].sum(axis=0).reshape(1, -1)
      
      # Update the weights
      self.W[i] -= self.learning_rate_init * (np.matmul(self.activations[i - 1].T, self.sensitivities[i]))
                                              
      # If lasso
      if self.penalty == 'l1':
        self.W[i] -= self.learning_rate_init * self.alpha * np.sign(self.W[i])                        
      # If ridge
      elif self.penalty == 'l2':
        self.W[i] -= self.learning_rate_init * self.alpha * self.W[i]                                              
      # If elastic net
      elif self.penalty == 'elasticnet':
        self.W[i] -= self.learning_rate_init * self.alpha * (self.gamma * np.sign(self.W[i]) + (1 - self.gamma) * self.W[i])                                              
          
  def get_net_input(self, i):
    """
    Get the net input on layer i
    
    Parameters
    ----------
    i : the ith layer
    
    Returns
    ----------
    The net input on layer i
    """
    
    return self.b[i] + np.matmul(self.activations[i - 1], self.W[i]) 

  def get_activation(self, i):
    """
    Get the activation on layer i
    
    Parameters
    ----------
    i : the ith layer
    
    Returns
    ----------
    The activation on layer i    
    """ 

    if self.activation == 'identity':
      return self.net_inputs[i]
    elif self.activation == 'logistic':
      return 1 / (1 + np.exp(-self.net_inputs[i]))
    elif self.activation == 'tanh':
      e_z = np.exp(self.net_inputs[i])
      e_neg_z = np.exp(-self.net_inputs[i])
      return (e_z - e_neg_z) / (e_z + e_neg_z)
    elif self.activation == 'relu':
      return np.clip(self.net_inputs[i], 0, None)
    else:
      print("Activation undefined!")
      sys.exit(1)
  
  def get_derivative(self, i):
    """
    Get the derivative on layer i
    
    Parameters
    ----------
    i : the ith layer
    
    Returns
    ----------
    The derivative on layer i    
    """ 
    
    if self.activation == 'identity':
      return np.array([np.identity(self.activations[i].shape[1]) 
                        for j in range(self.activations[i].shape[0])])
    elif self.activation == 'logistic':        
      return np.array([np.diag((self.activations[i] * 1 - self.activations[i])[j, :]) 
                        for j in range(self.activations[i].shape[0])])
    elif self.activation == 'tanh':
      return np.array([np.diag((1 - self.activations[i] ** 2)[j, :]) 
                        for j in range(self.activations[i].shape[0])])
    elif self.activation == 'relu':         
      return np.array([np.diag(np.where(self.net_inputs[i][j, :] >= 0, 1, 0).reshape(-1)) 
                        for j in range(self.net_inputs[i].shape[0])])
    else:
      print("Activation undefined!")
      sys.exit(1)
      
  def get_sensitivity(self, i):
    """
    Get the sensitivity on layer i
    
    Parameters
    ----------
    i : the ith layer
    
    Returns
    ----------
    The sensitivity on layer i    
    """ 
    
    # Get matrix multiplication
    M = np.matmul(self.sensitivities[i + 1], self.W[i + 1].T)
    
    return np.array([np.matmul(M[k, :], self.derivatives[i][k, :, :]) 
                      for k in range(M.shape[0])])
      
  def predict(self, X):
    """
    The predict function
    
    Parameters
    ----------
    X : the feature matrix
    
    Returns
    ----------
    The predicted class labels of the target
    """

    # Initialize the net inputs
    self.net_inputs = [0] * (len(self.layer_sizes))
    
    # Initialize the activations
    self.activations = [0] * (len(self.layer_sizes))
    # Initialize the activation in the first layer
    self.activations[0] = X

    # Propagate the input forward through the network
    for i in range(1, len(self.layer_sizes)):
      # Get the net input on layer i
      self.net_inputs[i] = self.get_net_input(i)  
      
      # Get the activation on layer i
      self.activations[i] = self.get_activation(i)
                            
    return np.argmax(self.activations[-1], axis=1)
      

#%%


class Dense:

  """
    A fully connected (Dense) layer in a neural network, commonly used in feedforward neural networks.

    Attributes:
    -----------
    name : str
        The name of the class for identification.
    n_neurons : int
        Number of neurons in the layer.
    input_dim : int or None
        Number of input features to the layer. Required for the first layer in a network.
    activation : str
        Activation function to apply to the layer's output. Supported options are 'linear', 'sigmoid', 'tanh', and 'softmax'.
    trainable : bool
        Whether the layer parameters (weights and biases) are trainable.
    weights : numpy.ndarray
        The weights matrix initialized based on the activation function specified.
    biases : numpy.ndarray
        The biases vector, initialized to zeros.

    Methods:
    --------
    info():
        Prints the weights and biases of the layer.

    layer():
        Returns the current instance of the Dense layer.

    get_params():
        Returns the current weights and biases of the layer as a tuple.

    set_params(weights, biases):
        Sets the weights and biases of the layer to the provided values.

    Parameters:
    -----------
    n_neurons : int
        The number of neurons in the layer.
    input_dim : int, optional
        The number of input features. Must be provided for the first layer in the network.
    activation : str, default 'linear'
        The activation function for the layer. Options include 'linear', 'sigmoid', 'tanh', and 'softmax'.
    trainable : bool, default True
        Determines whether the weights and biases of the layer should be updated during training.


    Examples:
    ---------
    >>> dense_layer = Dense(n_neurons=64, input_dim=128, activation='relu', trainable=True)
    >>> dense_layer.info()
    Weights: <weights matrix>

      Biases: <biases vector>
    >>> dense_layer.set_params(weights=new_weights, biases=new_biases)
    >>> weights, biases = dense_layer.get_params()
    """

  name = 'optilearn.nn.Dense'

  def __init__(self,n_neurons,input_dim=None,activation='linear',trainable=True):
    import numpy as np
    #if input_dim is not None:
    self.n_neurons=n_neurons
    self.input_dim=input_dim
    self.activation=activation
    #self.weights = None
    #self.biases = None
    if trainable in(True,False):
      self.trainable=trainable
    else:
      raise ValueError(f"The value of trainable parameter cane be ether True or False. Recived value is {trainable}")

    if input_dim is not None:
      if self.activation in('sigmoid','tanh','softmax'):
        #self.weights=np.random.randn(input_dim,n_neurons)
        self.weights=np.random.uniform(low=-0.1,high=0.1,size=(input_dim,n_neurons))
        #self.weights=np.ones((input_dim,n_neurons))
        #self.biases=np.random.randn(n_neurons)
        self.biases=np.zeros((n_neurons))
      else:
        shape=(input_dim,n_neurons)
        self.weights=np.random.normal(loc=0.0, scale=np.sqrt(2 / shape[0]), size=shape)
        self.biases=np.zeros((n_neurons))

    else:
      pass

  def info(self):
    print(f"Weights: {self.weights}\n\n  Biases: {self.biases}")

  def layer(self):
    return self

  def get_params(self):
    return self.weights,self.biases

  def set_params(self,weights,biases):
    self.weights=weights
    self.biases=biases


class Sequential:

  """
    A class representing a sequential neural network model.

    This class allows you to build and train a feedforward neural network by adding layers in a 
    linear stack. Each layer's output is the input to the next, forming a chain of transformations 
    from input to output. The network supports various types of layers like Dense, Dropout, 
    and custom layers. Additionally, it provides methods for compiling, training, and saving the model.

    Attributes:
    -----------
        * layers (list): A list of layers in the network, ordered sequentially.

        * weights (list): A list of weights for each layer.

        * biases (list): A list of biases for each layer.

        * activation (list): A list of activation functions used in each layer.

        * dropout (list): A list of dropout rates for each layer.

        * loss (str): The loss function used for training the model.

        * optimizer (str): The optimization algorithm used for training.

        * learning_rate (float): The learning rate used for optimization.

        * decay (float): The decay rate used for adjusting learning rate.

        * beta1 (float): The first moment estimate for optimizers like Adam.

        * beta2 (float): The second moment estimate for optimizers like Adam.

        * epsilon (float): A small value to prevent division by zero in optimization.

        

    Methods:
        ** add_layer(layer): Adds a new layer to the network.

        ** compile(loss, optimizer, learning_rate=0.01, decay=0.9, beta1=0.9, beta2=0.999, epsilon=1e-7):
            Compiles the model by setting loss, optimizer, and training parameters.

        ** fit(x_label, y_label, validation_data=None, epochs=10, batch_size=None, callbacks=None, 
            verbose=0, clipping=False, clipvalue=5, custome_grediant=None):
            Trains the model on the provided data.

        ** predict(data, output_from_all_layers=False):
            Makes predictions on the input data.

        ** save(file_name, saving_status=True):
            Saves the model's weights, biases, activations, and dropout rates to a file.

        ** load(file_name):
            Loads the model's parameters from a saved file.

        ** evaluate(data, y_label):
            Evaluates the model's performance based on the specified loss function and metric.

        ** summary():
            Prints a summary of the model, including layer details and parameter counts.


    Example:
        # Create a sequential model
        model = Sequential()
        
        # Add layers
        model.add_layer(Dense(units=64, input_dim=32, activation='relu'))
        model.add_layer(Dropout(0.5))
        model.add_layer(Dense(units=10, activation='softmax'))
        
        # Compile the model
        model.compile(loss='categorical_crossentropy', optimizer='adam')
        
        # Train the model
        model.fit(X_train, y_train, epochs=10, batch_size=32)
        
        # Evaluate the model
        accuracy = model.evaluate(X_test, y_test)
        print("Test Accuracy:", accuracy)
        
        # Save the model
        model.save('model.h5')
    """

  name = 'optilearn.nn.Sequential'

  def __init__(self):
    import numpy as np
    self.layers=[]
    self.weights=[]
    self.biases=[]
    self.activation=[]
    self.dropout=[]
    self.n_nurones=[1]
    self.input_dim=[]
    self.__drop=[]
    self.__best_weights = None
    self.__best_biases = None
    self.__learnable_layers = None
    self.__trainable_weights = None
    self.__trainable_biases = None
    self.__trainable_index = None

    # compile related attributes
    self.loss=None
    self.optimizer=None
    self.learning_rate=None
    self.metrics=None
    self.decay=None
    self.beta1=None
    self.beta2=None
    self.epsilon=None
    self.history={'epochs':[],'accuracy':[],'val_accuracy':[],'loss':[],'val_loss':[]}
    self.look_ahead_w=None
    self.look_ahead_b=None
  def add(self,layers):
    import numpy as np
    if type(layers) == Dense:
      try:
        self.n_nurones.append(layers.n_neurons)
        self.input_dim.append(layers.input_dim)
      except:
        pass
      try:
        #if layers.weights != None:
        self.weights.append(layers.weights)
        #if layers.biases != None:
        self.biases.append(layers.biases)
      except:
        #print('weights and biases not found')
        pass
      try:
        self.activation.append(layers.activation)
      except:
        pass
      #self.layers.append(layers)
      #print()

      # Adding the first layer input dim the first of the self.n_nurones list
      self.n_nurones.pop(0)
      self.n_nurones.insert(0,self.input_dim[0])
      #print(self.n_nurones)
      #print(self.input_dim)
      #print(self.weights)
      #print(self.biases)
      #print(self.activation)
      #print(self.layers)
      #if isinstance(self.layers,Dropout):                   # Drop out adding

      if len(self.n_nurones)>2:
        if self.activation[-1] in ('sigmoid','tanh','softmax'):
          #print(self.activation)
          self.weights.append(np.random.uniform(low=-0.1,high=0.1,size=(self.n_nurones[-2],self.n_nurones[-1])))
          self.biases.append(np.zeros(self.n_nurones[-1]))
        else:
          shape=(self.n_nurones[-2],self.n_nurones[-1])
          self.weights.append(np.random.normal(loc=0.0, scale=np.sqrt(2 / shape[0]), size=shape))
          self.biases.append(np.zeros(self.n_nurones[-1]))
    elif type(layers) in(Dense,Dropout):
      #drop=[]
      try:
        self.__drop.append(layers.dropout_rate)
      except:
        self.__drop.append(0.0)
      #if len(self.__drop)==len(self.layers):
        #for d in self.__drop:
          #if d == 0.0:
            #self.dropout.append(d)
          #else:
            #self.dropout.pop(-1)
            #self.dropout.append(d)
    self.layers.append(layers)




  def get_params(self):
    params=[]
    for i,j in zip(self.weights,self.biases):
      params.append(i)
      params.append(j)
    #return self.weights,self.biases,self.activation
    return params
  def set_params(self,parameters):
    weights=list([w for w in parameters[0::2]])
    biases=list([b for b in parameters[1::2]])
    self.weights=weights
    self.biases=biases


  def forword(self,input,return_all_outputs=False):
    import numpy as np
    def activation(x,name):
      def relu(x):
        return np.maximum(0, x)
      def sigmoid(x):
        return 1/(1+np.exp(-x))
      def softmax(x):
        exp_x = np.exp(x - np.max(x))  # Prevent overflow
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
      def tanh(x):
        return np.tanh(x)
      def licky_relu(x):
        y=0.01*x
        return np.maximum(y,x)
      if name =='sigmoid':
        return sigmoid(x)
      elif name =='relu':
        return relu(x)
      elif name =='softmax':
        return softmax(x)
      elif name =='licky_relu':
        return licky_relu(x)
      elif name =='tanh':
        return tanh(x)
      elif name == 'linear':
        return x
      else:
        raise ValueError(f"activation function named '{name}' not found in the pridefine functions of 'Sequential()'")

    w=self.weights
    b=self.biases
    a=self.activation
    input_array=input
    without_activation_output=[]
    with_activation=[]
    for i in range(len(w)):
      aa=np.dot(input_array,w[i])+b[i]
      without_activation_output.append(aa)
      with_activation.append(activation(aa,a[i]))
      input_array=activation(aa,a[i])
    if return_all_outputs == False:
      return input_array.flatten()
    elif return_all_outputs ==True:
      return dict({'Final_output':input_array.flatten(),'All_layers_outputs':with_activation})


  def compile(self,loss,optimizer,learning_rate=0.01,decay=0.9,beta1=0.9,beta2=0.999,epsilon=1e-7):  #metrics attribute was here
    e=[]
    for i in self.layers:
      try:
        e.append(i.dropout_rate)
      except:
        e.append(0.0)
    #d=[]
    for e1 in e:
      if e1 == 0.0:
        self.dropout.append(e1)
      else:
        self.dropout.pop(-1)
        self.dropout.append(e1)

    self.__eval_dropout=list(map(lambda x: 1-x,self.dropout))
    self.loss=loss
    self.optimizer=optimizer
    self.learning_rate=learning_rate
    self.decay=decay
    self.beta1=beta1
    self.beta2=beta2
    self.epsilon=epsilon

    self.__learnable_layers = list([i for i in self.layers if i.name == 'optilearn.nn.Dense'])
    self.__trainable_weights = list([self.weights[i] for i in range(len(self.__learnable_layers)) if self.__learnable_layers[i].trainable == True])
    self.__trainable_biases = list([self.biases[i] for i in range(len(self.__learnable_layers)) if self.__learnable_layers[i].trainable == True])
    self.__trainable_index = list([i for i in range(len(self.__learnable_layers)) if self.__learnable_layers[i].trainable == True])

    '''if metrics != None:
      if isinstance(metrics,list):
        self.metrics=metrics
      else:
        raise TypeError(f"'metrics' must be a list object but given type is '{type(metrics)}'")'''

  def fit(self,x_label,y_label,validation_data=None,epochs=10,batch_size=None,callbacks=None,verbose=0,clipping=False,clipvalue=5,custome_grediant=None):
    self.__clipvalue=clipvalue
    #def forward(input,weights,biases,activations,return_all_outputs=True):
    import numpy as np
    from sklearn.metrics import accuracy_score,mean_squared_error,mean_absolute_error,r2_score
    def activation(x,name):
      def relu(x):
        return np.maximum(0, x)
      def sigmoid(x):
        return 1/(1+np.exp(-x))
      def softmax(output):
         #For numerical stability, subtract the maximum value from logits
        #print("Output Type:", type(output))
        exp_logits = np.exp(output - np.max(output, axis=1, keepdims=True))
        return exp_logits / np.sum(exp_logits, axis=1, keepdims=True)

      '''def softmax(output):
        # Ensure output is a NumPy array
        output = np.asarray(output)

        # For numerical stability, subtract the maximum value from logits
        exp_logits = np.exp(output - np.max(output, axis=1, keepdims=True))
        return exp_logits / np.sum(exp_logits, axis=1, keepdims=True)'''

      '''def softmax(output):
        """
        Applies softmax activation function.

        Args:
            output: NumPy array or a list.

        Returns:
            Softmax-activated output.
        """
        # Convert output to NumPy array with float dtype
        output = np.asarray(output, dtype=np.float64)

        # For numerical stability, subtract the maximum value from logits
        exp_logits = np.exp(output - np.max(output, axis=1, keepdims=True))
        return exp_logits / np.sum(exp_logits, axis=1, keepdims=True)'''
      def softmax1(x):
       # Prevent overflow
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
      def tanh(x):
        return np.tanh(x)
      def licky_relu(x):
        y=0.01*x
        return np.maximum(y,x)
      if name =='sigmoid':
        return sigmoid(x)
      elif name =='relu':
        return relu(x)
      elif name =='softmax':
        return softmax(x)

      elif name =='licky_relu':
        return licky_relu(x)
      elif name =='tanh':
        return tanh(x)
      elif name == 'linear':
        return x
      else:
        raise ValueError(f"activation function named '{name}' not found in the pridefine functions of 'Sequential()'")

      '''w=weights
      b=biases
      a=activations
      input_array=input
      without_activation_output=[]
      with_activation=[]
      for i in range(len(w)):
        aa=np.dot(input_array,w[i])+b[i]
        without_activation_output.append(aa)
        with_activation.append(activation(aa,a[i]))
        input_array=activation(aa,a[i])
      if return_all_outputs == False:
        return input_array.flatten()
      elif return_all_outputs ==True:
        return dict({'Final_output':input_array.flatten(),'All_layers_outputs':with_activation})'''

    '''def derivative_activation(output,name):
      def relu_d(output):
        return np.where(output>0,1,0)
      def sigmoid_d(output):
        #print("Output type:", type(output))
        #print("Output values:", output)
        return output * (1 - output)

      def softmax_d(softmax_output):
        # Ensure softmax_output is 2D (n_samples, n_classes)
        if softmax_output.ndim == 1:
          softmax_output = softmax_output[np.newaxis, :]  # Convert to 2D

        n_classes = softmax_output.shape[1]
        n_samples = softmax_output.shape[0]

        # Initialize an array for derivatives
        derivative = np.empty((n_samples, n_classes))

        for i in range(n_samples):
          s = softmax_output[i]
          # Derivative of softmax for the i-th sample
          derivative[i] = s * (1 - s)  # Using softmax outputs directly

        return derivative

      def tanh_d(output):
        return 1-output**2
      def licky_relu_d(output):
        return np.where(output>0,1,0.01)
      def linear_d(output):
        return output
      if name =='relu':
        return relu_d(output)
      elif name =='sigmoid':
        return sigmoid_d(output)
      elif name == 'softmax':
        return softmax_d(output)
      elif name =='tanh':
        return tanh_d(output)
      elif name == 'licky_relu':
        return licky_relu_d(output)
      elif name == 'linear':
        return linear_d(output)'''

    def loss(y_true,y_pred,name):
      def binary_cross_entropy(y_true, y_pred):
        # Clip predictions to avoid log(0)
        epsilon = 1e-15
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
      def categorical_cross_entropy(y_true,y_pred,loss_type='mean',epsilon=1e-10):
        if type(y_true) != np.ndarray:
          y_true=y_true.to_numpy().reshape(-1,1)
        y_true = y_true.astype(int)
        n_classes = int(np.max(y_true) + 1)
        y_one_hot = np.eye(n_classes)[y_true.reshape(-1)]

        y_pred=np.clip(y_pred,epsilon,1-epsilon)

        cce=-y_one_hot*np.log(y_pred)
        loss=cce[cce!=0]
        if loss_type == 'mean':
          return np.mean(loss)
        elif loss_type == 'total':
          return np.sum(loss)
        elif loss_type == 'max':
          return np.max(loss)
        elif loss_type == 'min':
          return np.min(loss)
        else:
          raise ValueError(f"loss_type  '{loss_type}' not a valid loss_type of categorical_crossentropy")
      def mse(y_true, y_pred):
        return np.mean((y_true - y_pred) ** 2)
      def mae(y_true, y_pred):
        return np.mean(np.abs(y_true - y_pred))
      if name in('binary_cross_entropy','binary_crossentropy'):
        return binary_cross_entropy(y_true,y_pred)
      elif name in('categorical_cross_entropy','categorical_crossentropy'):
        return categorical_cross_entropy(y_true,y_pred)
      elif name == 'mse':
        return mse(y_true,y_pred)
      elif name == 'mae':
        return mae(y_true,y_pred)
      else:
        raise ValueError(f"loss '{name}' is not a valid loss type")

    '''def derivative_loss(y_true,y_pred,loss_name):
      def BCE_d(y_true,y_pred):
        epsilon = 1e-15
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        return (y_pred - y_true) / (y_pred * (1 - y_pred))
      #def cce_d(y_true,y_pred,epsilon=1e-10):
        #if type(y_true) != np.ndarray:
          #y_true=y_true.to_numpy().reshape(-1,1)
        #y_true = y_true.astype(int)
        #n_classes = int(np.max(y_true) + 1)
        #y_one_hot = np.eye(n_classes)[y_true.reshape(-1)]

        #y_pred=np.clip(y_pred,epsilon,1-epsilon)

        #derivative = -y_one_hot / y_pred
        #return derivative[derivative!=0].reshape(-1,1)
      def cce_d(y_true,y_pred):
        yy=y_true
        classes=np.max(yy)+1
        yy=yy.astype(int)
        #print('a')
        y_one_hot=np.eye(int(classes))[yy.reshape(-1)]
        #print('b')
        one_hot=y_one_hot.astype(int)
        #print('c')
        y_pred=np.clip(y_pred,1e-15,1-1e-15)
        #print('d')
        return -one_hot/y_pred

      def MSE_d(y_true, y_pred):
        return (-2 * (y_true - y_pred)) / y_true.shape[0]
      def MAE_d(y_true,y_pred):
        return np.where(y_pred < y_true, -1 / y_true.size, np.where(y_pred > y_true, 1 / y_true.size, 0))
      if loss_name in('binary_cross_entropy','binary_crossentropy'):
        return BCE_d(y_true,y_pred)
      elif loss_name in('categorical_cross_entropy','categorical_crossentropy'):
        return cce_d(y_true,y_pred)
      elif loss_name == 'mse':
        return MSE_d(y_true,y_pred)
      elif loss_name == 'mae':
        return MAE_d(y_true,y_pred)
      else:
        raise ValueError(f"loss '{loss_name}' is not a valid loss type")'''

    # Function to calculate different loss values
    def calculate_loss(y_true, y_pred, loss='categorical_crossentropy'):
      if loss == 'categorical_crossentropy':
        # Add a small value to avoid log(0)
        return -np.sum(y_true * np.log(y_pred + 1e-8), axis=1)
      elif loss == 'binary_crossentropy':
        return -np.mean(y_true * np.log(y_pred + 1e-8) + (1 - y_true) * np.log(1 - y_pred + 1e-8))
      elif loss == 'mse':
        return np.mean((y_true - y_pred) ** 2)
      elif loss == 'mae':
        return np.mean(np.abs(y_true - y_pred))
      else:
        raise ValueError(f"Unsupported loss function: {loss}")

      # Function to calculate the gradients with activation derivatives
    def compute_gradients_with_activations2(y_true, y_pred, outputs, weights, biases, activations, input_data, loss='categorical_crossentropy'):
      # Number of layers
      num_layers = len(weights)

      # Initialize gradient lists for weights and biases
      dW = [None] * num_layers
      db = [None] * num_layers

      # Gradient of loss with respect to y_pred (output layer)
      if loss == 'categorical_crossentropy':
        delta = y_pred - y_true  # For softmax + categorical cross-entropy
      elif loss == 'binary_crossentropy':
        delta = (y_pred - y_true)  # Simpler for binary cross-entropy when using sigmoid activation
      elif loss == 'mse':
        delta = -2 * (y_true - y_pred)  # MSE derivative
      elif loss == 'mae':
        delta = np.sign(y_pred - y_true)  # MAE derivative
      else:
        raise ValueError(f"Unsupported loss function: {loss}")

      # Backpropagate through each layer in reverse order
      for i in reversed(range(num_layers)):
        if i > 0:
            a_prev = outputs[i - 1]  # Activations from the previous layer
        else:
            a_prev = input_data  # For the first layer, use the input data

        # Compute gradients for the weights and biases
        dW[i] = np.dot(a_prev.T, delta)  # Gradient wrt weights
        db[i] = np.sum(delta, axis=0, keepdims=True)  # Gradient wrt biases

        # If not the first layer, compute the gradient wrt the previous layer's activation
        if i > 0:
            delta = np.dot(delta, weights[i].T) * derivative_activation(outputs[i - 1], activations[i - 1])

      return dW, db

    # Derivative of various activation functions
    def derivative_activation(Z, activation):
      if activation == 'relu':
        return np.where(Z > 0, 1, 0)
      elif activation == 'leaky_relu':
        return np.where(Z > 0, 1, 0.01)  # Leaky ReLU with alpha = 0.01
      elif activation == 'sigmoid':
        return Z * (1 - Z)  # Sigmoid derivative
      elif activation == 'tanh':
        return 1 - Z ** 2  # Tanh derivative
      elif activation == 'linear':
        return np.ones_like(Z)  # Derivative of linear is 1
      elif activation == 'softmax':
        # For softmax, we already used y_pred - y_true, no need for further activation derivative
        return Z
      return Z

    def EWMA(current_gradients,previous_velosity,beta=0.9):
      if previous_velosity == None:
        previous_velosity=list([np.zeros_like(g) for g in current_gradients])
      vt=list(map(lambda x,y: beta*x +(1-beta)*y,previous_velosity,current_gradients))
      return vt

    def optimizers(name,train_data_x,train_data_y,current_batch_size,old_weights,old_biases,weights_gradients,biases_gradients,wvt1,bvt1,wvt2,bvt2,wst1,bst1,learning_rate,beta1,beta2,decay,epsilon,time_stamp,t_value):
      weights_new=[]
      biases_new=[]
      if name == 'sgd':
        for i in range(len(weights_gradients)):

          weights_new.append(old_weights[i]-(1/current_batch_size)*(learning_rate*weights_gradients[i]))
          biases_new.append(old_biases[i]-(1/current_batch_size)*(learning_rate*biases_gradients[i]))
        return weights_new,biases_new,None,None,None,None,None,None

      elif name == 'momentum':
        wst=None
        bst=None
        if decay == None:
          decay=0.9
        if time_stamp==0:
          wvt=EWMA(weights_gradients,None,decay)
          bvt=EWMA(biases_gradients,None,decay)
          wvt1=wvt
          wbt1=bvt
        else:
          wvt=EWMA(weights_gradients,wvt1,decay)
          bvt=EWMA(biases_gradients,bvt1,decay)
          #wvt1=wvt
          #bvt1=bvt
        for i in range(len(weights_gradients)):
          weights_new.append(old_weights[i]-(1/current_batch_size)*(wvt[i]+learning_rate*weights_gradients[i]))
          biases_new.append(old_biases[i]-(1/current_batch_size)*(bvt[i]+learning_rate*biases_gradients[i]))
        return weights_new,biases_new,wvt,bvt,None,None,None,None

        '''elif name == 'nag':
        weights=self.weights
        biases=self.biases

        #wvt=None
        #bvt=None
        if decay == None:
          decay=0.9
        if time_stamp == 0:
          wvt=EWMA(weights_gradients,None,decay)
          bvt=EWMA(biases_gradients,None,decay)
        else:
          wvt=EWMA(weights_gradients,wvt1,decay)
          bvt=EWMA(biases_gradients,bvt1,decay)

        look_ahead_weights=list(map(lambda x,y: x-(decay*y),weights,wvt))
        look_ahead_biases=list(map(lambda x,y: x-(decay*y),biases,bvt))

        pre,all=forward(train_data_x,look_ahead_weights,look_ahead_biases,self.activation)
        if self.loss in('categorical_crossentropy','categorical_cross_entropy'):
          dw,db=compute_gradients_with_activations2(OneHotEncode(train_data_y),pre,all,look_ahead_weights,look_ahead_biases,self.activation,train_data_x,self.loss)
        else:
          dw,db=compute_gradients_with_activations2(train_data_y,pre,all,look_ahead_weights,look_ahead_biases,self.activation,train_data_x,self.loss)
        #print(dw)
        #print(db)
        if time_stamp == 0:
          wvt22=EWMA(dw,None,decay)
          bvt22=EWMA(db,None,decay)
        else:
          wvt22=EWMA(dw,wvt2,decay)
          bvt22=EWMA(db,bvt2,decay)

        vt_for_w = list(map(lambda x,y: (decay*x)+(learning_rate*y),wvt22,dw))
        vt_for_b = list(map(lambda x,y: (decay*x)+(learning_rate*y),bvt22,db))
        for i in range(len(weights_gradients)):
          #weights_new.append(old_weights[i]-(1/current_batch_size)*(decay*wvt2[i])+(learning_rate*dw[i]))
          #biases_new.append(old_biases[i]-(1/current_batch_size)*(decay*bvt2[i])+(learning_rate*db[i]))
          weights_new.append(old_weights[i]-((1/current_batch_size)*vt_for_w[i]))
          biases_new.append(old_biases[i]-((1/current_batch_size)*vt_for_b[i]))

        return weights_new,biases_new,wvt,bvt,wvt22,bvt22,None,None'''

      elif name == 'nag':
        decay = decay if decay != None else 0.9

        if time_stamp == 0:
          wvt_p = list([np.zeros_like(wg) for wg in weights_gradients])
          bvt_p = list([np.zeros_like(bg) for bg in biases_gradients])
        else:
          wvt_p=wvt1
          bvt_p=bvt1

        wvt = list([(decay*w_p) + (learning_rate*wg) for w_p,wg in zip(wvt_p,weights_gradients)])
        bvt = list([(decay*b_p) + (learning_rate*bg) for b_p,bg in zip(bvt_p,biases_gradients)])
        #print(wvt_p)
        #print(bvt_p)

        look_aheade_weights = list(map(lambda x,y: x - (decay*y),old_weights,wvt_p))
        look_ahead_biases = list(map(lambda x,y: x - (decay*y),old_biases,bvt_p))
        #print(look_aheade_weights)
        #print(look_ahead_biases)
        self.look_ahead_w=look_aheade_weights
        self.look_ahead_b=look_ahead_biases
        pre,all = forward(train_data_x,look_aheade_weights,look_ahead_biases,self.activation)
        #print(pre)
        if self.loss in('categorical_crossentropy','categorical_cross_entropy'):
          train_data_y = OneHotEncode(train_data_y)
        else:
          train_data_y = train_data_y

        dw,db = compute_gradients_with_activations2(train_data_y,pre,all,look_aheade_weights,look_ahead_biases,self.activation,train_data_x,self.loss)

        if time_stamp == 0:
          wvt22_p = list([np.zeros_like(lwg) for lwg in dw])
          bvt22_p = list([np.zeros_like(lbg) for lbg in db])
        else:
          wvt22_p = wvt2
          bvt22_p = bvt2

        wvt22 = list([(decay*w22_p) + (learning_rate*wgn) for w22_p,wgn in zip(wvt22_p,dw)])
        bvt22 = list([(decay*b22_p) + (learning_rate*bgn) for b22_p,bgn in zip(bvt22_p,db)])

        for i in range(len(old_weights)):
          weights_new.append(old_weights[i] - ((1/current_batch_size)*wvt22[i]))
          biases_new.append(old_biases[i] -((1/current_batch_size)*bvt22[i]))
        return weights_new,biases_new,wvt,bvt,wvt22,bvt22,None,None

      elif name  in('ada_grad','adagrad'):

        if decay == None:
          decay=0.9

        if time_stamp == 0:
          vt_w=list(map(lambda x: x**2,weights_gradients))
          vt_b=list(map(lambda x: x**2,biases_gradients))
        else:
          vt_w=list(map(lambda x,y: x+y**2,wvt1,weights_gradients))
          vt_b=list(map(lambda x,y: x+y**2,bvt1,biases_gradients))

        for i in range(len(weights_gradients)):
          weights_new.append(old_weights[i] - (1/current_batch_size)*((learning_rate/(np.sqrt(vt_w[i])+epsilon))*weights_gradients[i]))
          biases_new.append(old_biases[i] - (1/current_batch_size)*((learning_rate/(np.sqrt(vt_b[i])+epsilon))*biases_gradients[i]))
        return weights_new,biases_new,vt_w,vt_b,None,None,None,None

      elif name in('rmsprop','rms_prop'):

        if decay == None:
          decay=0.9
        if time_stamp == 0:
          wvt=EWMA(list(map(lambda x: x**2,weights_gradients)),None,decay)
          bvt=EWMA(list(map(lambda x: x**2,biases_gradients)),None,decay)
        else:
          wvt=EWMA(list(map(lambda x: x**2,weights_gradients)),wvt1,decay)
          bvt=EWMA(list(map(lambda x: x**2,biases_gradients)),bvt1,decay)

        for i in range(len(weights_gradients)):
          weights_new.append(old_weights[i] - (1/current_batch_size)*((learning_rate/(np.sqrt(wvt[i])+epsilon))*weights_gradients[i]))
          biases_new.append(old_biases[i] - (1/current_batch_size)*((learning_rate/(np.sqrt(bvt[i])+epsilon))*biases_gradients[i]))
        return weights_new,biases_new,wvt,bvt,None,None,None,None

      elif name == 'adam':
        #print(type(old_weights))
        #print(type(old_biases))
        if time_stamp == 0:
          vt_w=EWMA(weights_gradients,None,beta1)
          vt_b=EWMA(biases_gradients,None,beta1)

          st_w=EWMA(list(map(lambda x: x**2,weights_gradients)),None,beta2)
          st_b=EWMA(list(map(lambda x: x**2,biases_gradients)),None,beta2)

        else:
          vt_w=EWMA(weights_gradients,wvt1,beta1)
          vt_b=EWMA(biases_gradients,bvt1,beta1)

          st_w=EWMA(list(map(lambda x: x**2,weights_gradients)),wst1,beta2)
          st_b=EWMA(list(map(lambda x: x**2,biases_gradients)),bst1,beta2)

        vt_hat_w= list(map(lambda x: x/(1-beta1**t_value),vt_w))
        vt_hat_b= list(map(lambda x: x/(1-beta1**t_value),vt_b))

        st_hat_w= list(map(lambda x: x/(1-beta2**t_value),st_w))
        st_hat_b= list(map(lambda x: x/(1-beta2**t_value),st_b))

        for i in range(len(weights_gradients)):
          weights_new.append(old_weights[i] - (1/current_batch_size)*((learning_rate*(vt_hat_w[i]))/(np.sqrt(st_hat_w[i])+epsilon))) #*weights_gradients[i]
          biases_new.append(old_biases[i] - (1/current_batch_size)*((learning_rate*(vt_hat_b[i]))/(np.sqrt(st_hat_b[i])+epsilon)))  #*biases_gradients[i]
          #weights_new.append(
          #old_weights[i] - (1/current_batch_size)*(learning_rate * (vt_hat_w[i] / (np.sqrt(st_hat_w[i]) + epsilon)))
            #)

          #biases_new.append(
          #old_biases[i] - (1/current_batch_size)(learning_rate * (vt_hat_b[i] / (np.sqrt(st_hat_b[i]) + epsilon)))
            #)
        return weights_new,biases_new,vt_w,vt_b,None,None,st_w,st_b

    '''def drop_out(layer_output,drop_out_rate):
      arr=layer_output
      rate=drop_out_rate
      if isinstance(drop_out_rate,float):
        if drop_out_rate > 0.0:
          n_indexes_to_be_droped_out = (arr.shape[0]*(rate*100))/100
          count_in_round = round(n_indexes_to_be_droped_out)

          indexes = np.random.randint(arr.shape[0],size=(count_in_round))
          for i in indexes:
            arr[i]=0
          return arr
        elif drop_out_rate == 0.0:
          return layer_output
        else:
          raise ValueError(f"dropout value can't be a negative value")
      else:
        raise TypeError(f"dropout must be a float object")'''
    def drop_out(layer_output, drop_out_rate):
      """
      Applies dropout to the layer's output during training.

      Parameters:
      - layer_output: numpy array, output from a layer
      - drop_out_rate: float, probability of dropping out a unit (between 0 and 1)

      Returns:
      - Modified layer output after applying dropout.
      """
      if not isinstance(drop_out_rate, float):
        raise TypeError("Dropout rate must be a float.")

      if drop_out_rate < 0.0 or drop_out_rate >= 1.0:
        raise ValueError("Dropout rate must be between 0 and 1 (exclusive).")

      if drop_out_rate > 0.0:
        # Create a mask that randomly drops out neurons
        mask = np.random.binomial(1, 1 - drop_out_rate, size=layer_output.shape)
        # Apply the mask and scale the output
        return layer_output * mask / (1 - drop_out_rate)

      return layer_output  # If dropout rate is 0, return unchanged


    def OneHotEncode(y_true):
      import numpy as np

      if type(y_true) != np.ndarray:
        yy=y_true.astype(int).to_numpy().reshape(-1,1)
      else:
        yy=y_true.astype(int)
      classes=np.unique(yy)
      #classes=np.max(yy) + 1
      #print(classes)
      one_hot=np.eye(len(classes))[yy.reshape(-1)]
      #one_hot=np.eye(int(classes))[yy.reshape(-1)]
      return one_hot

    '''def forward(x_train,weights,biases,activations,dropout_rates):
      input=x_train
      all_outputs=[]
      for i in range(len(weights)):
        output=np.dot(input,weights[i])+biases[i]
        all_outputs.append(drop_out(activation(output,activations[i]),dropout_rates[i]))
        act=activation(output,activations[i])
        input=drop_out(act,dropout_rates[i])
      return input,all_outputs'''

    def forward(x_train, weights, biases, activations, dropout_rates):
      """
      Forward pass through the network with dropout applied to hidden layers.

      Parameters:
      - x_train: Input data (numpy array)
      - weights: List of weight matrices for each layer
      - biases: List of bias vectors for each layer
      - activations: List of activation functions (strings) for each layer
      - dropout_rates: List of dropout rates for each layer

      Returns:
      - Final output and all intermediate layer outputs.
      """
      input = x_train
      all_outputs = []

      for i in range(len(weights)):
        output = np.dot(input, weights[i]) + biases[i]
        activated_output = activation(output, activations[i])

        # Apply dropout to the output of this layer (except last layer)
        if i < len(weights) - 1:  # Usually we don't apply dropout to the output layer
            activated_output = drop_out(activated_output, dropout_rates[i])

        all_outputs.append(activated_output)
        input = activated_output

      return input, all_outputs

      '''def eval(x_test,weights,biases,activation,eval_dropouts):
      e_input=x_test
      e_all_outputs=[]
      for i in range(len(weights)):
        e_output=np.dot(e_input,weights[i])+biases[i]
        e_activated_output=activation(e_output,activation[i])
        e_all_outputs.append(e_activated_output*eval_dropouts[i])
        e_input=e_activated_output*eval_dropouts[i]
      return e_input,e_all_outputs'''
    def eval1(x_train,weights,biases,activations,eval_dropouts):
      import numpy as np
      input=x_train
      all_outputs=[]
      for i in range(len(weights)):
        output=np.dot(input,weights[i])+biases[i]
        all_outputs.append(activation(output,activations[i])*eval_dropouts[i])
        input=activation(output,activations[i])*eval_dropouts[i]
      #return tf.convert_to_tensor(input.astype('float32')),all_outputs
      return input,all_outputs
    def eval2(x_train,weights,biases,activations,eval_dropouts):
      import numpy as np
      input=x_train
      all_outputs=[]
      for i in range(len(weights)):
        output=(np.dot(input,weights[i])+biases[i])*eval_dropouts[i]
        all_outputs.append(activation(output,activations[i]))
        input=activation(output,activations[i])
      #return tf.convert_to_tensor(input.astype('float32')),all_outputs
      return input,all_outputs

    if batch_size == 0:
      l_loss=[]
      delta=[]
      gr=[]
      d_activation=[]
      all_o=[]
      all_o1=[]
      y_hats=[]
      for i in range(1,epochs+1):
        w=self.weights
        b=self.biases
        a=self.activation

        wr=list(reversed(self.weights))
        br=list(reversed(self.biases))
        ar=list(reversed(self.activation))

        wr1=list(reversed(self.weights))
        br1=list(reversed(self.biases))
        ar1=list(reversed(self.activation))

        y_pred,all_outputs=forward(x_label,w,b,a)
        #y_pred = np.clip(y_pred, 1e-8, 1 - 1e-8)
        yc=np.clip(y_pred, 1e-15, 1 - 1e-15)
        y_hats.append(yc)
        #epoch_and_output_of_al_layeer.append(all_outputs)
        #all_o.append(all_outputs)
        y_pred1=y_pred
        all_outputs1=list(reversed(all_outputs))
        all_o1.append(all_outputs1)
        last_layer_output_delta=0
        for e in range(len(wr)):
          if e == 0:
            y_clip=np.clip(y_pred,1e-15, 1 - 1e-15)
            current_batch_size=x_label.to_numpy().shape[0]
            output_loss=derivative_loss(y_label.to_numpy().reshape(-1,1),y_pred,self.loss)
            #l_loss.append(output_loss)
            output_delta=output_loss*derivative_activation(all_outputs1[e],ar[e])
            #output_delta= y_pred-y_label.to_numpy().reshape(-1,1)

            #d_activation.append(derivative_activation(all_outputs1[e],ar[e]))
            #d_acivation.append(derivative_activation(all_outputs1[e],ar[e]))
            #delta.append(output_delta)
            greadiant=(1./current_batch_size)*np.dot(all_outputs1[e+1].T,output_delta)
            greadiant = np.clip(greadiant, -1.0, 1.0)
            #gr.append(greadiant)    ######
            wr[e]-=self.learning_rate*greadiant
            br[e]-=self.learning_rate*np.sum(output_delta,axis=0)
            last_layer_output_delta=output_delta
          elif e >0 and e < len(wr)-1:
            current_batch_size=x_label.to_numpy().shape[0]
            output_loss=np.dot(last_layer_output_delta,wr1[e-1].T)
            #l_loss.append(output_loss)
            output_delta=output_loss * derivative_activation(all_outputs1[e],ar[e])
            #d_activation.append(derivative_activation(all_outputs1[e],ar[e]))
            #delta.append(output_delta)
            grediant=(1./current_batch_size)*np.dot(all_outputs1[e+1].T,output_delta)
            #gr.append(grediant)    ######
            wr[e]-=self.learning_rate*grediant
            br[e]-=self.learning_rate*np.sum(output_delta,axis=0)
            last_layer_output_delta=output_delta
          else:
            current_batch_size=x_label.to_numpy().shape[0]
            output_loss=np.dot(last_layer_output_delta,wr1[e-1].T)
            #l_loss.append(output_loss)
            output_delta=output_loss * derivative_activation(all_outputs1[e],ar[e])
            #d_activation.append(derivative_activation(all_outputs1[e],ar[e]))
            #delta.append(output_delta)
            grediant=(1./current_batch_size)*np.dot(x_label.to_numpy().T,output_delta)
            #gr.append(grediant)    ######
            wr[e]-=self.learning_rate*grediant
            br[e]-=self.learning_rate*np.sum(output_delta,axis=0)

        self.weights=list(reversed(wr))
        self.biases=list(reversed(br))
        y_pred_b = (y_pred >= 0.5).astype(int)
        print(f"Epoch: {i} accuracy : {accuracy_score(y_label.to_numpy().reshape(-1,1),y_pred_b)}")
      #return l_loss,delta,gr,d_activation,all_o,all_o1,y_hats

    elif batch_size != None or batch_size == None:
      import random
      batch_size = batch_size if batch_size != None else x_label.to_numpy().shape[0]
      if isinstance(batch_size,int):
        if type(x_label) != np.ndarray:
          batches_per_epoch=int(x_label.to_numpy().shape[0]/batch_size)
        else:
          batches_per_epoch=int(x_label.shape[0]/batch_size)
        #batches_per_epoch = int(np.ceil(len(x_label) / batch_size))
        #if isinstance(batches_per_epoch,float):
        if batches_per_epoch.as_integer_ratio()[1] !=1:
          batches_per_epoch+=1
          batches_per_epoch = int(batches_per_epoch)

        x_label1=x_label.to_numpy() if type(x_label) != np.ndarray else x_label                         #********
        y_label1=y_label.to_numpy().reshape(-1,1) if type(y_label) != np.ndarray else y_label           #********
        train_data=np.hstack((x_label1,y_label1))
        sub_sets=list(map(lambda x: train_data[x * batch_size : (x+1)*batch_size],list(range(batches_per_epoch))))
        gr=[]
        gr1=[]
        #random.shuffle(sub_sets)
        t_val=1
        for i in range(1,epochs+1):             # Epochs loops
          time_s=0
          random.shuffle(sub_sets)
          loss11=[]
          for j in sub_sets:
            w=self.weights
            b=self.biases
            a=self.activation

            wr=list(reversed(self.weights))
            br=list(reversed(self.biases))
            ar=list(reversed(self.activation))

            wr1=list(reversed(self.weights))
            br1=list(reversed(self.biases))
            ar1=list(reversed(self.activation))

            y_pred,all_outputs=forward(j[:,0:-1],w,b,a,self.dropout)    # Forward propagation
            #time_s+=1
            y_pred1=y_pred
            all_outputs1=list(reversed(all_outputs))
            loss11.append(loss(j[:,-1].reshape(-1,1),y_pred,self.loss))
            last_layer_output_delta=0
            train_x=j[:,0:-1]
            train_y=j[:,-1].reshape(-1,1)
            current_batch_size=j.shape[0]
            '''for e in range(len(wr)):
              if e ==0:
                current_batch_size=j.shape[0]
                if self.loss in('categorical_cross_entropy','categorical_crossentropy') and self.activation[-1] == 'softmax':
                  y_true=j[:,-1].reshape(-1,1)
                  y_true=y_true.astype(int)
                  if np.min(y_true) != 0:
                    y_true = y_true - np.min(y_true)
                  labels=np.max(y_true)+1
                  labels=int(labels)
                  y_one_hot1=np.eye(labels)[y_true.reshape(-1)]
                  #print(y_pred.shape)
                  #print(y_one_hot1.shape)
                  output_delta=y_pred-y_one_hot1
                  #print(output_delta)



                else:
                  output_loss=derivative_loss(j[:,-1].reshape(-1,1),y_pred,self.loss)
                  #print(output_loss)
                  #print(y_pred)
                  output_delta = output_loss * derivative_activation(all_outputs1[e],ar[e])
                greadiant=(1./current_batch_size)*np.dot(all_outputs1[e+1].T,output_delta)
                #gr.append(greadiant)
                if custome_grediant != None:
                  greadiant+= custome_grediant
                #greadiant=np.dot(all_outputs1[e+1].T,output_delta)
                if clipping == True:
                  greadiant=np.clip(greadiant, -self.__clipvalue, self.__clipvalue, out=greadiant)
                gr.append(greadiant)
                wr[e]-= self.learning_rate * greadiant
                br[e]-= self.learning_rate * np.sum(output_delta,axis=0)
                gr1.append(np.sum(output_delta,axis=0))
                last_layer_output_delta = output_delta
              elif e >0 and e < len(wr)-1:
                current_batch_size=j.shape[0]
                output_loss = np.dot(last_layer_output_delta,wr1[e-1].T)
                output_delta = output_loss * derivative_activation(all_outputs1[e],a[e])
                grediant =(1./current_batch_size)* np.dot(all_outputs1[e+1].T,output_delta)
                #grediant=(np.dot(all_outputs1[e+1].T,output_delta))/current_batch_size
                gr.append(grediant)
                if custome_grediant != None:
                  grediant+= custome_grediant
                #grediant =np.dot(all_outputs1[e+1].T,output_delta)
                if clipping == True:
                  grediant=np.clip(grediant, -self.__clipvalue, self.__clipvalue, out=grediant)
                #gr.append(grediant)
                wr[e]-= self.learning_rate * grediant
                br[e]-= self.learning_rate * np.sum(output_delta,axis=0)
                gr1.append(np.sum(output_delta,axis=0))
                last_layer_output_delta = output_delta
              else:
                current_batch_size=j.shape[0]
                output_loss = np.dot(last_layer_output_delta,wr1[e-1].T)
                output_delta = output_loss * derivative_activation(all_outputs1[e],a[e])
                #gr1.append(output_delta)
                grediant = (1./current_batch_size)*np.dot(j[:,0:-1].T,output_delta)
                #grediant=np.dot(j[:,0:-1].T,output_delta)/current_batch_size
                gr.append(grediant)
                if custome_grediant != None:
                  grediant+= custome_grediant
                #grediant = np.dot(j[:,0:-1].T,output_delta)
                if clipping == True:
                  grediant=np.clip(grediant, -self.__clipvalue, self.__clipvalue, out=grediant)
                #gr1.append(grediant)
                wr[e]-= self.learning_rate * grediant
                br[e]-= self.learning_rate * np.sum(output_delta,axis=0)
                gr1.append(np.sum(output_delta,axis=0))'''

            all_output1 = list(map(lambda x: all_outputs[x],self.__trainable_index))
            w1 = list(map(lambda x: self.weights[x],self.__trainable_index))
            b1 = list(map(lambda x: self.biases[x],self.__trainable_index))
            a1 = list(map(lambda x: self.activation[x],self.__trainable_index))

            if self.loss in('categorical_cross_entropy','categorical_crossentropy'):
              dw,db=compute_gradients_with_activations2(OneHotEncode(j[:,-1].reshape(-1,1)),y_pred,all_outputs,w,b,a,j[:,0:-1],self.loss)
            else:
              dw,db=compute_gradients_with_activations2(j[:,-1].reshape(-1,1),y_pred,all_outputs,w,b,a,j[:,0:-1],self.loss)
            #print(dw)
            #print(db)

            if clipping == True:
              dw=list(map(lambda x: np.clip(x, -clipvalue,clipvalue,out=x),dw))
              db=list(map(lambda x: np.clip(x, -clipvalue,clipvalue,out=x),db))

            if custome_grediant != None:
              dw=list(map(lambda x: x+custome_grediant,dw))
              db=list(map(lambda x: x+custome_grediant,db))


            if time_s == 0:
              w_previous_velosity=None
              b_previous_velosity=None
              w_previous_velosity_2=None
              b_previous_velosity_2=None
              w_previous_momentum=None
              b_previous_momentum=None
            new_weights,new_biases,w_previous_velosity,b_previous_velosity,w_previous_velosity_2,b_previous_velosity_2,w_previous_momentum,b_previous_momentum=optimizers(
                self.optimizer,
                j[:,0:-1],
                j[:,-1].reshape(-1,1),
                current_batch_size,
                self.weights,
                self.biases,
                dw,
                db,
                w_previous_velosity,
                b_previous_velosity,
                w_previous_velosity_2,
                b_previous_velosity_2,
                w_previous_momentum,
                b_previous_momentum,
                self.learning_rate,
                self.beta1,
                self.beta2,
                self.decay,
                self.epsilon,
                time_s,
                t_val)

            time_s+=1
            t_val+=1
            if len(self.__trainable_index) == len(self.weights):
              self.weights=new_weights
              self.biases=new_biases
            else:
              #ind_weights = dict(zip(self.__trainable_index,new_weights))
              #ind_biases = dict(zip(self.__trainable_index,new_biases))
              for ii2 in range(len(self.weights)):
                if ii2 in self.__trainable_index:
                  self.weights[ii2]=new_weights[ii2]
                  self.biases[ii2]=new_biases[ii2]



            #self.weights = list(reversed(wr))
            #self.biases = list(reversed(br))
          #y_p_b=((y_pred >= 0.5).astype(int))
          #y_pred_b = (y_pred >= 0.5).astype(int)
          y_pred1,all2=eval2(x_label,self.weights,self.biases,self.activation,self.__eval_dropout)
          if self.activation[-1] == 'softmax':
            y_pred_b=np.argmax(y_pred1,axis=1).reshape(-1,1)
          elif self.activation[-1] == 'sigmoid':
            y_pred_b=(y_pred1>=0.5).astype(int)
          else:
            y_pred_b=y_pred1

          if validation_data != None and isinstance(validation_data,(list,tuple)):
            #y_pre_test,y_pre_all=forward(validation_data[0],self.weights,self.biases,self.activation,self.dropout)
            y_pre_test,y_pre_all=eval2(validation_data[0],self.weights,self.biases,self.activation,self.__eval_dropout)
            #print(y_pre_test.shape)
            #print(validation_data[1].to_numpy().reshape(-1,1).shape)
            if self.activation[-1]=='softmax':
              y_pred_test_b=np.argmax(y_pre_test,axis=1).reshape(-1,1)
            elif self.activation[-1]=='sigmoid':
              y_pred_test_b=(y_pre_test>=0.5).astype(int)
            else:
              y_pred_test_b = y_pre_test
            #y_pred_test_b=(y_pre_test>=0.5).astype(int)
            #print(y_pred)
            if self.loss in('categorical_cross_entropy','categorical_crossentropy','binary_cross_entropy','binary_crossentropy'):
              #acc_tr=accuracy_score(j[:,-1],y_pred_b)
              acc_tr=accuracy_score(y_label,y_pred_b)
              acc_ts=accuracy_score(validation_data[1].to_numpy().reshape(-1,1),y_pred_test_b)
            else:
              #acc_tr=r2_score(j[:,-1],y_pred_b)
              acc_tr=r2_score(y_label,y_pred_b)
              #print(acc_tr)
              acc_ts=r2_score(validation_data[1].to_numpy().reshape(-1,1),y_pred_test_b)

              #print(acc_ts)
            self.history['epochs'].append(i)
            self.history['accuracy'].append(acc_tr)
            self.history['val_accuracy'].append(acc_ts)
            self.history['loss'].append(loss(y_label.to_numpy().flatten(),y_pred_b,self.loss))
            self.history['val_loss'].append(loss(validation_data[1].to_numpy().reshape(-1,1),y_pred_test_b,self.loss))

            '''if isinstance(callbacks,list):
              for c in callbacks:
                if c.name == 'optilearn.nn.ModelCheckpoint':
                  if i == 1:
                    pre_value = 0.0

                  bianary,f_name,check_value = c.check(self.history,self.history['epochs'][-1],pre_value)
                  pre_value = check_value
                  b=self.__checkpoint(bianary,f_name)

                elif c.name == 'optilearn.nn.EarlyStopping':
                  if i ==1:
                    pre_value_e = 0.0
                    time_step_e = 0

                  bianary_e,check_value_e,time_step_e1,bool_e = c.check(self.history,self.history['epochs'][-1],pre_value_e,time_step_e)
                  pre_value_e = check_value_e
                  time_step_e = time_step_e1
                  if c.restore_best_weights == True:
                    self.__best_weights,self.__best_biases = c.best_params(self.weights,self.biases)
                  b= self.__early_stopping(bianary_e)'''


            if verbose == 1:
              print(f"Epoch:{i}/{epochs}\nbatches: {batches_per_epoch}\n >>>training_accuracy : {acc_tr}\n training_loss : {loss(y_label.to_numpy().flatten(),y_pred_b,self.loss)}\n >>>validation_accuracy : {acc_ts}\n validation_loss : {loss(validation_data[1].to_numpy().reshape(-1,1),y_pred_test_b,self.loss)}")
              print()
            #print(f"Epoch: {i} loss : {sum(loss11)/len(loss11)}")
          else:
            if self.loss in('categorical_cross_entropy','categorical_crossentropy','binary_cross_entropy','binary_crossentropy'):
              #acc_tr=accuracy_score(j[:,-1],y_pred_b)
              acc_tr=accuracy_score(y_label,y_pred_b)
            else:
              #acc_tr = r2_score(j[:,-1],y_pred_b)
              acc_tr=r2_score(y_label,y_pred_b)
            self.history['epochs'].append(i)
            self.history['accuracy'].append(acc_tr)
            self.history['loss'].append(loss(j[:,-1],y_pred_b,self.loss))
            if verbose == 1:
              print(f"Epoch:{i}/{epochs}\nbatches: {batches_per_epoch}\n >>>training_accuracy : {acc_tr}\n training_loss :{loss(j[:,-1],y_pred_b,self.loss)}")
              print()

          if isinstance(callbacks,list):
              for c in callbacks:
                if c.name == 'optilearn.nn.ModelCheckpoint':
                  if i == 1:
                    pre_value = 0.0

                  bianary,f_name,check_value = c.check(self.history,self.history['epochs'][-1],pre_value)
                  pre_value = check_value
                  b=self.__checkpoint(bianary,f_name)

                elif c.name == 'optilearn.nn.EarlyStopping':
                  E=c
                  if i ==1:
                    pre_value_e = 0.0
                    time_step_e = 0

                  bianary_e,check_value_e,time_step_e1,bool_e = c.check(self.history,self.history['epochs'][-1],pre_value_e,time_step_e)
                  pre_value_e = check_value_e
                  time_step_e = time_step_e1
                  if c.restore_best_weights == True:
                    if i == 1:
                      pre_weights = None
                      pre_biases = None
                    p_w,p_b=c.best_params(self.weights,self.biases,pre_weights,pre_biases)
                    pre_weights = p_w
                    pre_biases = p_b
                  b= self.__early_stopping(bianary_e)

                elif c.name == 'optilearn.nn.ReduceLearningRate':
                  if i ==1:
                    pre_value_r = 0.0
                    time_step_r = 0
                    cooldown_timestep_r = 0

                  bianary_r,lr_rate,check_value_r,time_step_r1,cooldown_timestep_r1 = c.check(self.history,self.history['epochs'][-1],pre_value_r,time_step_r,self.learning_rate,cooldown_timestep_r)
                  pre_value_r = check_value_r
                  time_step_r = time_step_r1
                  cooldown_timestep_r = cooldown_timestep_r1
                  #print(cooldown_timestep_r)
                  b= self.__reduce_learning_rate(bianary_r,lr_rate)

          try:
            if len(self.history[E.monitor]) == 1:
              pre_value = self.history[E.monitor][0]
              self.__best_weights = self.weights
              self.__best_biases = self.biases
            else:
              if E.monitor in('accuracy','val_accuracy'):
                if self.history[E.monitor][-1] >= pre_value:
                  pre_value = self.history[E.monitor][-1]
                  self.__best_weights = self.weights
                  self.__best_biases = self.biases
                else:
                  pre_value = pre_value

              elif E.monitor in('loss','val_loss'):
                if self.history[E.monitor][-1] <= pre_value:
                  pre_value = self.history[E.monitor][-1]
                  self.__best_weights = self.weights
                  self.__best_biases = self.biases
                else:
                  pre_value = pre_value

          except:
            pass

          if b == 'break':
            break

        try:
          if E.restore_best_weights == True:
            self.weights = self.__best_weights
            self.biases = self.__best_biases
        except:
          pass

        '''if self.__best_weights != None and self.__best_biases != None:
          self.weights = self.__best_weights
          self.biases = self.__best_biases
        print(self.__best_weights)
        print(self.__best_biases)'''
        return self.history

  def save(self,file_name,saving_status = True):
    import h5py

    file_name1 = file_name

    ext=list([e for e in file_name1.split('.')])
    if ext[-1] != 'h5':
      raise ValueError(f"File extension must be 'h5'. Given type is '{ext[-1]}'")
    else:
      with h5py.File(file_name1,'a') as file:
        try:
          for i,(w,b) in enumerate(zip(self.weights,self.biases),start=0):
            file.create_dataset(f"weights : {i}",data=w)
            file.create_dataset(f"biases : {i}",data=b)
          file.create_dataset(f"activations",data=self.activation)
          file.create_dataset(f"dropouts",data=self.dropout)
        except Exception as ex:
          raise ex
        else:
          if saving_status == True:
            print(f"Model saved successfully")

  def predict(self,data,output_from_all_layers=False):

    def activation(x,name):
      def relu(x):
        return np.maximum(0, x)
      def sigmoid(x):
        return 1/(1+np.exp(-x))
      def softmax(output):
         #For numerical stability, subtract the maximum value from logits
        #print("Output Type:", type(output))
        exp_logits = np.exp(output - np.max(output, axis=1, keepdims=True))
        return exp_logits / np.sum(exp_logits, axis=1, keepdims=True)

      '''def softmax(output):
        # Ensure output is a NumPy array
        output = np.asarray(output)

        # For numerical stability, subtract the maximum value from logits
        exp_logits = np.exp(output - np.max(output, axis=1, keepdims=True))
        return exp_logits / np.sum(exp_logits, axis=1, keepdims=True)'''

      '''def softmax(output):
        """
        Applies softmax activation function.

        Args:
            output: NumPy array or a list.

        Returns:
            Softmax-activated output.
        """
        # Convert output to NumPy array with float dtype
        output = np.asarray(output, dtype=np.float64)

        # For numerical stability, subtract the maximum value from logits
        exp_logits = np.exp(output - np.max(output, axis=1, keepdims=True))
        return exp_logits / np.sum(exp_logits, axis=1, keepdims=True)'''
      def softmax1(x):
       # Prevent overflow
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
      def tanh(x):
        return np.tanh(x)
      def licky_relu(x):
        y=0.01*x
        return np.maximum(y,x)
      if name =='sigmoid':
        return sigmoid(x)
      elif name =='relu':
        return relu(x)
      elif name =='softmax':
        return softmax(x)

      elif name =='licky_relu':
        return licky_relu(x)
      elif name =='tanh':
        return tanh(x)
      elif name == 'linear':
        return x
      else:
        raise ValueError(f"activation function named '{name}' not found in the pridefine functions of 'Sequential()'")


    def eval2(x_train,weights,biases,activations,eval_dropouts):
      import numpy as np
      input=x_train
      all_outputs=[]
      for i in range(len(weights)):
        output=(np.dot(input,weights[i])+biases[i])*eval_dropouts[i]
        all_outputs.append(activation(output,activations[i]))
        input=activation(output,activations[i])
      #return tf.convert_to_tensor(input.astype('float32')),all_outputs
      return input,all_outputs

    eval_dropout = list(map(lambda x: 1-x,self.dropout))
    output,all_outputs=eval2(data,self.weights,self.biases,self.activation,eval_dropout)

    if output_from_all_layers == True:
      return all_outputs
    else:
      return output

  def summary(self):

    import numpy as np

    learnable_layers = dict(zip(list([i for i in range(len(self.layers)) if self.layers[i].name == 'optilearn.nn.Dense']),self.weights))

    all_layers_shape = []
    ex = 0
    for i in range(len(self.layers)):
      if self.layers[i].name == 'optilearn.nn.Dense':
        all_layers_shape.append(self.weights[ex].shape)
        ex+=1
      else:
        all_layers_shape.append(all_layers_shape[-1])
    output_shape = []
    for i in all_layers_shape:
      j = list(i)
      j[0]=None
      output_shape.append(tuple(j))

    ex1=0
    weights_and_zeros = []
    for l in self.layers:
      if l.name == 'optilearn.nn.Dense':
        weights_and_zeros.append(self.weights[ex1])
        ex1+=1
      else:
        weights_and_zeros.append(0)

    params = list(map(lambda x: (weights_and_zeros[x].shape[0] * weights_and_zeros[x].shape[1])+weights_and_zeros[x].shape[1] if type(weights_and_zeros[x]) == np.ndarray else 0,list(range(len(weights_and_zeros)))))
    total_params = sum(params)
    trainable_params = sum(list(map(lambda x: params[x] if self.layers[x].name == 'optilearn.nn.Dense' and self.layers[x].trainable == True else 0,list(range(len(params))))))

    header = f"Layers                           Output_shape                        Parameters"
    sep    = f"==============================================================================="
    #trainable_param = sum(list(map(lambda x: (self.weights[x].shape[0] * self.weights[x].shape[1])+self.weights[x].shape[1] if self.layers[x].name == 'optilearn.nn.Dense' and self.layers[x].trainable == True else 0,list(range(len(self.weights))))))
    #nontrainable_param = sum(list(map(lambda x: (self.weights[x].shape[0] * self.weights[x].shape[1])+self.weights[x].shape[1] if self.layers[x].name == 'optilearn.nn.Dense' and self.layers[x].trainable == False else 0,list(range(len(self.weights))))))
    body   = "\n\n".join([l.name + " "*(33-len(l.name)) + str(s) + " "*(36-len(str(s))) + str(p) for l,s,p in zip(self.layers,output_shape,params)])
    end_border = "-"
    print(f"{header}\n{sep}\n{body}\n{end_border * len(sep)}\n\nTotal_parameters : {total_params}\nTrainable_parameters : {trainable_params}\nNontrainable_parameters : {total_params - trainable_params}")


  def evaluate(self,data,y_label):
    import numpy as np
    from sklearn.metrics import accuracy_score,r2_score

    pre = self.predict(data)

    if self.loss == 'categorical_crossentropy':
      pre = np.argmax(pre,axis=1)

      return accuracy_score(y_label,pre)

    elif self.loss == 'binary_crossentropy':

      return accuracy_score(y_label,pre)

    elif self.loss in('mse','mae'):

      return r2_score(y_label,pre)


  def __checkpoint(self,bianary_value,file_name):

    if bianary_value == 1:
      self.save(file_name,saving_status=False)

      return None
    else:
      return None

  def __early_stopping(self,bianary_value,best_weights=None,best_biases=None):

    if best_weights != None and best_biases != None:
      self.weights = best_weights
      self.biases = best_biases

    if bianary_value == 1:
      return 'break'
    else:
      return None

  def __reduce_learning_rate(self,bianary_value,lr_rate):

    if bianary_value == 1:
      self.learning_rate = lr_rate
      return None

    else:
      return None


class Dropout:

  """
    A class representing a Dropout layer in a neural network.

    Dropout is a regularization technique used in neural networks to prevent overfitting.
    It works by randomly setting a fraction of the input units to zero at each update during 
    training time, which helps to prevent neurons from co-adapting too much.

    Attributes:
        name (str): The name of the class, typically used for identification in a neural network model.
        dropout_rate (float): The fraction of the input units to drop (set to zero) during training.
        
    Methods:
        __init__(dropout_rate=0.0):
            Initializes the Dropout layer with a given dropout rate.
        
        __drop():
            Returns the dropout rate for this layer.
    
    Example:
        # Create a Dropout layer with a dropout rate of 0.5 (50%)
        dropout_layer = Dropout(dropout_rate=0.5)
        
        # Access the dropout rate
        print(dropout_layer.__drop())  # Output: 0.5
    """

  name = 'optilearn.nn.Dropout'

  def __init__(self,dropout_rate=0.0):
    if isinstance(dropout_rate,float):
      self.dropout_rate=dropout_rate
    else:
      raise TypeError(f"dropout_rate must be float. But given type is {type(dropout_rate)}")
  def __drop(self):
    return self.dropout_rate
  
  
class ReduceLearningRate:

  """A callback to reduce the learning rate when a monitored metric has stopped improving.

    Parameters
    ----------
    * monitor : str, optional
        Metric to monitor. Choices are ['accuracy', 'val_accuracy', 'loss', 'val_loss'].

    * factor : float, optional
        Factor by which the learning rate will be reduced. `new_lr = lr * factor`.

    * patience : int, optional
        Number of epochs with no improvement after which learning rate will be reduced.

    * verbose : int, optional
        Verbosity mode. Set to 1 to print messages when learning rate is reduced.

    * min_delta : float, optional
        Minimum change in the monitored metric to qualify as an improvement.

    * cooldown : int, optional
        Number of epochs to wait after reducing the learning rate before resuming normal operation.

    * min_lr : float, optional
        Lower bound on the learning rate."""

  name = 'optilearn.nn.ReduceLearningRate'

  def __init__(self,monitor='val_accuracy',factor=0.1,patience=10,verbose=0,min_delta=1e-4,cooldown=0,min_lr=0):

    if monitor in('accuracy','val_accuracy','loss','val_loss'):
      self.monitor = monitor
    else:
      raise ValueError(f"Value of monitor parameter should be among ['accuracy','val_accuracy','loss','val_loss'].\nGiven value is {monitor}")
    self.factor = factor
    self.patience = patience
    self.verbose = verbose
    #self.mode = mode
    self.min_delta = min_delta
    self.cooldown = cooldown
    self.min_lr = min_lr
    self.current_learning_rate1 = None
    self.time_step1 = None
    self.cooldown_timestep1 = None
    self.check_value = None
    self.pre_value = None

  def check(self,metrics_values,number_of_epoch,pre_value,time_step,current_learning_rate,cooldown_timestep):

    """
        Checks whether the learning rate should be reduced based on monitored metric values.

        Parameters
        ----------
        * metrics_values : dict
            Dictionary containing metric values. The monitored metric should be a key in this dictionary.

        * number_of_epoch : int
            The current epoch number.

        * pre_value : float
            Previous value of the monitored metric.

        * time_step : int
            Number of epochs since the last improvement in the monitored metric.

        * current_learning_rate : float
            Current learning rate to be adjusted if necessary.

        * cooldown_timestep : int
            Number of epochs in the cooldown period.

        Returns
        -------
        tuple
            A tuple containing:
            - int : Flag indicating if learning rate was reduced (1 for reduced, 0 otherwise).
            - float : Updated learning rate.
            - float : Last monitored metric value that did not improve.
            - int : Updated time step.
            - int : Updated cooldown time step.
        """

    try:
      if len(metrics_values[self.monitor]) == 1:
        self.check_value = metrics_values[self.monitor][-1]
        return 0,current_learning_rate,self.check_value,time_step,cooldown_timestep

      else:
        #if self.mode == 'auto':
        if self.monitor in('accuracy','val_accuracy'):
          if cooldown_timestep == 0:
            if (metrics_values[self.monitor][-1] - pre_value) < self.min_delta :
              self.time_step1 = time_step+1
              self.check_value = pre_value
              if (self.time_step1 -1) == self.patience:
                self.current_learning_rate1 = current_learning_rate * self.factor
                if self.current_learning_rate1 < self.min_lr:
                  self.current_learning_rate1 = self.min_lr
                if self.cooldown == 0:
                  self.time_step1 = 0
                  if self.verbose == 1:
                    print()
                    print(f"learning_rate got reduced from {current_learning_rate} to {self.current_learning_rate1}")
                    print()
                  return 1,self.current_learning_rate1,self.check_value,self.time_step1,cooldown_timestep
                else:
                  if (metrics_values[self.monitor][-1] - pre_value) < self.min_delta :
                    self.cooldown_timestep1 = cooldown_timestep+1
                    print()
                    print(f"cooldown count : {self.cooldown_timestep1}/{self.cooldown}")
                    print()
                    if (self.cooldown_timestep1 -1) == self.cooldown:
                      self.time_step1 = 0
                      self.cooldown_timestep1 = 0
                      if self.verbose == 1:
                        print()
                        print(f"{self.monitor} didn't improve during cooldown period\n\n--> learning_rate got reduced from {current_learning_rate} to {self.current_learning_rate1}")
                      return 1,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1
                    else:
                      return 0,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1
                  else:
                    self.time_step1 = 0
                    self.cooldown_timestep1 = 0
                    self.current_learning_rate1 = current_learning_rate
                    if self.verbose ==1:
                      print()
                      print(f"{self.monitor} got improved during cooldown period")
                      print()
                    return 0,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1

              else:
                return 0,current_learning_rate,self.check_value,self.time_step1,cooldown_timestep

            else:
              self.time_step1 = 0
              self.cooldown_timestep1 = 0
              self.current_learning_rate1 = current_learning_rate
              self.check_value = metrics_values[self.monitor][-1]
              return 0,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1

          else:
            if (metrics_values[self.monitor][-1] - pre_value) < self.min_delta :
              self.cooldown_timestep1 = cooldown_timestep+1
              if self.cooldown_timestep1 <= self.cooldown:
                print()
                print(f"cooldown count : {self.cooldown_timestep1}/{self.cooldown}")
                print()
              if (self.cooldown_timestep1 -1) == self.cooldown:
                self.time_step1 = 0
                self.cooldown_timestep1 = 0
                if self.verbose == 1:
                  print()
                  print(f"{self.monitor} didn't improve during cooldown period\n\n--> learning_rate got reduced from {current_learning_rate} to {self.current_learning_rate1}")
                  print()
                return 1,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1
              else:
                return 0,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1

            else:
              self.time_step1 = 0
              self.cooldown_timestep1 = 0
              self.current_learning_rate1 = current_learning_rate
              self.check_value = metrics_values[self.monitor][-1]
              if self.verbose ==1:
                print()
                print(f"{self.monitor} got improved during cooldown period")
                print()
              return 0,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1




        elif self.monitor in('loss','val_loss'):
          if cooldown_timestep == 0:
            if (pre_value - metrics_values[self.monitor][-1]) < self.min_delta :
              self.time_step1 = time_step+1
              self.check_value = pre_value
              if (self.time_step1 -1) == self.patience:
                self.current_learning_rate1 = current_learning_rate * self.factor
                if self.current_learning_rate1 < self.min_lr:
                  self.current_learning_rate1 = self.min_lr
                if self.cooldown == 0:
                  self.time_step1 = 0
                  if self.verbose == 1:
                    print()
                    print(f"learning_rate got reduced from {current_learning_rate} to {self.current_learning_rate1}")
                    print()
                  return 1,self.current_learning_rate1,self.check_value,self.time_step1,cooldown_timestep

                else:
                  if (pre_value - metrics_values[self.monitor][-1]) < self.min_delta :
                    self.cooldown_timestep1 = cooldown_timestep+1
                    print()
                    print(f"cooldown count : {self.cooldown_timestep1}/{self.cooldown}")
                    print()
                    if self.cooldown_timestep1 == self.cooldown:
                      self.time_step1 = 0
                      self.cooldown_timestep1 = 0
                      if self.verbose == 1:
                        print()
                        print(f"{self.monitor} didn't improve during cooldown period\n\n--> learning_rate got reduced from {current_learning_rate} to {self.current_learning_rate1}")
                      return 1,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1
                    else:
                      return 0,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1

                  else:
                    self.time_step1 = 0
                    self.cooldown_timestep1 = 0
                    self.current_learning_rate1 = current_learning_rate
                    if self.verbose ==1:
                      print()
                      print(f"{self.monitor} got improved during cooldown period")
                      print()
                    return 0,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1

              else:
                return 0,current_learning_rate,self.check_value,self.time_step1,cooldown_timestep

            else:
              self.time_step1 = 0
              self.cooldown_timestep1 = 0
              self.current_learning_rate1 = current_learning_rate
              self.check_value = metrics_values[self.monitor][-1]
              return 0,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1

          else:
            if (pre_value - metrics_values[self.monitor][-1]) < self.min_delta :
              self.cooldown_timestep1 = cooldown_timestep+1
              if self.cooldown_timestep1 <= self.cooldown:
                print()
                print(f"cooldown count : {self.cooldown_timestep1}/{self.cooldown}")
                print()
              if (self.cooldown_timestep1 -1) == self.cooldown:
                self.time_step1 = 0
                self.cooldown_timestep1 = 0
                if self.verbose == 1:
                  print()
                  print(f"{self.monitor} didn't improve during cooldown period\n\n--> learning_rate got reduced from {current_learning_rate} to {self.current_learning_rate1}")
                  print()
                return 1,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1
              else:
                return 0,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1

            else:
              self.time_step1 = 0
              self.cooldown_timestep1 = 0
              self.current_learning_rate1 = current_learning_rate
              self.check_value = metrics_values[self.monitor][-1]
              if self.verbose ==1:
                print()
                print(f"{self.monitor} got improved during cooldown period")
                print()
              return 0,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1



        '''elif self.mode == 'max':
          if cooldown_timestep == 0:
            if (metrics_values[self.monitor][-1] - pre_value) < self.min_delta :
              self.time_step1 = time_step+1
              self.check_value = pre_value
              if (self.time_step1 -1) == self.patience:
                self.current_learning_rate1 = current_learning_rate * self.factor
                if self.current_learning_rate1 < self.min_lr:
                  self.current_learning_rate1 = self.min_lr
                if self.cooldown == 0:
                  self.time_step1 = 0
                  if self.verbose == 1:
                    print()
                    print(f"learning_rate got reduced from {current_learning_rate} to {self.current_learning_rate1}")
                    print()
                  return 1,self.current_learning_rate1,self.check_value,self.time_step1,cooldown_timestep

                else:
                  if (metrics_values[self.monitor][-1] - pre_value) < self.min_delta :
                    self.cooldown_timestep1 = cooldown_timestep+1
                    print()
                    print(f"cooldown count : {self.cooldown_timestep1}/{self.cooldown}")
                    print()
                    if self.cooldown_timestep1 == self.cooldown:
                      self.time_step1 = 0
                      self.cooldown_timestep1 = 0
                      if self.verbose == 1:
                        print()
                        print(f"{self.monitor} didn't increase during cooldown period\n\n--> learning_rate got reduced from {current_learning_rate} to {self.current_learning_rate1}")
                      return 1,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1
                    else:
                      return 0,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1

                  else:
                    self.time_step1 = 0
                    self.cooldown_timestep1 = 0
                    self.current_learning_rate1 = current_learning_rate
                    if self.verbose ==1:
                      print()
                      print(f"{self.monitor} got increased during cooldown period")
                      print()
                    return 0,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1

            else:
              self.time_step1 = 0
              self.cooldown_timestep1 = 0
              self.current_learning_rate1 = current_learning_rate
              self.check_value = metrics_values[self.monitor][-1]
              return 0,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1

          else:
            if (metrics_values[self.monitor][-1] - pre_value) < self.min_delta :
              self.cooldown_timestep1 = cooldown_timestep+1
              if self.cooldown_timestep1 <= self.cooldown:
                print()
                print(f"cooldown count : {self.cooldown_timestep1}/{self.cooldown}")
                print()
              if (self.cooldown_timestep1 -1) == self.cooldown:
                self.time_step1 = 0
                self.cooldown_timestep1 = 0
                if self.verbose == 1:
                  print()
                  print(f"{self.monitor} didn't increase during cooldown period\n\n--> learning_rate got reduced from {current_learning_rate} to {self.current_learning_rate1}")
                  print()
                return 1,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1
              else:
                return 0,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1
            else:
              self.time_step1 = 0
              self.cooldown_timestep1 = 0
              self.current_learning_rate1 = current_learning_rate
              self.check_value = metrics_values[self.monitor][-1]
              if self.verbose ==1:
                print()
                print(f"{self.monitor} got increased during cooldown period")
                print()
              return 0,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1

        elif self.mode == 'min':
          if cooldown_timestep == 0:
            if (pre_value - metrics_values[self.monitor][-1]) < self.min_delta :
              self.time_step1 = time_step+1
              self.check_value = pre_value
              if (self.time_step1 -1) == self.patience:
                self.current_learning_rate1 = current_learning_rate * self.factor
                if self.current_learning_rate1 < self.min_lr:
                  self.current_learning_rate1 = self.min_lr
                if self.cooldown == 0:
                  self.time_step1 = 0
                  if self.verbose == 1:
                    print()
                    print(f"learning_rate got reduced from {current_learning_rate} to {self.current_learning_rate1}")
                    print()
                  return 1,self.current_learning_rate1,self.check_value,self.time_step1,cooldown_timestep

                else:
                  if (pre_value - metrics_values[self.monitor][-1]) < self.min_delta :
                    self.cooldown_timestep1 = cooldown_timestep+1
                    if self.cooldown_timestep1 == self.cooldown:
                      self.time_step1 = 0
                      self.cooldown_timestep1 = 0
                      if self.verbose == 1:
                        print()
                        print(f"{self.monitor} didn't decrease during cooldown period\n\n--> learning_rate got reduced from {current_learning_rate} to {self.current_learning_rate1}")
                      return 1,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1
                    else:
                      return 0,self.current_learning_rate1,self.check_value,self.time_step1,cooldown_timestep

                  else:
                    self.time_step1 = 0
                    self.cooldown_timestep1 = 0
                    self.current_learning_rate1 = current_learning_rate
                    if self.verbose ==1:
                      print()
                      print(f"{self.monitor} got decreased during cooldown period")
                    return 0,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1

              else:
                return 0,current_learning_rate,self.check_value,self.time_step1,cooldown_timestep
            else:
              self.time_step1 = 0
              self.cooldown_timestep1 = 0
              self.current_learning_rate1 = current_learning_rate
              self.check_value = metrics_values[self.monitor][-1]
              return 0,current_learning_rate,self.check_value,self.time_step1,self.cooldown_timestep1

          else:
            if (pre_value - metrics_values[self.monitor][-1]) < self.min_delta :
              self.cooldown_timestep1 = cooldown_timestep+1
              if self.cooldown_timestep1 <= self.cooldown:
                print()
                print(f"cooldown count : {self.cooldown_timestep1}/{self.cooldown}")
                print()
              if (self.cooldown_timestep1 -1) == self.cooldown:
                self.time_step1 = 0
                self.cooldown_timestep1 = 0
                if self.verbose == 1:
                  print()
                  print(f"{self.monitor} didn't decrease during cooldown period\n\n--> learning_rate got reduced from {current_learning_rate} to {self.current_learning_rate1}")
                  print()
                return 1,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1
              else:
                return 0,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1
            else:
              self.time_step1 = 0
              self.cooldown_timestep1 = 0
              self.current_learning_rate1 = current_learning_rate
              self.check_value = metrics_values[self.monitor][-1]
              if self.verbose ==1:
                print()
                print(f"{self.monitor} got decreased during cooldown period")
                print()
              return 0,self.current_learning_rate1,self.check_value,self.time_step1,self.cooldown_timestep1'''


    except Exception as ex:
      raise ex
    

class EarlyStopping:

  """EarlyStopping is a callback to stop training when a monitored metric has stopped improving.

    This class monitors a specific metric (e.g., accuracy or loss) and halts training if the metric fails to improve
    after a defined number of epochs (`patience`). The stopping criteria can be customized to monitor either increases
    or decreases in the metric.

    Parameters
    ----------
    * monitor : str, optional
        Metric to monitor for early stopping. Options include ['accuracy', 'val_accuracy', 'loss', 'val_loss'].

    * mode : str, optional
        Determines whether the monitored metric should increase ('max') or decrease ('min') to be considered as an improvement.
        'auto' mode will infer the appropriate mode based on the selected metric.

    * patience : int, optional
        Number of epochs with no improvement after which training will be stopped.

    * verbose : int, optional
        Verbosity mode; set to 1 for progress messages when early stopping is triggered.

    * min_delta : float, optional
        Minimum change in the monitored metric to qualify as an improvement.

    * baseline : float, optional
        Baseline value for the monitored metric, training stops if the metric surpasses or falls below this value.

    * restore_best_weights : bool, optional
        If True, the model weights from the epoch with the best value of the monitored metric will be restored."""

  name = 'optilearn.nn.EarlyStopping'

  def __init__(self,monitor='val_accuracy',mode='auto',patience=5,verbose=0,min_delta=0,baseline=1.0,restore_best_weights=False):

    if monitor in('accuracy','val_accuracy','loss','val_loss'):
      self.monitor = monitor
    else:
      raise ValueError(f"Valid values for 'monitor' attribute are ['accuracy','val_accuracy','loss','val_loss']. But given value is {monitor}")
    self.mode = mode
    self.patience = patience
    self.verbose = verbose
    self.min_delta = min_delta
    self.baseline = baseline
    self.restore_best_weights = restore_best_weights

    self.check_value = None
    self.pre_value = None
    self.__metrics_values = None
    self.best_weights = None
    self.best_biases = None

  def check(self,metrics_values,number_of_epoch,pre_value,time_step):

    """
        Checks whether training should be stopped based on the monitored metric.

        This method compares the monitored metric's current value with previous values and the baseline.
        If the metric fails to improve by the specified `min_delta` within `patience` epochs, early stopping is triggered.

        Parameters
        ----------
        metrics_values : dict
            Dictionary containing metric values for each epoch, with the monitored metric as a key.
        number_of_epoch : int
            The current epoch number.
        pre_value : float
            The previous value of the monitored metric.
        time_step : int
            Number of epochs since the last improvement in the monitored metric.

        Returns
        -------
        tuple
            - int : Flag indicating if early stopping was triggered (1 for stop, 0 for continue).
            - float : Current monitored metric value.
            - int : Updated time step (count of epochs without improvement).
            - int : Flag for cooldown status, where 0 indicates the cooldown period is not active.
        """

    self.pre_value = pre_value
    self.__metrics_values = metrics_values

    try:
      if len(metrics_values[self.monitor]) == 1:
        self.check_value = metrics_values[self.monitor][-1]
        if self.monitor in('accuracy','val_accuracy'):
          if self.check_value >= self.baseline:
            print()
            print(f"{self.monitor} reached to {self.check_value} \n training got stopped at epoch {number_of_epoch}")
            return 1,self.check_value,time_step,0

          else:
            return 0,self.check_value,time_step,0

        elif self.monitor in('loss','val_loss'):
          if self.check_value <= self.baseline:
            return 1,self.check_value,time_step,0
          else:
            return 0,self.check_value,time_step,0

      else:
        if self.mode == 'auto':
          if self.monitor in('accuracy','val_accuracy'):
            #if self.baseline != None:
            if metrics_values[self.monitor][-1] >= self.baseline:
              print()
              print(f"{self.monitor} reached to {metrics_values[self.monitor][-1]} \n training got stopped at epoch {number_of_epoch}")
              return 1,None,time_step,0

            else:
              if (metrics_values[self.monitor][-1] - pre_value) < self.min_delta :
                #check_value = metrics_values[self.monitor][-1]
                self.check_value = pre_value
                time_step1 = time_step+1
                if (time_step1 - 1) == self.patience:
                  if self.verbose == 1:
                    print()
                    print(f"Early stopping triggered at epoch {number_of_epoch}")
                  return 1,self.check_value,time_step1,0
                else:
                  return 0,self.check_value,time_step1,0

              else:
                self.check_value = metrics_values[self.monitor][-1]
                time_step1 = 0
                return 0,self.check_value,time_step1,0

          elif self.monitor in('loss','val_loss'):
            if metrics_values[self.monitor][-1] <= self.baseline:
              print()
              print(f"{self.monitor} reached to {metrics_values[self.monitor][-1]} \n training got stopped at epoch {number_of_epoch}")
              return 1,None,time_step,0
            else:
              if (pre_value - metrics_values[self.monitor][-1]) < self.min_delta :
                self.check_value = pre_value
                time_step1 = time_step+1
                if (time_step1 - 1) == self.patience:
                  if self.verbose == 1:
                    print()
                    print(f"Early stopping triggered at epoch {number_of_epoch}")
                  return 1,self.check_value,time_step1,0
                else:
                  return 0,self.check_value,time_step1,0

              else:
                self.check_value = metrics_values[self.monitor][-1]
                time_step1 = 0
                return 0,self.check_value,time_step1,0

        elif self.mode == 'max':
          if metrics_values[self.monitor][-1] >= self.baseline:
            print()
            print(f"{self.monitor} reached to {metrics_values[self.monitor][-1]} \n training got stopped at epoch {number_of_epoch}")
            return 1,None,time_step,0
          else:
            if (metrics_values[self.monitor][-1] - pre_value) < self.min_delta :
              self.check_value = pre_value
              time_step1 = time_step+1
              if (time_step1 - 1) == self.patience:
                if self.verbose == 1:
                  print()
                  print(f"Early stopping triggered at epoch {number_of_epoch}")
                return 1,self.check_value,time_step1,0
              else:
                return 0,self.check_value,time_step1,0
            else:
              self.check_value = metrics_values[self.monitor][-1]
              time_step1 = 0
              return 0,self.check_value,time_step1,0

        elif self.mode == 'min':
          if metrics_values[self.monitor][-1] <= self.baseline:
            print()
            print(f"{self.monitor} reached to {metrics_values[self.monitor][-1]} \n training got stopped at epoch {number_of_epoch}")
            return 1,None,time_step,0
          else:
            if (pre_value - metrics_values[self.monitor][-1]) < self.min_delta :
              self.check_value = pre_value
              time_step1 = time_step+1
              if (time_step1 - 1) == self.patience:
                if self.verbose == 1:
                  print()
                  print(f"Early stopping triggered at epoch {number_of_epoch}")
                  return 1,self.check_value,time_step1,0
              else:
                return 0,self.check_value,time_step1,0
            else:
              self.check_value = metrics_values[self.monitor][-1]
              time_step1 = 0
              return 0,self.check_value,time_step1,0

        else:
          raise ValueError(f"Valid values for 'mode' attribute are ['auto','max','min']. But given value is {self.mode}")

    except Exception as ex:
      raise ex

  def best_params(self,weights,biases,privious_weights,previous_biases):

    try:
      if len(self.__metrics_values[self.monitor]) == 1:
        self.best_weights = weights
        self.best_biases = biases
        return self.best_weights,self.best_biases
      else:
        if self.monitor in('accuracy','val_accuracy'):
          if self.check_value >= self.pre_value:
            self.best_weights = weights
            self.best_biases = biases
            return self.best_weights,self.best_biases
          else:
            self.best_weights = privious_weights
            self.best_biases = previous_biases
            return self.best_weights,self.best_biases

        elif self.monitor in('loss','val_loss'):
          if self.check_value <= self.pre_value:
            self.best_weights = weights
            self.best_biases = biases
            return self.best_weights,self.best_biases
          else:
            self.best_weights = privious_weights
            self.best_biases = previous_biases
            return self.best_weights,self.best_biases

    except Exception as ex:
      raise ex

    #else:
      #return self.best_weights,self.best_biases


class ModelCheckpoint:

  """Implements a checkpointing mechanism to save model weights during training based on monitored metrics.

    Attributes:
    ----------
    * file_name : str
        The base file name for saved checkpoints. Must have an 'h5' extension.

    * monitor : str
        The metric to monitor, which can be one of ['accuracy', 'val_accuracy', 'loss', 'val_loss'].

    * mode : str
        Specifies the checkpointing mode. Options are:
        - 'auto': Automatically decides the direction of improvement based on the monitored metric.
        - 'max': Saves checkpoints when monitored metric increases.
        - 'min': Saves checkpoints when monitored metric decreases.

    * save_best_only : bool
        If True, only saves checkpoints when the monitored metric improves.

    * verbose : int
        If set to 1, provides detailed logging output during the checkpoint process."""

  name = 'optilearn.nn.ModelCheckpoint'

  def __init__(self,file_name,monitor='val_acccuracy',mode='auto',save_best_only=False,verbose=0):

    ext = list([et for et in file_name.split('.')])
    if ext[-1] == 'h5':
      self.file_name = file_name
    else:
      raise ValueError(f"file extension must be 'h5'. Recived type is '{ext[-1]}'")

    if monitor in('accuracy','val_accuracy','loss','val_loss'):
      self.monitor = monitor
    else:
      raise ValueError(f"Valid values for 'monitor' attribute are ['accuracy','val_accuracy','loss','val_loss']. But given value is {monitor}")

    self.mode = mode
    self.save_best_only =  save_best_only
    self.verbose = verbose

  def check(self,metrics_values,number_of_epoch,pre_value):

    """Evaluates whether the model checkpoint should be saved based on the monitored metric's value.

    Parameters
    ----------
    metrics_values : dict
        Dictionary containing the latest recorded values of metrics. The specified monitored metric
        should be included in this dictionary.
    number_of_epoch : int
        The current epoch number during training.
    pre_value : float
        The previous best value of the monitored metric for comparison with the current value.

    Returns
    -------
    tuple
        A tuple containing:
        - `int`: 1 if a checkpoint was saved, 0 otherwise.
        - `str`: The generated file name for the saved checkpoint.
        - `float`: The monitored metric's value for the current epoch."""

    try:

      if len(metrics_values[self.monitor]) == 1:
        check_value = metrics_values[self.monitor][-1]
        f_name = f"{self.file_name[0:-3]}-epoch : {number_of_epoch}-{self.monitor} : {check_value}.h5"

        if self.verbose == 1:
          print(f"{f_name} is saved successfully")
        return 1,f_name,check_value

      else:

        if self.save_best_only == False:
          check_value = metrics_values[self.monitor][-1]
          f_name = f"{self.file_name[0:-3]}-epoch : {number_of_epoch}-{self.monitor} : {check_value}.h5"

          if self.verbose == 1:
            print(f"{f_name} is saved successfully")
          return 1,f_name,check_value

        elif self.save_best_only == True:
          if self.mode == 'auto':

            if self.monitor in('accuracy','val_accuracy'):

              if metrics_values[self.monitor][-1] > pre_value:
                check_value = metrics_values[self.monitor][-1]
                f_name = f"{self.file_name[0:-3]}-epoch : {number_of_epoch}-{self.monitor} : {check_value}.h5"
                if self.verbose == 1:
                  print(f"{self.monitor} is improved from {pre_value}")
                  print(f"{f_name} is saved successfully")
                return 1,f_name,check_value

              else:
                check_value = pre_value
                f_name = f"{self.file_name[0:-3]}-epoch : {number_of_epoch}-{self.monitor} : {check_value}.h5"
                if self.verbose == 1:
                  print(f"---> {self.monitor} didn't inprove from {pre_value}")
                  print()
                return 0,f_name,check_value

            elif self.monitor in('loss','val_loss'):

              if metrics_values[self.monitor][-1] < pre_value :
                check_value = metrics_values[self.monitor][-1]
                f_name = f"{self.file_name[0:-3]}-epoch : {number_of_epoch}-{self.monitor} : {check_value}.h5"
                if self.verbose == 1:
                  print(f"---> {self.monitor} is improved from {pre_value}")
                  print(f"---> {f_name} is saved successfully")
                  print()
                return 1,f_name,check_value

              else:
                check_value = pre_value
                f_name = f"{self.file_name[0:-3]}-epoch : {number_of_epoch}-{self.monitor} : {check_value}.h5"
                if self.verbose == 1:
                  print(f"---> {self.monitor} didn't inprove from {pre_value}")
                  print()
                return 0,f_name,check_value

          elif self.mode == 'max':

            if metrics_values[self.monitor][-1] > pre_value:
              check_value = metrics_values[self.monitor][-1]
              f_name = f"{self.file_name[0:-3]}-epoch : {number_of_epoch}-{self.monitor} : {check_value}.h5"
              if self.verbose == 1:
                print(f"---> {self.monitor} is increased from {pre_value}")
                print(f"---> {f_name} is saved successfully")
                print()
              return 1,f_name,check_value

            else:
              check_value = pre_value
              f_name = f"{self.file_name[0:-3]}-epoch : {number_of_epoch}-{self.monitor} : {check_value}.h5"
              if self.verbose == 1:
                print(f"---> {self.monitor} didn't increase from {pre_value}")
                print()
              return 0,f_name,check_value

          elif self.mode == 'min':

            if metrics_values[self.monitor][-1] < pre_value:
              check_value = metrics_values[self.monitor][-1]
              f_name = f"{self.file_name[0:-3]}-epoch : {number_of_epoch}-{self.monitor} : {check_value}.h5"
              if self.verbose == 1:
                print(f"---> {self.monitor} is decreased from {pre_value}")
                print(f"---> {f_name} is saved successfully")
                print()
              return 1,f_name,check_value

            else:
              check_value = pre_value
              f_name = f"{self.file_name[0:-3]}-epoch : {number_of_epoch}-{self.monitor} : {check_value}.h5"
              if self.verbose == 1:
                print(f"---> {self.monitor} didn't decrease from {pre_value}")
                print()
              return 0,f_name,check_value

          else:
            raise ValueError(f"Valid values for 'mode' attribute are ['auto','max','min']. But given value is {self.mode}")

        else:
          raise TypeError(f"'save_best_only' must be a 'bool' object")

    except Exception as ex:
      raise ex


def load_model(file_path):

  """
    Loads a neural network model from an H5 file, including weights, biases, activation functions, and dropout rates.

    Parameters
    ----------
    * file_path : str
        The path to the H5 file containing the model parameters.

    Returns
    -------
    Sequential1
        An instance of the `Sequential` class with loaded weights, biases, activations, and dropouts.


    Examples
    --------
    >>> model = load_model("my_model.h5")
    >>> print("Loaded model:", model)
    """

  import numpy as np
  import h5py

  path=file_path

  if isinstance(path,str):
    ext=list([ex for ex in path.split('.')])

    parameters=[]
    if ext[-1] == 'h5':
      try:
        with h5py.File(path,'r') as file:
          for k in file.keys():
            if k == 'activations':
              activations = list(map(lambda x: str(x)[2:-1],np.array(file[k])))
            elif k == 'dropouts':
              dropouts = list(map(lambda x: x,np.array(file[k])))
            else:
              parameters.append(np.array(file[k]))

      except Exception as ex:
        raise ex

      else:
        biases = parameters[0:int(len(parameters)/2)]
        weights = parameters[int(len(parameters)/2)::]

        model = Sequential1()
        model.weights = weights
        model.biases = biases
        model.activation = activations
        model.dropout = dropouts

      print('Model loaded successfully')

      return model

    else:
      raise ValueError(f"file extension must be 'h5'. Recived type is '{ext[-1]}'")

  else:
    raise TypeError(f"'file_path' must be a 'str' object. But recived type is {type(file_path)}")


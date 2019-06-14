from builtins import range
import numpy as np


def affine_forward(x, w, b):
    """
    Computes the forward pass for an affine (fully-connected) layer.

    The input x has shape (N, d_1, ..., d_k) and contains a minibatch of N
    examples, where each example x[i] has shape (d_1, ..., d_k). We will
    reshape each input into a vector of dimension D = d_1 * ... * d_k, and
    then transform it to an output vector of dimension M.

    Inputs:
    - x: A numpy array containing input data, of shape (N, d_1, ..., d_k)
    - w: A numpy array of weights, of shape (D, M)
    - b: A numpy array of biases, of shape (M,)

    Returns a tuple of:
    - out: output, of shape (N, M)
    - cache: (x, w, b)
    """
    out = None
    ###########################################################################
    # TODO: Implement the affine forward pass. Store the result in out. You   #
    # will need to reshape the input into rows.                               #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    out = x.reshape( np.shape(x)[0], -1)
    out = np.dot( out ,w)
    out += b

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, w, b)
    return out, cache


def affine_backward(dout, cache):
    """
    Computes the backward pass for an affine layer.

    Inputs:
    - dout: Upstream derivative, of shape (N, M)
    - cache: Tuple of:
      - x: Input data, of shape (N, d_1, ... d_k)
      - w: Weights, of shape (D, M)
      - b: Biases, of shape (M,)

    Returns a tuple of:
    - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
    - dw: Gradient with respect to w, of shape (D, M)
    - db: Gradient with respect to b, of shape (M,)
    """
    x, w, b = cache
    dx, dw, db = None, None, None
    ###########################################################################
    # TODO: Implement the affine backward pass.                               #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    # Use the same formulas as in the handout (and used in assignment 1)
    N = np.shape(x)[0]
    db = np.sum(dout, axis=0)
    
    x_reshaped = x.reshape( N, -1)
    dw = np.dot( np.transpose(x_reshaped) , dout )
    
    dx = np.dot( dout, np.transpose(w) )
    dx = np.reshape(dx, np.shape(x) )

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dw, db


def relu_forward(x):
    """
    Computes the forward pass for a layer of rectified linear units (ReLUs).

    Input:
    - x: Inputs, of any shape

    Returns a tuple of:
    - out: Output, of the same shape as x
    - cache: x
    """
    out = None
    ###########################################################################
    # TODO: Implement the ReLU forward pass.                                  #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    out = np.copy(x)
    out[out < 0] = 0

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = x
    return out, cache


def relu_backward(dout, cache):
    """
    Computes the backward pass for a layer of rectified linear units (ReLUs).

    Input:
    - dout: Upstream derivatives, of any shape
    - cache: Input x, of same shape as dout

    Returns:
    - dx: Gradient with respect to x
    """
    dx, x = None, cache
    ###########################################################################
    # TODO: Implement the ReLU backward pass.                                 #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    dx = dout
    dx[x < 0] = 0

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx


def batchnorm_forward(x, gamma, beta, bn_param):
    """
    Forward pass for batch normalization.

    During training the sample mean and (uncorrected) sample variance are
    computed from minibatch statistics and used to normalize the incoming data.
    During training we also keep an exponentially decaying running mean of the
    mean and variance of each feature, and these averages are used to normalize
    data at test-time.

    At each timestep we update the running averages for mean and variance using
    an exponential decay based on the momentum parameter:

    running_mean = momentum * running_mean + (1 - momentum) * sample_mean
    running_var = momentum * running_var + (1 - momentum) * sample_var

    Note that the batch normalization paper suggests a different test-time
    behavior: they compute sample mean and variance for each feature using a
    large number of training images rather than using a running average. For
    this implementation we have chosen to use running averages instead since
    they do not require an additional estimation step; the torch7
    implementation of batch normalization also uses running averages.

    Input:
    - x: Data of shape (N, D)
    - gamma: Scale parameter of shape (D,)
    - beta: Shift paremeter of shape (D,)
    - bn_param: Dictionary with the following keys:
      - mode: 'train' or 'test'; required
      - eps: Constant for numeric stability
      - momentum: Constant for running mean / variance.
      - running_mean: Array of shape (D,) giving running mean of features
      - running_var Array of shape (D,) giving running variance of features

    Returns a tuple of:
    - out: of shape (N, D)
    - cache: A tuple of values needed in the backward pass
    """
    mode = bn_param['mode']
    eps = bn_param.get('eps', 1e-5)
    momentum = bn_param.get('momentum', 0.9)

    N, D = x.shape
    running_mean = bn_param.get('running_mean', np.zeros(D, dtype=x.dtype))
    running_var = bn_param.get('running_var', np.zeros(D, dtype=x.dtype))

    out, cache = None, None
    if mode == 'train':
        #######################################################################
        # TODO: Implement the training-time forward pass for batch norm.      #
        # Use minibatch statistics to compute the mean and variance, use      #
        # these statistics to normalize the incoming data, and scale and      #
        # shift the normalized data using gamma and beta.                     #
        #                                                                     #
        # You should store the output in the variable out. Any intermediates  #
        # that you need for the backward pass should be stored in the cache   #
        # variable.                                                           #
        #                                                                     #
        # You should also use your computed sample mean and variance together #
        # with the momentum variable to update the running mean and running   #
        # variance, storing your result in the running_mean and running_var   #
        # variables.                                                          #
        #                                                                     #
        # Note that though you should be keeping track of the running         #
        # variance, you should normalize the data based on the standard       #
        # deviation (square root of variance) instead!                        # 
        # Referencing the original paper (https://arxiv.org/abs/1502.03167)   #
        # might prove to be helpful.                                          #
        #######################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        sample_mean = np.sum( x, axis= 0 ) / N
        sample_variance = np.sum ( (x - sample_mean) ** 2, axis = 0 ) / N
        x_hat =  (x - sample_mean) / np.sqrt(sample_variance + eps)
        out = gamma * x_hat + beta
        
        # accomodate for layer norm 
        bn_param.setdefault('layer', 0)
        
        if (bn_param['layer'] == 0):
            running_mean = running_mean * momentum + ( 1 - momentum)* \
            sample_mean
        
            running_var = running_var * momentum + ( 1 - momentum)* \
            sample_variance
        
        cache = (sample_mean, sample_variance, x, x_hat, beta, gamma, eps)

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        #######################################################################
        #                           END OF YOUR CODE                          #
        #######################################################################
    elif mode == 'test':
        #######################################################################
        # TODO: Implement the test-time forward pass for batch normalization. #
        # Use the running mean and variance to normalize the incoming data,   #
        # then scale and shift the normalized data using gamma and beta.      #
        # Store the result in the out variable.                               #
        #######################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        x_hat = (x - running_mean) / (np.sqrt( running_var + eps) )
        out = gamma * x_hat + beta

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        #######################################################################
        #                          END OF YOUR CODE                           #
        #######################################################################
    else:
        raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

    # Store the updated running means back into bn_param
    bn_param['running_mean'] = running_mean
    bn_param['running_var'] = running_var

    return out, cache


def batchnorm_backward(dout, cache):
    """
    Backward pass for batch normalization.

    For this implementation, you should write out a computation graph for
    batch normalization on paper and propagate gradients backward through
    intermediate nodes.

    Inputs:
    - dout: Upstream derivatives, of shape (N, D)
    - cache: Variable of intermediates from batchnorm_forward.

    Returns a tuple of:
    - dx: Gradient with respect to inputs x, of shape (N, D)
    - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
    - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
    """
    dx, dgamma, dbeta = None, None, None
    ###########################################################################
    # TODO: Implement the backward pass for batch normalization. Store the    #
    # results in the dx, dgamma, and dbeta variables.                         #
    # Referencing the original paper (https://arxiv.org/abs/1502.03167)       #
    # might prove to be helpful.                                              #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    sample_mean, sample_variance, x, x_hat, beta, gamma, eps = cache
    N = np.shape(x)[0]
    # as in batch norm paper
    dx_hat  = dout * gamma # N,D
    dvar = np.sum (-0.5 * dx_hat * (x - sample_mean ) * ( sample_variance + 
                   eps ) ** (-3/2),axis = 0) # (D,)
    dmean = np.sum( -dx_hat * 1 / (np.sqrt(sample_variance + eps) ), axis = 0)\
    + dvar * (np.sum (-2 * (x - sample_mean), axis = 0 ) / N )#(D,)
    
    dx = dx_hat * ( 1 / (np.sqrt( sample_variance + eps ) ) ) + dvar * 2 * \
    (x - sample_mean) / N + dmean * 1 / N # N,D
    
    dgamma = np.sum( dout * x_hat , axis = 0) # D
    dbeta = np.sum (dout, axis = 0) # D
    

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def batchnorm_backward_alt(dout, cache):
    """
    Alternative backward pass for batch normalization.

    For this implementation you should work out the derivatives for the batch
    normalizaton backward pass on paper and simplify as much as possible. You
    should be able to derive a simple expression for the backward pass. 
    See the jupyter notebook for more hints.
     
    Note: This implementation should expect to receive the same cache variable
    as batchnorm_backward, but might not use all of the values in the cache.

    Inputs / outputs: Same as batchnorm_backward
    """
    dx, dgamma, dbeta = None, None, None
    ###########################################################################
    # TODO: Implement the backward pass for batch normalization. Store the    #
    # results in the dx, dgamma, and dbeta variables.                         #
    #                                                                         #
    # After computing the gradient with respect to the centered inputs, you   #
    # should be able to compute gradients with respect to the inputs in a     #
    # single statement; our implementation fits on a single 80-character line.#
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    
    sample_mean, sample_variance, x, x_hat, beta, gamma, eps = cache
    N = np.shape(x)[0]
    # as in batch norm paper
    dx_hat  = dout * gamma # N,D
    
    dgamma = np.sum( dout * x_hat , axis = 0) # D
    dbeta = np.sum (dout, axis = 0) # D

    dx = 1 / (N * np.sqrt(sample_variance + eps) ) * (N * dx_hat - \
             np.sum ( dx_hat , axis=0) - (x_hat - np.sum(x_hat, axis=0) )* \
             np.sum(dx_hat * x_hat, axis=0) ) 
    


    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def layernorm_forward(x, gamma, beta, ln_param):
    """
    Forward pass for layer normalization.

    During both training and test-time, the incoming data is normalized per data-point,
    before being scaled by gamma and beta parameters identical to that of batch normalization.
    
    Note that in contrast to batch normalization, the behavior during train and test-time for
    layer normalization are identical, and we do not need to keep track of running averages
    of any sort.

    Input:
    - x: Data of shape (N, D)
    - gamma: Scale parameter of shape (D,)
    - beta: Shift paremeter of shape (D,)
    - ln_param: Dictionary with the following keys:
        - eps: Constant for numeric stability

    Returns a tuple of:
    - out: of shape (N, D)
    - cache: A tuple of values needed in the backward pass
    """
    out, cache = None, None
    eps = ln_param.get('eps', 1e-5)
    ###########################################################################
    # TODO: Implement the training-time forward pass for layer norm.          #
    # Normalize the incoming data, and scale and  shift the normalized data   #
    #  using gamma and beta.                                                  #
    # HINT: this can be done by slightly modifying your training-time         #
    # implementation of  batch normalization, and inserting a line or two of  #
    # well-placed code. In particular, can you think of any matrix            #
    # transformations you could perform, that would enable you to copy over   #
    # the batch norm code and leave it almost unchanged?                      #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    # layer norm performs the same operations as batch norm but on a transposed 
    # version of the input - we can just reuse our code
    
    #batchnorm code expects dict "bn_param" with key "mode"
    ln_param['mode'] = 'train'
    ln_param['layer'] = 1
    out, cache = batchnorm_forward(x.T, gamma.reshape(-1,1), beta.reshape(-1,1),
                                   ln_param)
    out = out.T

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return out, cache


def layernorm_backward(dout, cache):
    """
    Backward pass for layer normalization.

    For this implementation, you can heavily rely on the work you've done already
    for batch normalization.

    Inputs:
    - dout: Upstream derivatives, of shape (N, D)
    - cache: Variable of intermediates from layernorm_forward.

    Returns a tuple of:
    - dx: Gradient with respect to inputs x, of shape (N, D)
    - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
    - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
    """
    dx, dgamma, dbeta = None, None, None
    ###########################################################################
    # TODO: Implement the backward pass for layer norm.                       #
    #                                                                         #
    # HINT: this can be done by slightly modifying your training-time         #
    # implementation of batch normalization. The hints to the forward pass    #
    # still apply!                                                            #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    
    # backward pass of layer norm is similar to backward pass of batch norm
    dx, _, _ = batchnorm_backward(dout.T, cache)
    
    # come back to the layer norm realm by transposing
    dx = dx.T
    
    # TODO: fix this
    # do the lazy thing instead of modifying batch norm code 
    _, _, _, x_hat, _,_, _ = cache
    dgamma = np.sum(dout * x_hat.T, axis = 0)
    dbeta = np.sum(dout, axis = 0)
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dgamma, dbeta


def dropout_forward(x, dropout_param):
    """
    Performs the forward pass for (inverted) dropout.

    Inputs:
    - x: Input data, of any shape
    - dropout_param: A dictionary with the following keys:
      - p: Dropout parameter. We keep each neuron output with probability p.
      - mode: 'test' or 'train'. If the mode is train, then perform dropout;
        if the mode is test, then just return the input.
      - seed: Seed for the random number generator. Passing seed makes this
        function deterministic, which is needed for gradient checking but not
        in real networks.

    Outputs:
    - out: Array of the same shape as x.
    - cache: tuple (dropout_param, mask). In training mode, mask is the dropout
      mask that was used to multiply the input; in test mode, mask is None.

    NOTE: Please implement **inverted** dropout, not the vanilla version of dropout.
    See http://cs231n.github.io/neural-networks-2/#reg for more details.

    NOTE 2: Keep in mind that p is the probability of **keep** a neuron
    output; this might be contrary to some sources, where it is referred to
    as the probability of dropping a neuron output.
    """
    p, mode = dropout_param['p'], dropout_param['mode']
    if 'seed' in dropout_param:
        np.random.seed(dropout_param['seed'])

    mask = None
    out = None

    if mode == 'train':
        #######################################################################
        # TODO: Implement training phase forward pass for inverted dropout.   #
        # Store the dropout mask in the mask variable.                        #
        #######################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        
        # keep neuron output with probability p
        mask = (np.random.rand(*x.shape) < p) / p
        out = mask * x
        

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        #######################################################################
        #                           END OF YOUR CODE                          #
        #######################################################################
    elif mode == 'test':
        #######################################################################
        # TODO: Implement the test phase forward pass for inverted dropout.   #
        #######################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        
        # We're using inverted dropout, so at test time, we do nothing.
        out = x

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        #######################################################################
        #                            END OF YOUR CODE                         #
        #######################################################################

    cache = (dropout_param, mask)
    out = out.astype(x.dtype, copy=False)

    return out, cache


def dropout_backward(dout, cache):
    """
    Perform the backward pass for (inverted) dropout.

    Inputs:
    - dout: Upstream derivatives, of any shape
    - cache: (dropout_param, mask) from dropout_forward.
    """
    dropout_param, mask = cache
    mode = dropout_param['mode']

    dx = None
    if mode == 'train':
        #######################################################################
        # TODO: Implement training phase backward pass for inverted dropout   #
        #######################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        dx = mask * dout

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        #######################################################################
        #                          END OF YOUR CODE                           #
        #######################################################################
    elif mode == 'test':
        dx = dout
    return dx


def conv_forward_naive(x, w, b, conv_param):
    """
    A naive implementation of the forward pass for a convolutional layer.

    The input consists of N data points, each with C channels, height H and
    width W. We convolve each input with F different filters, where each filter
    spans all C channels and has height HH and width WW.

    Input:
    - x: Input data of shape (N, C, H, W)
    - w: Filter weights of shape (F, C, HH, WW)
    - b: Biases, of shape (F,)
    - conv_param: A dictionary with the following keys:
      - 'stride': The number of pixels between adjacent receptive fields in the
        horizontal and vertical directions.
      - 'pad': The number of pixels that will be used to zero-pad the input. 
        

    During padding, 'pad' zeros should be placed symmetrically (i.e equally on both sides)
    along the height and width axes of the input. Be careful not to modfiy the original
    input x directly.

    Returns a tuple of:
    - out: Output data, of shape (N, F, H', W') where H' and W' are given by
      H' = 1 + (H + 2 * pad - HH) / stride
      W' = 1 + (W + 2 * pad - WW) / stride
    - cache: (x, w, b, conv_param)
    """
    out = None
    ###########################################################################
    # TODO: Implement the convolutional forward pass.                         #
    # Hint: you can use the function np.pad for padding.                      #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    
    N,C,H,W = np.shape(x)
    F,_,HH, WW = np.shape(w)

    pad_num = conv_param['pad']
    stride = conv_param['stride']
    
    # define output size - integer division since we need to pass this to np.zeros
    H_bar = 1 + (H + 2 * pad_num - HH)  // stride
    W_bar = 1 + (W + 2 * pad_num - WW ) // stride
    
    x_padded = np.pad(x, ((0,0), (0,0), (pad_num,pad_num), (pad_num,pad_num)), 
                      mode='constant',
                      constant_values=0)
    
    out = np.zeros( (N, F, H_bar, W_bar ) )
    
    # naiv-est(?) possbile loop
    for image in range(N):
        for f in range(F):
            for height in range(H_bar):
                
                h_start = height * stride
                h_end = height * stride + HH
                
                for width in range(W_bar):
                    w_start = width * stride
                    w_end = width * stride + WW
                    
                    out[image,f,height,width] = np.sum (
                            x_padded[image, :, h_start:h_end, w_start:w_end] * \
                            w[f, :, :, : ] ) + b[f]
                    


    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, w, b, conv_param)
    return out, cache


def conv_backward_naive(dout, cache):
    """
    A naive implementation of the backward pass for a convolutional layer.

    Inputs:
    - dout: Upstream derivatives.
    - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

    Returns a tuple of:
    - dx: Gradient with respect to x
    - dw: Gradient with respect to w
    - db: Gradient with respect to b
    """
    dx, dw, db = None, None, None
    ###########################################################################
    # TODO: Implement the convolutional backward pass.                        #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    from scipy import signal 
    
    x,w,b,conv_param = cache
    
    N,C,H,W = np.shape(x)
    F,_,HH, WW = np.shape(w)
    _, _, H_bar, W_bar = np.shape(dout)
    
    pad_num = conv_param['pad']
    stride = conv_param['stride']
    
    H_bar = 1 + (H + 2 * pad_num - HH)  // stride
    W_bar = 1 + (W + 2 * pad_num - WW ) // stride
    
    # db is just a sum
    db = np.sum(dout, axis=(0,2,3))
    
    # dw - naiver than naive
    x_padded = np.pad(x, ((0,0), (0,0), (pad_num,pad_num), (pad_num,pad_num)), 
                  mode='constant',
                  constant_values=0)
    
    dw = np.zeros( np.shape(w) )
    dx_padded = np.zeros( np.shape(x_padded) )
    
    for f in range(F):
        
        for image in range(N):
            
            # 2d dout
            #dout_part = dout[image,f,:,:]
            
            for height in range(H_bar):
                
                h_start = height * stride
                h_end = height * stride + HH
                
                for width in range(W_bar):
                    w_start = width * stride
                    w_end = width * stride + WW
                    
                    dw[f] += x_padded[image, :, h_start:h_end, w_start:w_end] *\
                    dout[image, f, height, width]
                    
                    dx_padded[image, :, h_start:h_end, w_start:w_end] += w[f] * \
                    dout[image, f, height, width]

    dx = dx_padded[:, :, pad_num:pad_num+H, pad_num:pad_num+W]
                    
    
    """
    for c in range(C):
        dw[f,c, height, width] += np.sum (
                x_padded[image,c, h_start:h_end, w_start:w_end ] * \
        dout_part)
        
        dx[]
    """    

    #dx full convolution
    """
    dout_padded = np.pad( dout, 
                     ((0,0), (0,0), (HH-1,HH-1), (WW-1,WW-1)),
                     mode='constant',
                     constant_values=0 )
    
    dx = np.zeros( np.shape(x) )
    
    for image in range(N):
        for f in range(F):
            
            for c in range(C):
                
                dw_rev = np.flip( w[f,c,:,:] )
                
                for height in range(H):
                    h_start = height
                    h_end = height + HH
                    
                    for width in range(W):
                        w_start = width
                        w_end = width + WW
                        
                        
                        dx[image, c, height, width ] += np.sum ( 
                               dout_padded[image, f, h_start:h_end, w_start:w_end] * \
                               dw_rev )
                        
    """           


    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dw, db


def max_pool_forward_naive(x, pool_param):
    """
    A naive implementation of the forward pass for a max-pooling layer.

    Inputs:
    - x: Input data, of shape (N, C, H, W)
    - pool_param: dictionary with the following keys:
      - 'pool_height': The height of each pooling region
      - 'pool_width': The width of each pooling region
      - 'stride': The distance between adjacent pooling regions

    No padding is necessary here. Output size is given by 

    Returns a tuple of:
    - out: Output data, of shape (N, C, H', W') where H' and W' are given by
      H' = 1 + (H - pool_height) / stride
      W' = 1 + (W - pool_width) / stride
    - cache: (x, pool_param)
    """
    out = None
    ###########################################################################
    # TODO: Implement the max-pooling forward pass                            #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    N,C,H,W = np.shape(x)
    
    pool_width = pool_param['pool_width']
    pool_height = pool_param['pool_height']
    stride  = pool_param['stride']
    
    H_bar = 1 + (H - pool_height) // stride
    W_bar = 1 + (W - pool_width) // stride
    
    out = np.zeros ( ( N, C, H_bar, W_bar ) )
    
    for image in range(N):
        for height in range(H_bar):
            h_start = height * stride
            h_end = height * stride + pool_height
            
            for width in range(W_bar):
                
                w_start = width * stride
                w_end = width * stride + pool_width
                
                out[image, :, height, width] = np.max( 
                        x[image, :, h_start:h_end, w_start:w_end], axis=(1,2) )
    

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, pool_param)
    return out, cache


def max_pool_backward_naive(dout, cache):
    """
    A naive implementation of the backward pass for a max-pooling layer.

    Inputs:
    - dout: Upstream derivatives
    - cache: A tuple of (x, pool_param) as in the forward pass.

    Returns:
    - dx: Gradient with respect to x
    """
    dx = None
    ###########################################################################
    # TODO: Implement the max-pooling backward pass                           #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    
    x,pool_param = cache
    
    N, C, H, W = np.shape(x)
    _, _, H_bar, W_bar = np.shape(dout)

    pool_width = pool_param['pool_width']
    pool_height = pool_param['pool_height']
    stride  = pool_param['stride']
    
    dx = np.zeros(np.shape(x))
    for image in range(N):
        for height in range(H_bar):
            
            h_start = height * stride
            h_end = height * stride + pool_height
            
            for width in range(W_bar):
                w_start = width * stride
                w_end = width * stride + pool_width
                
                x_sub = x[image, :, h_start:h_end, w_start:w_end]
                x_max = np.max (x_sub, axis =(1,2))
                
                # expand dims to enable broadcasting
                x_max = x_max[:, np.newaxis, np.newaxis]
                mask = (x_sub == x_max)
                
                out = dout[image, :, height, width]
                #prepare for broadcasting
                out = out[:, np.newaxis, np.newaxis]
                
                dx[image, :, h_start:h_end, w_start:w_end] = \
                 out * mask

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx


def spatial_batchnorm_forward(x, gamma, beta, bn_param):
    """
    Computes the forward pass for spatial batch normalization.

    Inputs:
    - x: Input data of shape (N, C, H, W)
    - gamma: Scale parameter, of shape (C,)
    - beta: Shift parameter, of shape (C,)
    - bn_param: Dictionary with the following keys:
      - mode: 'train' or 'test'; required
      - eps: Constant for numeric stability
      - momentum: Constant for running mean / variance. momentum=0 means that
        old information is discarded completely at every time step, while
        momentum=1 means that new information is never incorporated. The
        default of momentum=0.9 should work well in most situations.
      - running_mean: Array of shape (D,) giving running mean of features
      - running_var Array of shape (D,) giving running variance of features

    Returns a tuple of:
    - out: Output data, of shape (N, C, H, W)
    - cache: Values needed for the backward pass
    """
    out, cache = None, None

    ###########################################################################
    # TODO: Implement the forward pass for spatial batch normalization.       #
    #                                                                         #
    # HINT: You can implement spatial batch normalization by calling the      #
    # vanilla version of batch normalization you implemented above.           #
    # Your implementation should be very short; ours is less than five lines. #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****    
    
    # compute mean and variance across examples and spatial dimensions
    # for each feature map
    N, C, H, W = np.shape(x)
    x_batch = np.transpose(x, ( 0, 2, 3, 1) )
    x_batch = x_batch.reshape(-1, C )
    out, cache = batchnorm_forward(x_batch, gamma, beta, bn_param )
    out = ( out.reshape( N, H, W , C) ).transpose(0,3,1,2)
    
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return out, cache


def spatial_batchnorm_backward(dout, cache):
    """
    Computes the backward pass for spatial batch normalization.

    Inputs:
    - dout: Upstream derivatives, of shape (N, C, H, W)
    - cache: Values from the forward pass

    Returns a tuple of:
    - dx: Gradient with respect to inputs, of shape (N, C, H, W)
    - dgamma: Gradient with respect to scale parameter, of shape (C,)
    - dbeta: Gradient with respect to shift parameter, of shape (C,)
    """
    dx, dgamma, dbeta = None, None, None

    ###########################################################################
    # TODO: Implement the backward pass for spatial batch normalization.      #
    #                                                                         #
    # HINT: You can implement spatial batch normalization by calling the      #
    # vanilla version of batch normalization you implemented above.           #
    # Your implementation should be very short; ours is less than five lines. #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    N,C,H,W = dout.shape
    dout = ( dout.transpose(0,2,3,1) ).reshape( -1 , C)
    dx, dgamma, dbeta = batchnorm_backward( dout, cache )
    dx = ( dx.reshape( N, H, W, C ) ).transpose(0,3,1,2)
    
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def spatial_groupnorm_forward(x, gamma, beta, G, gn_param):
    """
    Computes the forward pass for spatial group normalization.
    In contrast to layer normalization, group normalization splits each entry 
    in the data into G contiguous pieces, which it then normalizes independently.
    Per feature shifting and scaling are then applied to the data, in a manner identical to that of batch normalization and layer normalization.

    Inputs:
    - x: Input data of shape (N, C, H, W)
    - gamma: Scale parameter, of shape (C,)
    - beta: Shift parameter, of shape (C,)
    - G: Integer mumber of groups to split into, should be a divisor of C
    - gn_param: Dictionary with the following keys:
      - eps: Constant for numeric stability

    Returns a tuple of:
    - out: Output data, of shape (N, C, H, W)
    - cache: Values needed for the backward pass
    """
    out, cache = None, None
    eps = gn_param.get('eps',1e-5)
    ###########################################################################
    # TODO: Implement the forward pass for spatial group normalization.       #
    # This will be extremely similar to the layer norm implementation.        #
    # In particular, think about how you could transform the matrix so that   #
    # the bulk of the code is similar to both train-time batch normalization  #
    # and layer normalization!                                                # 
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    N, C , H , W = np.shape(x)
    
    # from group norm paper
    x_group = x.reshape(N, G, C // G, H, W)
    mean = np.mean(x_group, axis=(2,3,4), keepdims=True)
    variance = np.var (x_group, axis=(2,3,4), keepdims=True)
    
    x_group = ( x_group - mean ) / ( np.sqrt ( variance + eps ) ) 
    
    x_group = np.reshape (x_group, (N, C, H, W) )
    
    out = gamma.reshape( 1, -1, 1, 1) * x_group + beta.reshape( 1, -1, 1, 1)
    
    cache = (mean, variance, x, x_group, gamma, beta, G, eps)
    

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return out, cache


def spatial_groupnorm_backward(dout, cache):
    """
    Computes the backward pass for spatial group normalization.

    Inputs:
    - dout: Upstream derivatives, of shape (N, C, H, W)
    - cache: Values from the forward pass

    Returns a tuple of:
    - dx: Gradient with respect to inputs, of shape (N, C, H, W)
    - dgamma: Gradient with respect to scale parameter, of shape (1,C,1,1)
    - dbeta: Gradient with respect to shift parameter, of shape (1,C,1,1)
    
    Note: The ipython notebook provided by CS 231n expect dgamma and dbeta to
    be of the shape (1,C,1,1) which is why this function returns dgamma and 
    dbeta in that shape. The original function docstring said that dgamma 
    and dbeta are of the shape (C,)
    """
    dx, dgamma, dbeta = None, None, None

    ###########################################################################
    # TODO: Implement the backward pass for spatial group normalization.      #
    # This will be extremely similar to the layer norm implementation.        #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    
    mean, variance, x, x_group, beta, gamma, G, eps = cache
    
    # dgamma and dbeta as in batch norm
    dgamma = np.sum( dout * x_group , axis=(0,2,3), keepdims=True )
    dbeta = np.sum(dout, axis=(0,2,3), keepdims=True)
    
    N,C,H,W = np.shape(x)
    
    # we can now just follow the batch norm paper taking care to sum over the 
    # right dimensions
    dx_group = dout * gamma
    dx_group = dx_group.reshape(N, G, C//G, H, W)
    
    x_input = x.reshape( N, G, C//G, H, W)
    
    x_minus_mean = x_input - mean
    second_dim = (C//G) * H * W
    
    dvar = np.sum( dx_group * ( x_minus_mean ) * -0.5 * ( variance + eps )** (-3/2 ), 
                  axis=(2,3,4), keepdims=True)
    
    dmean = np.sum ( dx_group * -1 / (np.sqrt( variance+eps ) ), 
                    axis=(2,3,4),keepdims=True  ) + dvar * (np.sum ( -2 * x_minus_mean 
                         , axis=(2,3,4), keepdims=True ) ) / second_dim 
    
    dx = dx_group * 1 / ( np.sqrt(variance + eps ) ) + dvar * 2 * (x_minus_mean) / \
    second_dim + dmean * 1 / second_dim
    
    dx = dx.reshape(N, C, H, W)
    
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dgamma, dbeta


def svm_loss(x, y):
    """
    Computes the loss and gradient using for multiclass SVM classification.

    Inputs:
    - x: Input data, of shape (N, C) where x[i, j] is the score for the jth
      class for the ith input.
    - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
      0 <= y[i] < C

    Returns a tuple of:
    - loss: Scalar giving the loss
    - dx: Gradient of the loss with respect to x
    """
    N = x.shape[0]
    correct_class_scores = x[np.arange(N), y]
    margins = np.maximum(0, x - correct_class_scores[:, np.newaxis] + 1.0)
    margins[np.arange(N), y] = 0
    loss = np.sum(margins) / N
    num_pos = np.sum(margins > 0, axis=1)
    dx = np.zeros_like(x)
    dx[margins > 0] = 1
    dx[np.arange(N), y] -= num_pos
    dx /= N
    return loss, dx


def softmax_loss(x, y):
    """
    Computes the loss and gradient for softmax classification.

    Inputs:
    - x: Input data, of shape (N, C) where x[i, j] is the score for the jth
      class for the ith input.
    - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
      0 <= y[i] < C

    Returns a tuple of:
    - loss: Scalar giving the loss
    - dx: Gradient of the loss with respect to x
    """
    shifted_logits = x - np.max(x, axis=1, keepdims=True)
    Z = np.sum(np.exp(shifted_logits), axis=1, keepdims=True)
    log_probs = shifted_logits - np.log(Z)
    probs = np.exp(log_probs)
    N = x.shape[0]
    loss = -np.sum(log_probs[np.arange(N), y]) / N
    dx = probs.copy()
    dx[np.arange(N), y] -= 1
    dx /= N
    return loss, dx

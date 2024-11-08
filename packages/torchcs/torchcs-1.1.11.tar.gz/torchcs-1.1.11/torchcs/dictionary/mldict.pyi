def weights_init(m):
    ...

class DictLayer(th.nn.Module):
    ...

    def __init__(self, n=1024):
        ...

    def forward(self, x):
        ...

class DictNet(object):
    r"""Neural network for dictionary learning

    Parameters
    ----------
    cin : int, optional
        the number of channels of input signal, by default 1
    lr : float, optional
        learning rate, by default 0.1
    seed : int or None, optional
        random seed for weight initialization, by default None (not set)
    device : str, optional
        computation device, ``'cuda:x'`` or ``'cpu'`` by default ``'cpu'``
    """        

    def __init__(self, n=1, lr=0.1, seed=None, device='cpu'):
        ...

    def get_dict(self):
        ...

    def dictt(self, x):
        ...

    def idictt(self, x):
        ...

    def train(self, Xtrain, Ytrain, Xvalid, Yvalid, bs, nepoch):
        r"""train

        Parameters
        ----------
        Xtrain : tensor
            target for training
        Ytrain : tensor
            input for training, :math:`N\times C\times L`
        Xvalid : tensor
            target for validation
        Yvalid : tensor
            input for validation
        bs : int
            batch size
        nepoch : int
            the number of epochs
        """        

    def test(self, X, bs):
        r"""test

        Parameters
        ----------
        X :  tensor
             input for testing, :math:`N\times C\times L`

        bs :  int
             batch size

        Returns
        -------
         tensor
             recovered signals
        """        

    def save(self, modelfile):
        r"""save network model to a file

        Parameters
        ----------
        modelfile :  str
             model file path
        """        

    def load(self, modelfile):
        r"""load network model from a file

        Parameters
        ----------
        modelfile :  str
             model file path
        """        



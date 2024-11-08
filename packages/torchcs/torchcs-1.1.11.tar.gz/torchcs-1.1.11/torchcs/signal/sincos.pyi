def sinwave(N, Fr=[1, 100], Ar=[1, 5], Pr=[0, tb.PI], Fs=1e3, Ts=1., seed=None):
    r"""generates rectangular pulse

    Parameters
    ----------
    N : int, optional
        the number of waves
    Fr : list, optional
        the range of frequency, by default [1, 100]
    Ar : list, optional
        the range of amplitudes, by default [1, 4]
    Pr : list, optional
        the range of initial phase, by default [0, pi]
    Fs : float, optional
        the sampling frequency, by default 1e3
    Ts : float, optional
        the sampling duration, by default 1.
    seed : int or None, optional
        the seed for random number generator, by default None

    Returns
    -------
    tensor
        generated signal tensor (:math:`N_s\times 1`)

    Examples
    ---------

    .. image:: ./_static/Demosinwave.png
       :scale: 80 %
       :align: center

    The results shown in the above figure can be obtained by the following codes.

    ::
        
        import torchbox as tb
        import matplotlib.pyplot as plt

        x = tb.sinwave(1, seed=2023)

        plt.figure()
        plt.grid()
        plt.plot(x, '-b')
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.show()

    """



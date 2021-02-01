import numpy as np

from scipy import linalg
from scipy.sparse import issparse
from scipy.sparse.linalg import eigs


def spectral_radius(W):
    """Given a squarred weight matrix (e.g. the recurrent reservoir matrix),
    returns the spectral radius"""
    if issparse(W):
        return max(abs(eigs(W,
                            k=1,
                            which='LM',
                            maxiter=W.shape[0] * 20,
                            return_eigenvectors=False)))
    return max(abs(linalg.eig(W)[0]))


def compute_error_NRMSE(teacher_signal, predicted_signal, verbose=False):
    """ Computes Normalized Root-Mean-Squarred Error between a teacher signal and a predicted signal
    Return the errors in this order: nmrse mean, nmrse max-min, rmse, mse.
    By default, only NMRSE mean should be considered as a general measure to be
    compared for different datasets.

    For more information, see:
    - Mean Squared Error https://en.wikipedia.org/wiki/Mean_squared_error
    - Root Mean Squared Error https://en.wikipedia.org/wiki/Root-mean-square_deviation for more info
    """
    errorLen = len(predicted_signal[:])
    mse = np.mean((teacher_signal - predicted_signal)**2)
    rmse = np.sqrt(mse)
    nmrse_mean = abs(rmse / np.mean(predicted_signal[:])) # Normalised RMSE (based on mean)
    nmrse_maxmin = rmse / abs(np.max(predicted_signal[:]) - np.min(predicted_signal[:])) # Normalised RMSE (based on max - min)
    if verbose:
        print("Errors computed over %d time steps" % (errorLen))
        print("\nMean Squared error (MSE):\t\t%.4e" % (mse) )
        print("Root Mean Squared error (RMSE):\t\t%.4e\n" % rmse )
        print("Normalized RMSE (based on mean):\t%.4e" % (nmrse_mean) )
        print("Normalized RMSE (based on max - min):\t%.4e" % (nmrse_maxmin) )
    return nmrse_mean, nmrse_maxmin, rmse, mse

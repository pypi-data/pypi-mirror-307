import scipy.io as sio


def load_mat(filename):
    """
    Load .mat file and return a dictionary with variable names as keys, and loaded matrices as values.
    """
    return sio.loadmat(filename)


def save_mat(filename, varname, data):
    """
    Save data to .mat file with the given variable name.
    """
    sio.savemat(filename, {varname: data})

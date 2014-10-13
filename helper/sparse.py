from scipy import sparse

def build_sparse_matrix(sparse_X):
    """Build n_samples x n_features matrix out of list of n_samples vectors."""
    X = sparse_X[0]

    for x in sparse_X[1:]:
        # Append row x from the bottom
        X = sparse.vstack((X, x))

    return X

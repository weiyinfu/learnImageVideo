import numpy as np


def regular_grid(ar_shape, n_points):
    """Find `n_points` regularly spaced along `ar_shape`.

    The returned points (as slices) should be as close to cubically-spaced as
    possible. Essentially, the points are spaced by the Nth root of the input
    array size, where N is the number of dimensions. However, if an array
    dimension cannot fit a full step size, it is "discarded", and the
    computation is done for only the remaining dimensions.

    Parameters
    ----------
    ar_shape : array-like of ints
        The shape of the space embedding the grid. ``len(ar_shape)`` is the
        number of dimensions.
    n_points : int
        The (approximate) number of points to embed in the space.

    Returns
    -------
    slices : list of slice objects
        A slice along each dimension of `ar_shape`, such that the intersection
        of all the slices give the coordinates of regularly spaced points.

    Examples
    --------
    >>> ar = np.zeros((20, 40))
    >>> g = regular_grid(ar.shape, 8)
    >>> g
    [slice(5, None, 10), slice(5, None, 10)]
    >>> ar[g] = 1
    >>> ar.sum()
    8.0
    >>> ar = np.zeros((20, 40))
    >>> g = regular_grid(ar.shape, 32)
    >>> g
    [slice(2, None, 5), slice(2, None, 5)]
    >>> ar[g] = 1
    >>> ar.sum()
    32.0
    >>> ar = np.zeros((3, 20, 40))
    >>> g = regular_grid(ar.shape, 8)
    >>> g
    [slice(1, None, 3), slice(5, None, 10), slice(5, None, 10)]
    >>> ar[g] = 1
    >>> ar.sum()
    8.0
    """
    ar_shape = np.asanyarray(ar_shape)
    ndim = len(ar_shape)
    unsort_dim_idxs = np.argsort(np.argsort(ar_shape))
    sorted_dims = np.sort(ar_shape)
    space_size = float(np.prod(ar_shape))
    if space_size <= n_points:
        return [slice(None)] * ndim
    stepsizes = (space_size / n_points) ** (1.0 / ndim) * np.ones(ndim)
    if (sorted_dims < stepsizes).any():
        for dim in range(ndim):
            stepsizes[dim] = sorted_dims[dim]
            space_size = float(np.prod(sorted_dims[dim + 1:]))
            stepsizes[dim + 1:] = ((space_size / n_points) **
                                   (1.0 / (ndim - dim - 1)))
            if (sorted_dims >= stepsizes).all():
                break
    starts = (stepsizes // 2).astype(int)
    stepsizes = np.round(stepsizes).astype(int)
    slices = [slice(start, None, step) for
              start, step in zip(starts, stepsizes)]
    slices = [slices[i] for i in unsort_dim_idxs]
    return slices

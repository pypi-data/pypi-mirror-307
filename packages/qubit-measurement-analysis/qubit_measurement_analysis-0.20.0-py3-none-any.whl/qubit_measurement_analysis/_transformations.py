def _add(array, other):
    return array + other


def _sub(array, other):
    return array - other


def _mul(array, other):
    return array * other


def _div(array, other):
    return array / other


def _mean(array, axis):
    return array.mean(axis, keepdims=True)


def _mean_filter(array, k, module):
    p = array.shape[-1]
    diag_offset = module.np.linspace(-(k // 2), k // 2, k, dtype=int)
    sparse_matrix = module.scipy.sparse.diags(
        module.np.ones((k, p)), offsets=diag_offset, shape=(p, p)
    ).toarray()
    nrmlize = module.np.ones_like(array) @ sparse_matrix
    new_array = (array @ sparse_matrix) / nrmlize
    return new_array


def _mean_convolve(array, kernel_size, stride, module):
    kernel = module.np.ones(kernel_size) / kernel_size
    kernel = kernel.reshape(1, 1, -1) if array.ndim == 3 else kernel.reshape(1, -1)
    return module.scipy.signal.fftconvolve(array, kernel, mode="valid", axes=-1)[
        ..., ::stride
    ]


def _whittaker_eilers_smoother(signals, lamb, d, module):
    # Handle different input shapes
    if signals.ndim == 2:
        signals = signals[module.newaxis, :, :]  # Reshape to (1, number_channels, len)

    batch_size, number_channels, signal_len = signals.shape

    # Create the difference matrix (D)
    D = module.scipy.sparse.eye(signal_len, format="csc")
    for _ in range(d):
        D = D[1:] - D[:-1]

    # Regularization matrix (penalizing large differences in the second derivative)
    DTD = D.T @ D

    # Construct the smoother matrix (I + λ * D^T * D)
    smoother_matrix = module.scipy.sparse.eye(signal_len, format="csc") + lamb * DTD

    # Make sure it's in the right format (sparse)
    smoother_matrix = smoother_matrix.tocsc()

    # Solve for each signal in the batch and each channel
    smoothed_signals = module.zeros_like(signals)
    for i in range(batch_size):
        for j in range(number_channels):
            smoothed_signals[i, j] = module.scipy.sparse.linalg.spsolve(
                smoother_matrix, signals[i, j]
            )

    if signals.shape[0] == 1:  # No batch input, just multiple channels
        return smoothed_signals[0]
    return smoothed_signals


def _mean_centring(array, axis=-1):
    return array - array.mean(axis=axis, keepdims=True)


def _normalize(array, axis=-1):
    min_array = array.min(axis=axis, keepdims=True)
    max_array = array.max(axis=axis, keepdims=True)
    normalized = (array - min_array) / (max_array - min_array)
    return normalized


def _standardize(array, axis=-1):
    std_real = array.real.std(axis=axis, keepdims=True)
    std_imag = array.imag.std(axis=axis, keepdims=True)
    standardized = (array - array.mean(axis=axis, keepdims=True)) / (
        std_real + std_imag * 1j
    )
    return standardized


def _demodulate(array, intermediate_freq, meas_time, direction, module):
    # Calculate phase using broadcasting
    phase = 2 * module.pi * intermediate_freq @ meas_time
    # Calculate rotation using broadcasting
    rotation = (
        module.exp(-1j * phase) if direction == "clockwise" else module.exp(1j * phase)
    )
    # Perform the rotation on the array
    demodulated = array * rotation
    return demodulated

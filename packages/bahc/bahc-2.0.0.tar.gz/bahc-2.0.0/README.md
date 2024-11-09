# BAHC

BAHC (Bootstrap Aggregated Hierarchical Clustering) is a Python package for filtering covariance matrices using hierarchical clustering and bootstrap aggregation.

## Installation

To install the package, you can use pip:

```sh
pip install bahc
```

Alternatively, you can clone the repository and install the dependencies manually:

```sh
git clone https://github.com/yourusername/bahc.git
cd bahc
pip install -r requirements.txt
```

## Usage

Here is an example of how to use the BAHC class:

```python
import numpy as np
from bahc import BAHC

# Generate random data
data = np.random.normal(0, 1, size=(10, 100))

# Create an instance of BAHC and filter the data
bahc_instance = BAHC(data, K=[1, 2, 3], Nboot=100, method='near', filter_type='correlation')

# Print the filtered matrix
print(bahc_instance.filtered_matrix)
```

## Methods

### `BAHC.__init__(self, data, K=1, Nboot=100, method='near', filter_type='covariance')`

Initializes the BAHC class and performs the filtering.

- `data` (ndarray): Data matrix (N x T).
- `K` (int or list): Recursion order.
- `Nboot` (int): Number of bootstraps.
- `method` (str): Regularization method ('no-neg' or 'near').
- `filter_type` (str): Type of filtering ('correlation' or 'covariance').

### `BAHC.filter_matrix(self)`

Filters the matrix using k-BAHC.

- Returns: Filtered matrix (N x N). If K is a list, returns a list of matrices.

### `BAHC.nearest_positive_semidefinite(self, matrix, n_iter=100, eig_tol=1e-6, conv_tol=1e-8)`

Finds the nearest positive semidefinite matrix.

- `matrix` (ndarray): Input matrix.
- `n_iter` (int): Maximum number of iterations.
- `eig_tol` (float): Eigenvalue tolerance.
- `conv_tol` (float): Convergence tolerance.
- Returns: Nearest positive semidefinite matrix.

### `BAHC.higher_order_covariance(self, C, K)`

Computes higher order covariance matrices.

- `C` (ndarray): Input covariance matrix.
- `K` (list): List of recursion orders.
- Yields: Higher order covariance matrices.

### `BAHC.generate_noise(self, N, T, epsilon=1e-10)`

Generates noise for the given dimensions.

- `N` (int): Number of rows.
- `T` (int): Number of columns.
- `epsilon` (float): Standard deviation of the noise.
- Returns: Generated noise matrix.

### `BAHC.remove_negative_eigenvalues(self, matrix)`

Removes negative eigenvalues from the matrix.

- `matrix` (ndarray): Input matrix.
- Returns: Matrix with non-negative eigenvalues.

## References

- Bongiorno, C., & Challet, D. (2021). Covariance matrix filtering with bootstrapped hierarchies. PLoS ONE, 16(1), e0245092.
- Bongiorno, C., & Challet, D. (2022). Reactive global minimum variance portfolios with k-BAHC covariance cleaning. The European Journal of Finance, 28(13-15), 1344-1360.

Please cite the above papers if you use this code.

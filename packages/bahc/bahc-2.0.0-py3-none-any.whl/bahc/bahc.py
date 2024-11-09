import numpy as np
from scipy.cluster.hierarchy import average, cophenet
from scipy.spatial.distance import squareform
from statsmodels.stats.correlation_tools import cov_nearest
import random

class BAHC:
    def __init__(self, data, K=1, Nboot=100, method='near', filter_type='covariance'):
        """
        Initializes the BAHC class and performs the filtering.

        Parameters:
        data (ndarray): Data matrix (N x T).
        K (int or list): Recursion order.
            - K=1: Uses the basic BAHC method as described in Bongiorno & Challet (2021).
            - K>1: Uses the k-BAHC method as described in Bongiorno & Challet (2022).
        Nboot (int): Number of bootstraps.
        method (str): Regularization method ('no-neg' or 'near').
        filter_type (str): Type of filtering ('correlation' or 'covariance').

        Notes:
        - For the basic BAHC method, see:
          Bongiorno, C., & Challet, D. (2021). Covariance matrix filtering with bootstrapped hierarchies.
          PLoS ONE, 16(1), e0245092.
        - For the k-BAHC method, see:
          Bongiorno, C., & Challet, D. (2022). Reactive global minimum variance portfolios with k-BAHC covariance cleaning.
          The European Journal of Finance, 28(13-15), 1344-1360.
        - Please cite the above papers if you use this code.
        """
        self.data = data
        self.K = K if isinstance(K, list) else [K]
        self.Nboot = Nboot
        self.method = method
        self.filter_type = filter_type
        self.regularization_methods = {'no-neg': self.remove_negative_eigenvalues, 'near': cov_nearest}
        self.N, self.T = data.shape
        self.std_devs = data.std(axis=1)
        self.filtered_matrix = self.filter_matrix()

    def filter_matrix(self, R):
        """
        Filters the input matrix using hierarchical clustering.

        Parameters:
        R (ndarray): Input matrix.

        Returns:
        ndarray: Filtered matrix.
        """
        distance = R[np.triu_indices(R.shape[0], 1)]
        dendrogram = average(distance)
        return 1 - squareform(cophenet(dendrogram))

    def generate_noise(self, N, T, epsilon=1e-10):
        """
        Generates noise for the given dimensions.

        Parameters:
        N (int): Number of rows.
        T (int): Number of columns.
        epsilon (float): Standard deviation of the noise.

        Returns:
        ndarray: Generated noise matrix.
        """
        return np.random.normal(0, epsilon, size=(N, T))

    def remove_negative_eigenvalues(self, matrix):
        """
        Removes negative eigenvalues from the matrix.

        Parameters:
        matrix (ndarray): Input matrix.

        Returns:
        ndarray: Matrix with non-negative eigenvalues.
        """
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)
        positive_indices = eigenvalues > 0
        eigenvalues, eigenvectors = eigenvalues[positive_indices], eigenvectors[:, positive_indices]
        return np.dot(eigenvectors * eigenvalues, eigenvectors.T)

    def nearest_positive_semidefinite(self, matrix, n_iter=100, eig_tol=1e-6, conv_tol=1e-8):
        """
        Finds the nearest positive semidefinite matrix.

        Parameters:
        matrix (ndarray): Input matrix.
        n_iter (int): Maximum number of iterations.
        eig_tol (float): Eigenvalue tolerance.
        conv_tol (float): Convergence tolerance.

        Returns:
        ndarray: Nearest positive semidefinite matrix.
        """
        D = np.zeros(matrix.shape)
        diag = matrix.diagonal()

        for _ in range(n_iter):
            y = matrix
            R = matrix - D
            matrix = self.remove_negative_eigenvalues(R)
            D = matrix - R
            np.fill_diagonal(matrix, diag)
            
            # Check for convergence
            if np.linalg.norm(matrix - y, ord=np.inf) / np.linalg.norm(y, ord=np.inf) < conv_tol:
                break
        else:
            print("Convergence not achieved")
        return matrix

    def higher_order_covariance(self, C, K):
        """
        Computes higher order covariance matrices.

        Parameters:
        C (ndarray): Input covariance matrix.
        K (list): List of recursion orders.

        Yields:
        ndarray: Higher order covariance matrices.
        """
        Cf = np.identity(C.shape[0])
        for i in range(max(K)):
            res = C - Cf
            res = self.filter_matrix(1 - res)
            np.fill_diagonal(res, 0)
            Cf += res
            if i + 1 in K:
                yield Cf.copy()

    def filter_matrix(self):
        """
        Filters the matrix using k-BAHC.

        Returns:
        ndarray: Filtered matrix (N x N). If K is a list, returns a list of matrices.
        """
        noise_matrix = self.generate_noise(self.N, self.T)
        C = np.zeros((len(self.K), self.N, self.N))

        if self.Nboot == 0:
            # Compute the correlation matrix
            Cb = np.corrcoef(self.data)
            # Apply regularization and higher order filtering
            C = np.array(list(map(self.regularization_methods[self.method], np.array(list(self.higher_order_covariance(Cb, self.K))))))
            if self.filter_type == 'covariance':
                C *= np.outer(self.std_devs, self.std_devs)
            return C[0] if len(self.K) == 1 else C

        for _ in range(self.Nboot):
            # Generate bootstrap samples with noise
            bootstrap_sample = self.data[:, random.choices(range(self.T), k=self.T)] + noise_matrix
            # Compute the correlation matrix
            Cb = np.corrcoef(bootstrap_sample)
            # Apply regularization and higher order filtering
            C += np.array(list(map(self.regularization_methods[self.method], np.array(list(self.higher_order_covariance(Cb, self.K))))))

        if self.filter_type == 'covariance':
            C = (C / self.Nboot) * np.outer(self.std_devs, self.std_devs)
        else:
            C /= self.Nboot

        return C[0] if len(self.K) == 1 else C

if __name__ == '__main__':
    # Generate random data
    x = np.random.normal(0, 1, size=(10, 100))
    # Create an instance of CovarianceFilter and filter the data
    filter_instance = BAHC(x, K=[1,2,3], Nboot=100, method='near', filter_type='correlation')
    # Print the filtered matrix
    print(filter_instance.filtered_matrix)
import numpy as np
from scipy.cluster.hierarchy import average, cophenet
from scipy.spatial.distance import squareform
from statsmodels.stats.correlation_tools import cov_nearest
import random
import timeit

class BAHC:
    def __init__(self, data, K=1, Nboot=100, method='near', filter_type='covariance', seed=None):
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
        seed (int): Random seed.

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
        self.regularization_methods = {'no-neg': self._remove_negative_eigenvalues, 'near': cov_nearest}
        self.N, self.T = data.shape
        self.std_devs = data.std(axis=1)
        self.rng = np.random.default_rng(seed)
        self.indices = np.triu_indices(self.N, 1)
        self.observations =  list(range(self.T))
    

    def _shift_dendrogram(self,dendrogram):
        """
        Adjusts the dendrogram to ensure all values in the third column are non-negative.
        This function shifts the values in the third column of the dendrogram such that the minimum value becomes zero.
        If the minimum value is already non-negative, no shift is applied.
        Parameters:
        dendrogram (numpy.ndarray): A 2D array representing the dendrogram, where the third column contains the values to be adjusted.
        Returns:
        tuple: A tuple containing the adjusted dendrogram and the offset value used for the shift.
        """
        
        if dendrogram[:,2].min()<0:
            offset_value = dendrogram[:,2].min()
            dendrogram[:,2] = dendrogram[:,2] - offset_value
        else:
            offset_value = 0
        return dendrogram-offset_value,offset_value

    def _hierarchical_cleaning(self, R):
        """
        Filters the input matrix using hierarchical clustering.

        Parameters:
        R (ndarray): Input matrix.

        Returns:
        ndarray: Filtered matrix.
        """
        distance = R[self.indices]
        dendrogram = average(distance)
        
        dendrogram,offset_value = self._shift_dendrogram(dendrogram)
        
        return 1 - (squareform(cophenet(dendrogram)+offset_value))


    def _generate_noise(self, epsilon=1e-10):
        """
        Generates noise for the given dimensions.

        Parameters:
        epsilon (float): Standard deviation of the noise.

        Returns:
        ndarray: Generated noise matrix.
        """
        return self.rng.normal(0, epsilon, size=(self.N, self.T))

    def _remove_negative_eigenvalues(self, matrix):
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
            matrix = self._remove_negative_eigenvalues(R)
            D = matrix - R
            np.fill_diagonal(matrix, diag)
            
            # Check for convergence
            if np.linalg.norm(matrix - y, ord=np.inf) / np.linalg.norm(y, ord=np.inf) < conv_tol:
                break
        else:
            print("Convergence not achieved")
        return matrix

    def _higher_order_covariance(self, C, K):
        """
        Computes higher order covariance matrices.

        Parameters:
        C (ndarray): Input covariance matrix.
        K (list): List of recursion orders.

        Yields:
        ndarray: Higher order covariance matrices.
        """
        Cf = np.identity(self.N)
        for i in range(max(K)):
            res = C - Cf
            res = self._hierarchical_cleaning(1-res)
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
        noise_matrix = self._generate_noise()
        C = np.zeros((len(self.K), self.N, self.N))

        if self.Nboot == 0:
            # Compute the correlation matrix
            Cb = np.corrcoef(self.data)
            # Apply regularization and higher order filtering
            C = np.array(list(map(self.regularization_methods[self.method], np.array(list(self._higher_order_covariance(Cb, self.K))))))
            if self.filter_type == 'covariance':
                C *= np.outer(self.std_devs, self.std_devs)
            return C[0] if len(self.K) == 1 else C

        for _ in range(self.Nboot):
            # Generate bootstrap samples with noise
            bootstrap_sample = self.data[:, self.rng.choice(self.observations, size=self.T)] + noise_matrix
            # Compute the correlation matrix
            Cb = np.corrcoef(bootstrap_sample)
            # Apply regularization and higher order filtering
            C += np.array(list(map(self.regularization_methods[self.method], np.array(list(self._higher_order_covariance(Cb, self.K))))))
        if self.filter_type == 'covariance':
            C = (C / self.Nboot) * np.outer(self.std_devs, self.std_devs)
        else:
            C /= self.Nboot

        return C[0] if len(self.K) == 1 else C

if __name__ == '__main__':
    # Generate random data
    # set a seed
    np.random.seed(42)
    x = np.random.normal(0, 1, size=(100, 10))
    # Create an instance of CovarianceFilter and filter the data
    
    bahc_instance = BAHC(x,K=[2,3], filter_type='correlation',seed=42)
    filtered_matrix = bahc_instance.filter_matrix()
    # Print the filtered matrix
    print(filtered_matrix)
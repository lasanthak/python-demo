import numpy as np
import matplotlib.pyplot as plt

def draw_noraml_dist_plot_1d(count=1000):
    mean = [0]
    covariance = [[2]]
    positions = np.random.multivariate_normal(mean, covariance, count)

    plt.figure(figsize=(np.ceil(np.percentile(positions, 99.9)), 3))
    plt.scatter(positions, np.repeat(0, count), s=5, alpha=0.5)
    plt.title("Particle Distribution with Normal Density")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis('equal')
    plt.grid(True)
    plt.show()


def draw_noraml_dist_plot_2d(count=1000):
    mean = [0, 0]  # Center of the normal distribution
    # Controls the spread of the distribution
    # covariance = [[1, 0], [0, 1]]
    covariance = [[2, 0], [0, 2]]
    # covariance = [[1, 1.5], [1.5, 2]]

    # Generate particle positions using a multivariate normal distribution
    positions = np.random.multivariate_normal(mean, covariance, count)
    x = positions[:, 0]
    y = positions[:, 1]

    plt.figure(figsize=(np.ceil(np.percentile(x, 99.9)),
                        np.ceil(np.percentile(y, 99.9))
                        ))
    plt.scatter(x, y, s=0.8, alpha=0.5)
    plt.title("Particle Distribution with Normal Density")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis('equal')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    draw_noraml_dist_plot_1d()

from GBMSimulator.GBMSimulator import GBMSimulator
import argparse
import matplotlib
# Using interactive backend capable of displaying plots
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt





simulator = GBMSimulator()

print("GBMSimulator.cli is being imported")


def generate_paths(mu, n, T, M, y0, sigma ):
    '''
    Function to generate GBM paths
    '''
    paths = simulator.simulate(mu, n,T, M, y0, sigma )
    print("returning an array with shape: ")
    print(paths.shape)

    return paths

def plot_paths(simulated_paths, M):

    '''Plots the simulated paths'''
    
    # template
    plt.style.use('ggplot') 
    # changing size of chart
    plt.figure(figsize=(12, 5))

    # Loop to do a line plot for each simulation
    for num, sim in enumerate(simulated_paths.T):
        # length of each simulation
        t_values = list(range(len(sim)))
        # simulated values
        y_values = sim

        # line plot for each sim
        plt.plot(t_values, y_values, label=f"GBM path {num+1}")


    # labelling chart
    plt.xlabel("Time")
    plt.ylabel("Y(t)")
    plt.title("Simulated Geometric Brownian Motion Path")
    if M <= 10:
        plt.legend()
        plt.show()
    else:
        plt.show()

def create_parser():
    """
    Creates and returns the argument parser
    """    
    parser = argparse.ArgumentParser(description="Generate and plot Gemoetric Brownian motion paths")
    parser.add_argument("--mu", type=float, required=True, help="Drift coefficient")
    parser.add_argument("--n", type=int, required=True, help="Number of time steps")
    parser.add_argument("--T", type=float, required=True, help="Total time duration")
    parser.add_argument("--M", type=int, required=True, help="Number of simulations")
    parser.add_argument("--y0", type=float, required=True, help="Initial value")
    parser.add_argument("--sigma", type=float, required=True, help="Volatility coefficient")

    return parser

def main():
    """
    main function for the CLI tool
    """
    parser = create_parser()
    args = parser.parse_args()

    # Generate paths
    paths = generate_paths(args.mu, args.n, args.T, args.M, args.y0, args.sigma)

    # plot paths
    plot_paths(paths, args.M)

if __name__ == "__main__":
    main()
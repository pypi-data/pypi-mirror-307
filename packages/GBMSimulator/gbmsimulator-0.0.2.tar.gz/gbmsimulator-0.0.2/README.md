# GBMSimulator

`GBMSimulator` is a Python class designed to simulate Geometric Brownian Motion (GBM), a stochastic process widely used in mathematical finance for modeling stock prices and other financial instruments.

## Features

* Simulates GBM paths given user-defined parameters.
* Supports customizable drift, volatility, initial value, number of paths, and time steps.
* Returns an array of simulated paths, which can be easily visualized or analyzed.

## Installation

Ensure you have Python 3.12 or higher. You can install the package and its dependencies from source with:

```bash
pip install -e .
```

or from PyPi with:

```bash
pip install GBMSimulator==0.0.2
```

## Usage

**Please also refer to Examples/GBMnotebook.ipynb**

1. Import the `GBMSimulator` class and `matplotlib` for plotting

```python
from GBMSimulator.GBMSimulator import  GBMSimulator
import matplotlib.pyplot as plt
```

2. Set the parameters for the GBMsimulator

```python
'''
Args:
    mu (int): drift coefficient
    n (int): number of steps
    T (int): time in years
    M (int): number of sims
    y0 (int): initial value
    sigma (int): volatility
'''
mu = 0.1
n = 100
T =  1
M = 1000
y0 = 0.01
sigma = 0.5
```

3. Create an instance of `GMBSimulator`

```python
simulator = GBMSimulator()
```

4. Create an array of simulated paths

```python
simulated_paths = simulator.simulate(mu, n, T, M, y0, sigma)
```

5. Plot the data

```python
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
else:
    plt.show()
```

## Documentation

Visit our [documentation page](https://gbmsimulator.readthedocs.io/en/latest/index.html).

## Contributing

Contributions are welcome! Fork our repository and submit a pull request.



<script
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"
  type="text/javascript">
</script>

# ModFibonacci
The Modulus of the Fibonacci Series is periodic for any mod n, 
this project both determines the period of these sequences, 
and determines whether the sequence contains every remainder of the modulus operation.

# Data
In order to save time when generating the figures, the data is stored in a npy files.
Currently, the data will be generated unless the file containing exactly the same modulus range is found.
This could easily be optimized away, but I currently don't intend to go beyond modulus $10^5$
as visualizing the data is already quite lag inducing at this point.

# Visualization
The data is visualized using either plotly or matplotlib. Pre-generated interactive plotly graphs are included in this repo as follows.
- [Up to Modulus 100k](./figures/99998/fibonacci_modulus_periods.html)
- [Up to Modulus 10k](./figures/9998/fibonacci_modulus_periods.html)
- [Up to Modulus 1k](./figures/998/fibonacci_modulus_periods.html)
- [Up to Modulus 100](./figures/98/fibonacci_modulus_periods.html)

I recommend using 10k or 1k modulus, as 100k is very large and takes a long time to load while 100 doesn't give much insight.

# Future Plans
Currently, the data is generated for all moduli up to $10^5$. This took about 6 hours to generate, so to go further, I would likely need to make some major optimizations.
Some current ideas include:
- Implement storing the data in a more efficient way, e.g. using a database.
- Pre-generate the fibonacci numbers up to some significant number, say, $10^6$ or $10^7$.
- Switch the generation to a fully compiled language for faster execution and better multithreading support.
- Experiment with GPU acceleration?

Pre-generating the fibonacci numbers, unfortunately might not be feasible due to integer limits if I switch to an explicit compiled language.
By sticking to generating the sequence purely for the moduli, I can remain under the integer limit, however this results in generating the sequence for all moduli.
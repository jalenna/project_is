# Key code components
We're following the [Black Python style guide](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html) for code formatting.

- class `Brain`:
    + Comprised of all the relevant regions in the brain
    + Main implementation of the neural network
- class `Region`:
    + Base class for all regions of the brain
    + Contains all relevant methods _| Keep in mind that the implementation **will** vary accross different regions._
- function `main`:
    + Main entry point of the application
    + Application set up is done within this function
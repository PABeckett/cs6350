# cs6350
Repository for Machine Learning Course, University of Utah

This is a machine learning library developed by Parker Beckett for CS5350/6350 at the University of Utah

*THE INSTRUCTIONS FOR HW 1 AND HW 2 WILL BE HERE SOON*

For perceptron, please put the run.sh file and hw03_perceptron.py files in the same directory. Navigate to that directory and type ./run.sh mode learning_rate epochs training_data testing_data
Mode should be st for standard, vo for voted, or av for average. Anything else will not work
Learning rate should be a number less than 1 but any number should not crash the program just result in poor results
Epochs should be an integer, any decimals will crash the program
Training and Testing data should be the filenames of the training and testing data respectively

* this should work fine, but I have been locked out of the cade lab even after changing my password numerous times. I will try to test it on campus, but this is the same syntax as the hw1 which worked


For Hw04, the user must simply type ./run.sh <problem> <C_index>
problem can be 2a 2b 3a or 3b, and C_index can be 0, 1, or 2.
You wil be prompted if your inputs are incorrect
C_index is a parameter because it can be helpful to run things with a particular C value, and many other potential arguments give perhaps too much freedom

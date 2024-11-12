# main.py

from . import exp1, exp2, exp3, exp4, exp5, exp6

experiments = {
    1: exp1.run,
    2: exp2.run,
    3: exp3.run,
    4: exp4.run,
    5: exp5.run,
    6: exp6.run
}

def list_experiments():
    print("Available Experiments:")
    for i in range(1, 7):
        print(f"{i}. Experiment {i}")

def run_experiment(exp_number):
    if exp_number in experiments:
        experiments[exp_number]()
    else:
        print("Invalid experiment number.")

# Example search using grid

from netpyne.batchtools.search import generate_constructors
from batchtk import runtk
from batchtk.runtk import constructors
from batchtk.utils import expand_path, TomlParser
from batchtk.algos import Trial

from concurrent.futures import ThreadPoolExecutor
import numpy
from itertools import product
dispatcher, _ = generate_constructors('sh', 'sfs')

parser = TomlParser(file_path="script.toml")
submit = parser.get_submit_class()

params = {
    'x0': [0, 1], #[-3, -2, -1, 0, 1, 2, 3],
    'x1': [2, 4], #[0, 1, 2, 3, 4, 5],
}

project_dir = expand_path('.', create_dirs=True)
output_dir = expand_path('./output', create_dirs=True)
storage_dir = expand_path('./output', create_dirs=True)
submit_kwargs = {'command': 'python rosenbrock.py'}
storage_constructor = constructors.SQLiteStorage
log_constructor = constructors.BatchtkLogger

trial = Trial()

trial.set_fixed_trial_args(
    dispatcher_constructor=dispatcher,
    project_dir=project_dir,
    output_dir=output_dir,
    submit_constructor=submit,
    storage_dir=storage_dir,
    submit_kwargs={'command': 'python rosenbrock.py'},
    interval=5,
    storage_constructor=storage_constructor,
    log_constructor=log_constructor,
    check_storage=True,)

grid = list(product(params['x0'], params['x1']))

def run_trial(args):
    i, (x0, x1) = args
    config = {'label': f'trial{i}', 'x0': x0, 'x1': x1}
    results = trial.run_trial(label='rosenbrock', tid=i, config=config)
    print(results)
    return results

with ThreadPoolExecutor(max_workers=4) as executor:
    all_results = list(executor.map(run_trial, enumerate(grid)))

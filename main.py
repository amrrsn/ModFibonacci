from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


###
#   Global variables
#   ----------------
#   - range_start: must be an integer >= 2
#   - range_end: must be an integer
#   - loop_count: do not change
#   - data_dir: directory where data is stored, should be a string
###

range_start = 2
range_end = 10
loop_count = range_end - range_start
data_dir = f'data/{loop_count}'


def check_sequence(modulus: int) -> (bool, int, int):
    remainders = np.arange(stop=modulus, dtype=int)

    count = 2
    last_digits = [0, 1]
    while True:
        count += 1
        last_digits = [last_digits[1], (last_digits[0] + last_digits[1]) % modulus]
        if last_digits[1] in remainders:
            remainders = np.delete(remainders, np.where(remainders == last_digits[1]))
        ###
        # optimizes the loop by skipping the rest of the loop if the sequence is found
        # this is because the sequence is found when the remainders array is empty
        # commented out because this case is rare in the long run
        # and it is preferable to keep the count consistent for the graph
        ###
        # if not remainders.size:
        #     contains_y[modulus-range_start] = count
        #     return True
        if last_digits == [0, 1]:
            break

    if not remainders.size:
        return True, modulus, count
    return False, modulus, count


if __name__ == '__main__' and not os.path.exists(f"{data_dir}/contains_x_{loop_count}.npy"):
    contains_x = np.arange(stop=loop_count, dtype=int)
    contains_y = np.zeros(loop_count, dtype=int)
    doesnt_contain_x = np.arange(stop=loop_count, dtype=int)
    doesnt_contain_y = np.zeros(loop_count, dtype=int)

    contains_all = 0
    doesnt_contain_all = 0
    pool = mp.Pool(processes=mp.cpu_count())
    for i, mod, ct in tqdm(pool.imap_unordered(check_sequence, np.arange(range_start, range_end, dtype=int)), total=loop_count):
        contains_y[mod - range_start] = i*ct
        doesnt_contain_y[mod - range_start] = (not i)*ct
        contains_all += i
        doesnt_contain_all += (not i)
    pool.close()

    contains_x = np.delete(contains_x, np.where(contains_y == 0))
    contains_y = np.delete(contains_y, np.where(contains_y == 0))
    doesnt_contain_x = np.delete(doesnt_contain_x, np.where(doesnt_contain_y == 0))
    doesnt_contain_y = np.delete(doesnt_contain_y, np.where(doesnt_contain_y == 0))

    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    if not os.path.exists(f'{data_dir}/contains_x_{loop_count}.npy'):
        np.save(f'{data_dir}/contains_y_{loop_count}.npy', contains_y)
        np.save(f'{data_dir}/doesnt_contain_x_{loop_count}.npy', doesnt_contain_x)
        np.save(f'{data_dir}/doesnt_contain_y_{loop_count}.npy', doesnt_contain_y)
        np.save(f'{data_dir}/contains_x_{loop_count}.npy', contains_x)

    print(f"{(contains_all+1)}/{contains_all+doesnt_contain_all+1} = {(contains_all+1)/(contains_all + doesnt_contain_all+1)*100}% of the moduli contain every remainder.")

if __name__ == '__main__':
    contains_x = np.load(f'{data_dir}/contains_x_{loop_count}.npy')
    contains_y = np.load(f'{data_dir}/contains_y_{loop_count}.npy')
    doesnt_contain_x = np.load(f'{data_dir}/doesnt_contain_x_{loop_count}.npy')
    doesnt_contain_y = np.load(f'{data_dir}/doesnt_contain_y_{loop_count}.npy')

    # plt.plot(doesnt_contain_x, doesnt_contain_y, 'yo', label="Doesn't contain every remainder")
    # plt.plot(contains_x, contains_y, 'kx', label="Contains every remainder")
    # plt.xlabel("Modulus")
    # plt.ylabel("Iterations")
    # plt.legend(fontsize=10)
    # plt.title("Fibonacci modulus iterations before repeating sequence")
    # plt.show()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=contains_x, y=contains_y, mode='markers', name='Contains every remainder'))
    fig.add_trace(go.Scatter(x=doesnt_contain_x, y=doesnt_contain_y, mode='markers', name='Doesn\'t contain every remainder'))
    fig.update_layout(title="Fibonacci modulus iterations before repeating sequence", xaxis_title="Modulus", yaxis_title="Iterations")
    fig.show()

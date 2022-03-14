from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import plotly.graph_objects as go

###
#   Global variables
#   ----------------
#   - range_start: must be an integer >= 2
#   - range_end: must be an integer
#   - loop_count: do not change
#   - data_dir: directory where data is stored, should be a string
#   - figures_dir: directory where figures are stored, should be a string
#   - plot_type: plotly or matplotlib
###

range_start = 2
range_end = 100000
loop_count = range_end - range_start
data_dir = f'data/{loop_count}'
figures_dir = f'figures/{loop_count}'
plot_type = 'plotly'


def check_sequence(modulus: int) -> (bool, int, int):
    """
    Generates the periodic sequence of the fibonacci series for a given modulus.

    :param modulus: The modulus to be used in the sequence.
    :return: Tuples of (bool, int, int) where the first element is a boolean indicating whether the sequence contains every remainder modulus, the second element is the modulus, and the third element is the length of the period.
    """
    remainders = np.arange(stop=modulus, dtype=int)

    period_length = 0
    last_digits = [0, 1]
    while True:
        period_length += 1
        last_digits = [last_digits[1], (last_digits[0] + last_digits[1]) % modulus]
        if last_digits[1] in remainders:
            remainders = np.delete(remainders, np.where(remainders == last_digits[1]))
        ###
        # optimizes the loop by skipping the rest of the loop if the sequence is found
        # this is because the sequence is found when the remainders array is empty
        # commented out because this case is rare in the long run,
        # and it is preferable to keep the period length consistent for the graph
        ###
        # if not remainders.size:
        #     contains_y[modulus-range_start] = period_length
        #     return True
        if last_digits == [0, 1]:
            break

    if not remainders.size:
        return True, modulus, period_length
    return False, modulus, period_length


###
#   The variables contains_y/x and doesnt_contain_y/x are used to store the results of the check_sequence function
#   They are vaguely named, but the contains array is for the case where the sequence contains every remainder modulus,
#   and the doesnt_contain array is for the case where the sequence does not contain every remainder modulus.
###


if __name__ == '__main__' and not os.path.exists(f"{data_dir}/contains_x_{loop_count}.npy"):
    contains_x = np.arange(stop=range_end, dtype=int)
    contains_y = np.zeros(range_end, dtype=int)
    doesnt_contain_x = np.arange(stop=range_end, dtype=int)
    doesnt_contain_y = np.zeros(range_end, dtype=int)

    contains_all = 0
    doesnt_contain_all = 0
    pool = mp.Pool(processes=mp.cpu_count())
    for i, mod, ct in tqdm(pool.imap_unordered(
            check_sequence, np.arange(start=range_start, stop=range_end, dtype=int)), total=loop_count):
        contains_y[mod] = i * ct
        doesnt_contain_y[mod] = (not i) * ct
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

    print(f"{(contains_all + 1)}/{contains_all + doesnt_contain_all + 1} = "
          f"{(contains_all + 1) / (contains_all + doesnt_contain_all + 1) * 100}% of moduli contain every remainder.")

if __name__ == '__main__':
    contains_x = np.load(f'{data_dir}/contains_x_{loop_count}.npy')
    contains_y = np.load(f'{data_dir}/contains_y_{loop_count}.npy')
    doesnt_contain_x = np.load(f'{data_dir}/doesnt_contain_x_{loop_count}.npy')
    doesnt_contain_y = np.load(f'{data_dir}/doesnt_contain_y_{loop_count}.npy')

    if plot_type == 'matplotlib':
        plt.plot(doesnt_contain_x, doesnt_contain_y, 'yo', label="Doesn't contain every remainder")
        plt.plot(contains_x, contains_y, 'kx', label="Contains every remainder")
        plt.xlabel("Modulus")
        plt.ylabel("Iterations")
        plt.legend(fontsize=10)
        plt.title("Fibonacci modulus iterations before repeating sequence")
        plt.show()

    if plot_type == 'plotly':
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=doesnt_contain_x, y=doesnt_contain_y, mode='markers', marker=dict(
            size=10, symbol="circle"), name="Doesn't contain every remainder"))
        fig.add_trace(go.Scatter(x=contains_x, y=contains_y, mode='markers', marker=dict(
            size=10, symbol="star"), name="Contains every remainder"))
        fig.update_layout(template="plotly_white", title="Fibonacci Modulus Sequence Periods",
                          xaxis_title="Modulus", yaxis_title="Sequence Period")
        # fig.show()
        if not os.path.exists(figures_dir):
            os.mkdir(figures_dir)
        fig.write_html(f'{figures_dir}/fibonacci_modulus_periods.html')

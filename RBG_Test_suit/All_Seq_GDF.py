import matplotlib.pyplot as plt
import os


# ======================= Calculate Gap Structures =====================================================================
# Function to calculate gap structures (lengths of consecutive zeros) in a sequence
def cal_gaps(_sequence):
    gap = []
    gap_counter = 0
    no_gap = 0                  # when we do not know the first bit is 1 or 0 so the condition is false

    for bits in _sequence:
        if bits == 0:
            gap_counter += 1    # calculate the number of continued zeros between two ones
        elif bits == 1:         # finds the 1s in a list start checking for no gaps.
            if no_gap:          # if there are two continued 1s in a list then append the counter
                gap.append(gap_counter)  # add 0s in every step with no gap
            gap_counter = 0     # Reset the counter
            no_gap = 1          # found the no_gap in the list, it is true
    # print("gaps: ", gap)
    return gap


# ==================== Count and Normalise the gap structure ===========================================================
def cal_norm_gaps(my_seq):                   # find the unique gaps in the sequence
    uniq_gaps_ = []
    counts_ = []
    for unq_gap_len in set(my_seq):
        count = my_seq.count(unq_gap_len)    # count repetition of same gaps
        uniq_gaps_.append(unq_gap_len)        # find and store the unique gaps
        counts_.append(count)                 # Total Number of similar gaps

    # Normalise the gap structures
    total = sum(my_seq)                      # sum of Gap sequence
    norm_gaps_ = []                           # normalised gap structures
    for count in counts_:
        normalised = count / total           # normalise every count using total sum of gaps
        norm_gaps_.append(normalised)         # store normalised gaps in a list

    # print("counts: ", counts, "unique gaps: ", uniq_gaps_, "norm gaps: ", norm_gaps_)
    return uniq_gaps_, norm_gaps_, counts_


# Function to read sequences from a .txt file ==========================================================================
def read_sequences(file_name_):
    with open(file_name_, 'r') as file:                      # open the file in a read mode
        _sequences = []                                      # set a buffer to store the sequences
        for line in file:
            stripped_line = line.strip()                     # extract each sequence as a separate line
            mapped_line = list(map(int, stripped_line))      # convert each line to the list of integers
            _sequences.append(mapped_line)                   # append each sequence as a list to the buffer
    return _sequences                                        # return the list of sequences


# Function to calculate norm_gaps and uniq_gaps of each sequence =======================================================
def get_norm_gaps(seq_):
    all_norm_gaps = []                                          # set a buffer to store the normalised gaps
    for sequence in seq_:
        gaps = cal_gaps(sequence)                               # find the gaps from each sequence
        u_gaps, norm_gaps, count = cal_norm_gaps(gaps)          # collect only normalised gaps
        all_norm_gaps.append(norm_gaps)   # set them with a descending order to ease the further part
    return all_norm_gaps


# Function to get particular gap lengths from the list of sequences ====================================================
def get_selected_gap(seq_list, gap_index_value):
    sel_gaps = []
    for n in seq_list:
        # Check for list is empty or not
        if len(n) > 0:
            sel_gaps.append(n[gap_index_value])
        else:
            # If empty, append 0
            sel_gaps.append(0)
    return sel_gaps

# Function to plot the normalized gap length of 0 and 1 for all sequences ==============================================
def plot_GDF_zeros(norm_gaps_zero, f_name=None):
    avg_norm_gap_zero = sum(norm_gaps_zero) / len(norm_gaps_zero)
    plt.figure()
    plt.plot(norm_gaps_zero, label=f'Expected = 0.50\nAvg. = {avg_norm_gap_zero:.5f}')
    plt.axhline(y=0.5, color='r', linestyle='-', linewidth=1)  # Horizontal line at y = 0.5
    plt.axhline(y=avg_norm_gap_zero, color='g', linestyle='-', linewidth=1)  # Horizontal line at average value
    plt.text(0, avg_norm_gap_zero, f'Avg: {avg_norm_gap_zero:.2f}', color='b', va='bottom')  # Add average value label
    plt.title(f"Normalized length of 0 gap for {f_name}")
    plt.xlabel("Sequence Number")
    plt.ylabel("Normalized Gap Length")
    plt.legend()


def plot_GDF_ones(norm_gaps_one, file_n=None):
    avg_norm_gap_one = sum(norm_gaps_one) / len(norm_gaps_one)
    plt.figure()
    plt.plot(norm_gaps_one, label=f'Avg. = {avg_norm_gap_one:.3f}')
    plt.axhline(y=avg_norm_gap_one, color='g', linestyle='-', linewidth=1.5)  # Horizontal line at average value
    plt.text(0, avg_norm_gap_one, f'Avg: {avg_norm_gap_one:.2f}', color='b', va='bottom')  # Add average value label
    plt.title(f"Normalized length of 1 gap {file_n}")
    plt.xlabel("Sequence Number")
    plt.ylabel("Normalized Gap Length")
    plt.legend()


# Use the functions ====================================================================================================
file_names = ['../RBG_data_files/QRNG.txt',
              '../RBG_data_files/AES_DRBG.txt', '../RBG_data_files/BBS_blum_blum_shub.txt',
              '../RBG_data_files/ChaCha20.txt', '../RBG_data_files/CTR_DRBG.txt',
              '../RBG_data_files/hash_drbg.txt',
              '../RBG_data_files/hmac_drbg.txt', '../RBG_data_files/M_sequences.txt',
              '../RBG_data_files/RC4_algorithm.txt', '../RBG_data_files/RSA_algorithm.txt',
              '../RBG_data_files/Synthetic_RBG.txt', '../RBG_data_files/Q_bit-flip_noice_Model.txt',
              '../RBG_data_files/Ideal Q-simulator.txt', '../RBG_data_files/Q_thermal_noice_Model.txt']

for file_name in file_names[0:1]:
    # get the file names
    b_n = os.path.basename(file_name)           # Extract only the file name
    base_name = os.path.splitext(b_n)[0]        # Remove file extension

    sequences = read_sequences(file_name)       # collect All the sequences
    ang = get_norm_gaps(sequences)              # all normalised gaps
    get_gap0 = get_selected_gap(ang, 0)
    get_gap1 = get_selected_gap(ang, 1)

    plot_GDF_zeros(get_gap0, base_name)
    plt.savefig(f"Zeros_{base_name}.png")

    plot_GDF_ones(get_gap1, base_name)
    plt.savefig(f"Ones_{base_name}.png")
#
plt.show()

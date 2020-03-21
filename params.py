import os

from sklearn.preprocessing import MinMaxScaler

# os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

# if multiple autoencoder exist, say n, each embedding dim will be TOTAL_EMBEDDING_DIM/n
TOTAL_EMBEDDING_DIM = 96

# walk, bike, bus, driving, //or train/subway
modes_to_use = [0, 1, 3]
N_CLASS = len(modes_to_use)

MAX_SEGMENT_SIZE = 184
MIN_N_POINTS = 10

DIM = 8  # Embedding dimension
TAU = 8  # Embedding delay

N_VECTORS = MAX_SEGMENT_SIZE - TAU * (DIM - 1) # RP mat size

SCALER = MinMaxScaler()

RP_MAT_SCALE_EACH_FEATURE = False
RP_MAT_SCALE_ALL = False

SCALE_SEGS_EACH_FEATURE = False

FILTER_SEGS = False

# 0        1     2  3  4  5  6   7    8  9
# delta_t, hour, d, v, a, h, hc, hcr, s, tn
FEATURES_SET_1 = [3, 4, 7]
FEATURES_SET_2 = [3, 4, 7]
# loss wight
ALPHA = 1
BETA = 4
GAMMA = 1

MULTI_GPU = False

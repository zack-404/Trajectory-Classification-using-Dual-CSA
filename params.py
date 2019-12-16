from sklearn.preprocessing import MinMaxScaler

from trajectory_extraction import modes_to_use

# if multiple autoencoder exist, say n, each embedding dim will be TOTAL_EMBEDDING_DIM/n
TOTAL_EMBEDDING_DIM = 30
N_CLASS = len(modes_to_use)

MAX_SEGMENT_SIZE = 184
MIN_N_POINTS = 10

DIM = 8  # Embedding dimension
TAU = 8  # Embedding delay

SCALER = MinMaxScaler()

RP_MAT_SCALE_EACH_FEATURE = False
RP_MAT_SCALE_ALL = False

SCALE_SEGS_EACH_FEATURE = False

FILTER_SEGS = False

import argparse
import multiprocessing
import time
from math import cos, pi

import numpy as np
from numpy.linalg import norm
from pyts.image.recurrence import _trajectories

from params import DIM, TAU, FEATURES_SET_1
from utils import scale_any_shape_data, scale_RP_each_feature

#  Settings for the embedding

# Distance metric in phase space ->
# Possible choices ("manhattan","euclidean","supremum")
METRIC = "euclidean"

EPS = 0.05  # Fixed recurrence threshold


def gen_multiple_RP_mats(series, scale=False, dim=DIM, tau=TAU):
    """
    generate a RP mat for each series
    """

    n_series = len(series)

    print('calc distance_mats ....')
    # each series generates n_vectors phase space phase_vectors
    phase_vectorss = _trajectories(series, dimension=dim, time_delay=tau)
    n_vectors = phase_vectorss.shape[1]
    # calc distances mats, 1 mat for each series.
    # shape:(n_samples, n_vectors, n_vectors)
    # from source code in pyts.image.recurrence.RecurrencePlot.transform
    distance_mats = np.sqrt(
        np.sum((phase_vectorss[:, None, :, :] - phase_vectorss[:, :, None, :]) ** 2,
               axis=3, dtype='float32')
    )
    print('end calc distance_mats')

    mycode = False
    if mycode:
        ## my code to calc distances
        RP_mats = []  # !!skipped Heavside function
        count = 0
        for distance_mat, phase_vectors in zip(distance_mats, phase_vectorss):
            print('{}/{}'.format(count, n_series))
            # now no need to use this method since we want to calc sign value
            # https://stackoverflow.com/questions/13079563/how-does-condensed-distance-matrix-work-pdist
            # distances = pdist(phase_vectors, )
            sign_value_mat = np.empty((n_vectors, n_vectors))
            for i in range(n_vectors):
                for j in range(n_vectors):
                    a = phase_vectors[i]
                    b = phase_vectors[j]
                    if i == j:
                        sign_value = 1
                    else:
                        # equation (5) in "Robust Single Accelerometer-Based Activity Recognition
                        # Using Modified Recurrence Plot"
                        sign_value = sign(a, b)
                    sign_value_mat[i][j] = sign_value
            sign_value_mat = np.array(sign_value_mat)
            RP_mat = sign_value_mat * distance_mat
            RP_mats.append(RP_mat)
            count += 1

        RP_mats = np.array(RP_mats)
    else:
        RP_mats = distance_mats  # !!skipped Heavside function
    if scale:
        RP_mats = scale_any_shape_data(RP_mats)
    return RP_mats


def sign(m, n):
    # equation (5) in "Robust Single Accelerometer-Based Activity Recognition
    # Using Modified Recurrence Plot"
    m = np.array(m)
    n = np.array(n)
    dim = m.shape[0]  # vector dim
    v = np.repeat(1, dim)  # base vec
    cos_angle = np.dot(m - n, v) / (norm(m - n) * norm(v))
    if cos_angle < cos(3. / 4. * pi):
        return -1
    else:
        return 1


if __name__ == '__main__':
    start = time.time()
    parser = argparse.ArgumentParser(description='RP_mat')
    parser.add_argument('--dim', default=DIM, type=int)
    parser.add_argument('--tau', default=TAU, type=int)
    parser.add_argument('--feature_set', type=str)
    parser.add_argument('--trjs_segs_features_path', type=str)
    parser.add_argument('--save_path', type=str)

    args = parser.parse_args()
    dim = args.dim
    tau = args.tau
    print('dim:{} tau:{}'.format(dim, tau))
    if args.feature_set is None:
        feature_set = FEATURES_SET_1
    else:
        feature_set = [int(item) for item in args.feature_set.split(',')]
    print('feature_set:{}'.format(feature_set))

    trjs_segs_features = np.load(args.trjs_segs_features_path)

    features_RP_mats = []
    n_features = trjs_segs_features.shape[3]
    trjs_segs_features = np.squeeze(trjs_segs_features)

    for i in range(n_features):
        single_feature_segs = trjs_segs_features[:, :, i]  # (n, seg_size)
        # generate RP mat for each seg
        feature_RP_mats = gen_multiple_RP_mats(single_feature_segs[:], scale=False, dim=dim, tau=tau)
        feature_RP_mats = np.expand_dims(feature_RP_mats, axis=3)
        features_RP_mats.append(feature_RP_mats)
        max = np.max(feature_RP_mats)
        min = np.min(feature_RP_mats)
        print('RP mat value range:', min, max)
    features_RP_mats = np.concatenate(features_RP_mats, axis=3)

    print(' ####\nfeatures_RP_mats.shape:{}'.format(features_RP_mats.shape))
    end = time.time()
    print('Running time: %s Seconds' % (end - start))
    np.save(args.save_path, scale_RP_each_feature(features_RP_mats))  # note scaled!

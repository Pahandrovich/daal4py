#*******************************************************************************
# Copyright 2014-2019 Intel Corporation
# All Rights Reserved.
#
# This software is licensed under the Apache License, Version 2.0 (the
# "License"), the following terms apply:
#
# You may not use this file except in compliance with the License.  You may
# obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#*******************************************************************************

# daal4py logistic regression example for shared memory systems

import daal4py as d4p
import numpy as np
import os
from daal4py.oneapi import sycl_context, sycl_buffer

# let's try to use pandas' fast csv reader
try:
    import pandas
    read_csv = lambda f, c, t=np.float64: pandas.read_csv(f, usecols=c, delimiter=',', header=None, dtype=t)
except:
    # fall back to numpy loadtxt
    read_csv = lambda f, c, t=np.float64: np.loadtxt(f, usecols=c, delimiter=',', ndmin=2)


# Commone code for both CPU and GPU computations
def compute(train_data, train_labels, predict_data, nClasses):
    # set parameters and train
    train_alg = d4p.logistic_regression_training(nClasses=nClasses, interceptFlag=True)
    train_result = train_alg.compute(train_data, train_labels)
    # set parameters and compute predictions
    predict_alg = d4p.logistic_regression_prediction(nClasses=nClasses)
    return predict_alg.compute(predict_data, train_result.model), train_result


# At this moment with sycl we are working only with numpy arrays
def to_numpy(data):
    try:
        from pandas import DataFrame
        if isinstance(data, DataFrame):
            return np.ascontiguousarray(data.values)
    except:
        pass
    try:
        from scipy.sparse import csr_matrix
        if isinstance(data, csr_matrix):
            return data.toarray()
    except:
        pass
    return data


def main(readcsv=read_csv, method='defaultDense'):
    nClasses = 2
    nFeatures = 20

    # read training data from file with 20 features per observation and 1 class label
    trainfile = os.path.join('..', 'data', 'batch', 'binary_cls_train.csv')
    train_data = readcsv(trainfile, range(nFeatures))
    train_labels = readcsv(trainfile, range(nFeatures, nFeatures + 1))

    # read testing data from file with 20 features per observation
    testfile = os.path.join('..', 'data', 'batch', 'binary_cls_test.csv')
    predict_data = readcsv(testfile, range(nFeatures))
    predict_labels = readcsv(testfile, range(nFeatures, nFeatures + 1))

    # Using of the classic way (computations on CPU)
    result_classic, train_result = compute(train_data, train_labels, predict_data, nClasses)

    train_data = to_numpy(train_data)
    train_labels = to_numpy(train_labels)
    predict_data = to_numpy(predict_data)

    # It is possible to specify to make the computations on GPU
    with sycl_context('gpu'):
        sycl_train_data = sycl_buffer(train_data)
        sycl_train_labels = sycl_buffer(train_labels)
        sycl_predict_data = sycl_buffer(predict_data)
        result_gpu, _ = compute(sycl_train_data, sycl_train_labels, sycl_predict_data, nClasses)

    # the prediction result provides prediction
    assert result_classic.prediction.shape == (predict_data.shape[0], train_labels.shape[1])

    assert np.allclose(result_classic.prediction, result_gpu.prediction)

    return (train_result, result_classic, predict_labels)


if __name__ == "__main__":
    (train_result, predict_result, predict_labels) = main()
    print("\nLogistic Regression coefficients:\n", train_result.model.Beta)
    print("\nLogistic regression prediction results (first 10 rows):\n", predict_result.prediction[0:10])
    print("\nGround truth (first 10 rows):\n", predict_labels[0:10])
    print('All looks good!')

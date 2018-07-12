#*******************************************************************************
# Copyright 2014-2018 Intel Corporation
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

# daal4py Decision Tree Regression example for shared memory systems

import daal4py as d4p
from numpy import loadtxt, allclose

if __name__ == "__main__":

    infile = "./data/batch/decision_tree_train.csv"
    prunefile = "./data/batch/decision_tree_prune.csv"

    # Configure a Linear regression training object
    train_algo = d4p.decision_tree_regression_training()
    
    # Read data. Let's have 5 independent, and 1 dependent variables (for each observation)
    indep_data = loadtxt(infile, delimiter=',', usecols=range(5))
    dep_data   = loadtxt(infile, delimiter=',', usecols=range(5,6))
    prune_indep = loadtxt(prunefile, delimiter=',', usecols=range(5))
    prune_dep = loadtxt(prunefile, delimiter=',', usecols=range(5,6))
    dep_data.shape = (dep_data.size, 1) # must be a 2d array
    prune_dep.shape = (prune_dep.size, 1) # must be a 2d array
    # Now train/compute, the result provides the model for prediction
    train_result = train_algo.compute(indep_data, dep_data, prune_indep, prune_dep)

    # Now let's do some prediction
    predict_algo = d4p.decision_tree_regression_prediction()
    # read test data (with same #features)
    pdata = loadtxt("./data/batch/decision_tree_test.csv", delimiter=',', usecols=range(5))
    # now predict using the model from the training above
    predict_result = predict_algo.compute(pdata, train_result.model)

    # The prediction result provides prediction
    assert predict_result.prediction.shape == (pdata.shape[0], dep_data.shape[1])

    print('All looks good!')
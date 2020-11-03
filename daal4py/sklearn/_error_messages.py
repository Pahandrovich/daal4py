#
#*******************************************************************************
# Copyright 2020 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#******************************************************************************/

class daal4py_message():
    """
    This class defined all messages for error handling of python part of daal4py
    """
    def get_eps_must_be_positive():
        return "eps must be positive."
    def get_cluster_centers_should_either_be():
        return "Cluster centers should either be 'k-means++', 'random', 'deterministic' or an array"
    def get_wrong_iterations_number():
        return "Wrong iterations number"
    def get_invalid_number_of_initializations():
        return "Invalid number of initialization. n_init=%d must be bigger than zero."
    def get_number_of_iterations_should_be_a_positive_number():
        return "Number of iterations should be a positive number, got %d instead"
    def get_precompute_distances_should_be():
        return "precompute_distances should be 'auto' or True/False, but a value of %s was passed"
    def get_the_shape_of_the_initial_centers_does_not_match_the_number_of_clusters():
        return "The shape of the initial centers %s does not match the number of clusters %d."
    def get_the_shape_of_the_initial_centers_does_not_match_the_number_of_features():
        return "The shape of the initial centers %s does not match the number of features of the data %d."
    def get_init_should_be_either():
        return ("init should be either 'k-means++', 'random', a ndarray or a "
                "callable, got '%s' instead.")
    def get_n_init_should_be():
        return "n_init should be > 0, got %d instead."
    def get_max_iter_should_be():
        return "max_iter should be > 0, got %d instead."
    def get_algorithm_must_be_auto_full_or_elkan():
        return ("Algorithm must be 'auto', 'full' or 'elkan', got"
                         "%s")
    def get_incorrect_number_of_features_got():
        return ("Incorrect number of features. Got %d features, "
                "expected %d.")

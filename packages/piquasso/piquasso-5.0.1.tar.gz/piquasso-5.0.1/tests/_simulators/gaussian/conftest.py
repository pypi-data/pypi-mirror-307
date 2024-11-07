#
# Copyright 2021-2024 Budapest Quantum Computing Group
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

import pytest

import numpy as np

import piquasso as pq


@pytest.fixture
def state():
    with pq.Program() as initialization:
        pq.Q(0) | pq.Displacement(r=1)
        pq.Q(1) | pq.Displacement(r=1, phi=np.pi / 2)
        pq.Q(2) | pq.Displacement(r=1, phi=np.pi / 4)

        pq.Q(0) | pq.Squeezing(np.log(2), phi=np.pi / 2)
        pq.Q(1) | pq.Squeezing(np.log(1), phi=np.pi / 4)
        pq.Q(2) | pq.Squeezing(np.log(2), phi=np.pi / 2)

    simulator = pq.GaussianSimulator(d=3)
    state = simulator.execute(initialization).state
    state.validate()

    return state

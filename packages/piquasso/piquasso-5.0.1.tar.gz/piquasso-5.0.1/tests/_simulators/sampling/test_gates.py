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


def test_program():
    U = np.array([[0.5, 0, 0], [0, 0.5j, 0], [0, 0, -1]], dtype=complex)

    with pq.Program() as program:
        pq.Q(all) | pq.StateVector([1, 1, 1, 0, 0])

        pq.Q(0, 1) | pq.Beamsplitter(0.5)
        pq.Q(1, 2, 3) | pq.Interferometer(U)
        pq.Q(3) | pq.Phaseshifter(0.5)
        pq.Q(4) | pq.Phaseshifter(0.5)
        pq.Q() | pq.ParticleNumberMeasurement()

    simulator = pq.SamplingSimulator(d=5)
    result = simulator.execute(program, shots=10)

    assert len(result.samples) == 10


def test_interferometer():
    U = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=complex)

    with pq.Program() as program:
        pq.Q(all) | pq.StateVector([1, 1, 1, 0, 0])

        pq.Q(4, 3, 1) | pq.Interferometer(U)

    simulator = pq.SamplingSimulator(d=5)
    state = simulator.execute(program).state

    expected_interferometer = np.array(
        [
            [1, 0, 0, 0, 0],
            [0, 9, 0, 8, 7],
            [0, 0, 1, 0, 0],
            [0, 6, 0, 5, 4],
            [0, 3, 0, 2, 1],
        ],
        dtype=complex,
    )

    assert np.allclose(state.interferometer, expected_interferometer)


def test_phaseshifter():
    phi = np.pi / 2

    with pq.Program() as program:
        pq.Q(all) | pq.StateVector([1, 1, 1, 0, 0])

        pq.Q(2) | pq.Phaseshifter(phi)

    simulator = pq.SamplingSimulator(d=5)
    state = simulator.execute(program).state

    x = np.exp(1j * phi)
    expected_interferometer = np.array(
        [
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, x, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
        ],
        dtype=complex,
    )

    assert np.allclose(state.interferometer, expected_interferometer)


def test_beamsplitter():
    theta = np.pi / 4
    phi = np.pi / 3

    with pq.Program() as program:
        pq.Q(all) | pq.StateVector([1, 1, 1, 0, 0])

        pq.Q(1, 3) | pq.Beamsplitter(theta, phi)

    simulator = pq.SamplingSimulator(d=5)
    state = simulator.execute(program).state

    t = np.cos(theta)
    r = np.exp(1j * phi) * np.sin(theta)
    rc = np.conj(r)
    expected_interferometer = np.array(
        [
            [1, 0, 0, 0, 0],
            [0, t, 0, -rc, 0],
            [0, 0, 1, 0, 0],
            [0, r, 0, t, 0],
            [0, 0, 0, 0, 1],
        ],
        dtype=complex,
    )

    assert np.allclose(state.interferometer, expected_interferometer)


def test_lossy_program():
    r"""
    This test checks the average number of particles in the lossy BS.
    We expect average number to be smaller than initial one.
    """
    losses = 0.5

    d = 5
    simulator = pq.SamplingSimulator(d=d)

    initial_state = [1, 1, 1, 0, 0]

    with pq.Program() as program:
        pq.Q(all) | pq.StateVector(initial_state)

        for i in range(d):
            pq.Q(i) | pq.Loss(losses)

        pq.Q(0) | pq.Loss(transmissivity=0.0)
        pq.Q() | pq.ParticleNumberMeasurement()

    result = simulator.execute(program, shots=1)
    sample = result.samples[0]
    assert sum(sample) < sum(initial_state)


@pytest.mark.monkey
def test_LossyInterferometer_decreases_particle_number(generate_unitary_matrix):
    d = 5

    singular_values = np.array([0.0, 0.2, 0.3, 0.4, 0.5])

    lossy_interferometer_matrix = (
        generate_unitary_matrix(d)
        @ np.diag(singular_values)
        @ generate_unitary_matrix(d)
    )

    simulator = pq.SamplingSimulator(d=d)

    initial_state = [1, 1, 1, 0, 0]

    with pq.Program() as program:
        pq.Q(all) | pq.StateVector(initial_state)

        pq.Q() | pq.LossyInterferometer(lossy_interferometer_matrix)
        pq.Q() | pq.ParticleNumberMeasurement()

    result = simulator.execute(program, shots=1)
    sample = result.samples[0]
    assert sum(sample) < sum(initial_state)


@pytest.mark.monkey
def test_LossyInterferometer_is_equivalent_to_Loss_and_Interferometers(
    generate_unitary_matrix,
):
    d = 5

    singular_values = np.array([0.0, 0.2, 0.3, 0.4, 0.5])

    first_unitary = generate_unitary_matrix(d)
    second_unitary = generate_unitary_matrix(d)

    lossy_interferometer_matrix = (
        first_unitary @ np.diag(singular_values) @ second_unitary
    )

    simulator = pq.SamplingSimulator(d=d)

    with pq.Program() as program_using_lossy_interferometer:
        pq.Q() | pq.StateVector([1, 1, 1, 0, 0])

        pq.Q() | pq.LossyInterferometer(lossy_interferometer_matrix)

    state_obtained_via_lossy_interferometer = simulator.execute(
        program_using_lossy_interferometer
    ).state

    with pq.Program() as program_using_loss:
        pq.Q() | pq.StateVector([1, 1, 1, 0, 0])

        pq.Q() | pq.Interferometer(second_unitary)

        for mode, loss in enumerate(singular_values):
            pq.Q(mode) | pq.Loss(loss)

        pq.Q() | pq.Interferometer(first_unitary)

    state_obtained_via_loss = simulator.execute(program_using_loss).state

    assert state_obtained_via_lossy_interferometer == state_obtained_via_loss


@pytest.mark.monkey
def test_LossyInterferometer_raises_InvalidParameter_for_invalid_matrix(
    generate_unitary_matrix,
):
    d = 5

    singular_values_out_of_bound = np.array([42, 0.2, 0.3, 0.4, 0.5])

    invalid_matrix = (
        generate_unitary_matrix(d)
        @ np.diag(singular_values_out_of_bound)
        @ generate_unitary_matrix(d)
    )

    with pytest.raises(pq.api.exceptions.InvalidParameter):
        pq.LossyInterferometer(invalid_matrix)


@pytest.mark.parametrize("connector", (pq.NumpyConnector(), pq.JaxConnector()))
def test_Interferometer_fock_probabilities(connector):
    U = np.array(
        [
            [
                -0.17959207 - 0.29175972j,
                -0.64550941 - 0.02897055j,
                -0.023922 - 0.38854671j,
                -0.07908932 + 0.35617293j,
                -0.39779191 + 0.14902272j,
            ],
            [
                -0.36896208 + 0.19468375j,
                -0.11545557 + 0.20434514j,
                0.25548079 + 0.05220164j,
                -0.51002161 + 0.38442256j,
                0.48106678 - 0.25210091j,
            ],
            [
                0.25912844 + 0.16131742j,
                0.11886251 + 0.12632645j,
                0.69028213 - 0.25734432j,
                0.01276639 + 0.05841739j,
                0.03713264 + 0.57364845j,
            ],
            [
                -0.20314019 - 0.18973473j,
                0.59146854 + 0.28605532j,
                -0.11096495 - 0.26870144j,
                -0.47290354 - 0.0489408j,
                -0.42459838 + 0.01554643j,
            ],
            [
                -0.5021973 - 0.53474291j,
                0.24524545 - 0.0741398j,
                0.37786104 + 0.10225255j,
                0.46696955 + 0.10636677j,
                0.07171789 - 0.09194236j,
            ],
        ]
    )

    with pq.Program() as program:
        pq.Q(all) | pq.StateVector([2, 1, 1, 0, 1])

        pq.Q(all) | pq.Interferometer(U)

    simulator = pq.SamplingSimulator(
        d=5, connector=connector, config=pq.Config(cutoff=6)
    )
    state = simulator.execute(program).state

    assert np.allclose(
        state.fock_probabilities,
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.00943787,
            0.00952411,
            0.00372613,
            0.01094254,
            0.02038039,
            0.00721118,
            0.01276527,
            0.00433598,
            0.00237178,
            0.00278069,
            0.00318524,
            0.00132885,
            0.00397591,
            0.00996051,
            0.01264881,
            0.00220331,
            0.0263324,
            0.00118848,
            0.00093221,
            0.00004332,
            0.00010173,
            0.03650928,
            0.00019833,
            0.00083033,
            0.00359651,
            0.01506536,
            0.00535646,
            0.00911342,
            0.00016192,
            0.00136495,
            0.01919529,
            0.00575667,
            0.00475163,
            0.00292093,
            0.01845835,
            0.00263738,
            0.01015263,
            0.00054558,
            0.01018948,
            0.00096209,
            0.00011264,
            0.00943751,
            0.00189028,
            0.00000646,
            0.02838532,
            0.01428406,
            0.00594266,
            0.0064234,
            0.00449348,
            0.00728765,
            0.00350418,
            0.00156008,
            0.00514618,
            0.00322227,
            0.0169176,
            0.01227155,
            0.00377727,
            0.03192492,
            0.00117325,
            0.00669423,
            0.00949246,
            0.00333097,
            0.00253143,
            0.00598864,
            0.00747331,
            0.0070525,
            0.01895052,
            0.00600548,
            0.00199403,
            0.01716476,
            0.00200791,
            0.00334997,
            0.00360096,
            0.00415943,
            0.00176133,
            0.00270693,
            0.00259121,
            0.00057382,
            0.02113925,
            0.00132904,
            0.00270719,
            0.00567207,
            0.0001369,
            0.00668861,
            0.00735136,
            0.00048563,
            0.00270623,
            0.00486821,
            0.03074534,
            0.0014593,
            0.00561172,
            0.00473769,
            0.00560528,
            0.00067681,
            0.01497427,
            0.00084121,
            0.00354908,
            0.02619859,
            0.00973237,
            0.00476371,
            0.00088827,
            0.00295503,
            0.01322995,
            0.01936212,
            0.01078059,
            0.00281038,
            0.00269666,
            0.01091767,
            0.00893086,
            0.03206584,
            0.01258918,
            0.00497573,
            0.01822315,
            0.03937057,
            0.00976562,
            0.00331421,
            0.00606718,
            0.01002473,
            0.01228917,
            0.00763452,
            0.00235901,
            0.01066404,
            0.01109757,
            0.02292789,
            0.00136971,
            0.0023765,
        ],
    )


@pytest.mark.parametrize("connector", (pq.NumpyConnector(), pq.JaxConnector()))
def test_LossyInterferometer_fock_probabilities(connector):
    U = np.array(
        [
            [
                -0.17959207 - 0.29175972j,
                -0.64550941 - 0.02897055j,
                -0.023922 - 0.38854671j,
                -0.07908932 + 0.35617293j,
                -0.39779191 + 0.14902272j,
            ],
            [
                -0.36896208 + 0.19468375j,
                -0.11545557 + 0.20434514j,
                0.25548079 + 0.05220164j,
                -0.51002161 + 0.38442256j,
                0.48106678 - 0.25210091j,
            ],
            [
                0.25912844 + 0.16131742j,
                0.11886251 + 0.12632645j,
                0.69028213 - 0.25734432j,
                0.01276639 + 0.05841739j,
                0.03713264 + 0.57364845j,
            ],
            [
                -0.20314019 - 0.18973473j,
                0.59146854 + 0.28605532j,
                -0.11096495 - 0.26870144j,
                -0.47290354 - 0.0489408j,
                -0.42459838 + 0.01554643j,
            ],
            [
                -0.5021973 - 0.53474291j,
                0.24524545 - 0.0741398j,
                0.37786104 + 0.10225255j,
                0.46696955 + 0.10636677j,
                0.07171789 - 0.09194236j,
            ],
        ]
    )

    singular_values = np.array([0.9, 0.8, 0.7, 0.6, 0.5])

    lossy_interferometer_matrix = U @ np.diag(singular_values) @ U @ U.T

    with pq.Program() as program:
        pq.Q(all) | pq.StateVector([2, 1, 1, 0, 1])

        pq.Q(all) | pq.LossyInterferometer(lossy_interferometer_matrix)

    simulator = pq.SamplingSimulator(
        d=5, connector=connector, config=pq.Config(cutoff=6)
    )
    state = simulator.execute(program).state

    assert np.allclose(
        state.fock_probabilities,
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.00000817,
            0.00001853,
            0.00011531,
            0.00000414,
            0.00015421,
            0.00000895,
            0.00015489,
            0.00000074,
            0.00028061,
            0.00018395,
            0.00009286,
            0.0005873,
            0.00000329,
            0.00010945,
            0.00055886,
            0.00000038,
            0.00001363,
            0.00000067,
            0.00007211,
            0.00004254,
            0.0000026,
            0.00061655,
            0.00000101,
            0.00000061,
            0.00110988,
            0.00015013,
            0.00029921,
            0.00044755,
            0.00007452,
            0.00085563,
            0.00001532,
            0.0000001,
            0.00012006,
            0.00058028,
            0.00054547,
            0.0000063,
            0.00005692,
            0.00000133,
            0.00001646,
            0.00006361,
            0.0000311,
            0.00016344,
            0.00000034,
            0.00001476,
            0.00053404,
            0.0004333,
            0.00024504,
            0.00029713,
            0.00000085,
            0.00018765,
            0.00100461,
            0.0000003,
            0.00000541,
            0.00004598,
            0.00237147,
            0.00037026,
            0.00031803,
            0.00000723,
            0.00023062,
            0.0000086,
            0.00034283,
            0.00000409,
            0.00121991,
            0.00036429,
            0.00023933,
            0.00000002,
            0.00000252,
            0.0012302,
            0.00053479,
            0.00220692,
            0.00000628,
            0.00014024,
            0.00000078,
            0.00009678,
            0.00059082,
            0.00001539,
            0.00050913,
            0.00000096,
            0.00001018,
            0.00014861,
            0.00061172,
            0.00006556,
            0.00010699,
            0.00004406,
            0.00005206,
            0.00150149,
            0.00000042,
            0.00002822,
            0.00003041,
            0.0019066,
            0.00044064,
            0.00008295,
            0.00010511,
            0.00045442,
            0.00003943,
            0.00103867,
            0.00001407,
            0.00038873,
            0.00031623,
            0.0003676,
            0.00000003,
            0.00001066,
            0.00004472,
            0.00016568,
            0.00145667,
            0.00016119,
            0.00005173,
            0.00007859,
            0.00045526,
            0.00017394,
            0.00016566,
            0.00010343,
            0.00002395,
            0.00013923,
            0.0001394,
            0.00000056,
            0.00013875,
            0.00231979,
            0.00102331,
            0.0003841,
            0.0,
            0.00000047,
            0.00004096,
            0.00296666,
            0.00278055,
            0.00000124,
        ],
    )


@pytest.mark.parametrize("connector", (pq.NumpyConnector(), pq.JaxConnector()))
def test_Interferometer_state_vector(connector):
    U = np.array(
        [
            [
                -0.17959207 - 0.29175972j,
                -0.64550941 - 0.02897055j,
                -0.023922 - 0.38854671j,
                -0.07908932 + 0.35617293j,
                -0.39779191 + 0.14902272j,
            ],
            [
                -0.36896208 + 0.19468375j,
                -0.11545557 + 0.20434514j,
                0.25548079 + 0.05220164j,
                -0.51002161 + 0.38442256j,
                0.48106678 - 0.25210091j,
            ],
            [
                0.25912844 + 0.16131742j,
                0.11886251 + 0.12632645j,
                0.69028213 - 0.25734432j,
                0.01276639 + 0.05841739j,
                0.03713264 + 0.57364845j,
            ],
            [
                -0.20314019 - 0.18973473j,
                0.59146854 + 0.28605532j,
                -0.11096495 - 0.26870144j,
                -0.47290354 - 0.0489408j,
                -0.42459838 + 0.01554643j,
            ],
            [
                -0.5021973 - 0.53474291j,
                0.24524545 - 0.0741398j,
                0.37786104 + 0.10225255j,
                0.46696955 + 0.10636677j,
                0.07171789 - 0.09194236j,
            ],
        ]
    )

    with pq.Program() as program:
        pq.Q(all) | pq.StateVector([2, 1, 1, 0, 1])

        pq.Q(all) | pq.Interferometer(U)

    simulator = pq.SamplingSimulator(
        d=5, connector=connector, config=pq.Config(cutoff=6)
    )
    state = simulator.execute(program).state

    assert np.allclose(
        state.state_vector,
        [
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.09673635 + 0.00894129j,
            -0.04054607 - 0.08877005j,
            -0.04103266 + 0.04519354j,
            0.10191569 - 0.02357385j,
            0.13979208 + 0.02895795j,
            -0.01888176 + 0.08279288j,
            0.09212894 - 0.06540282j,
            -0.04172277 - 0.05094306j,
            -0.03922737 - 0.02886168j,
            0.04815971 - 0.02147865j,
            -0.04106801 + 0.03871252j,
            0.03208992 + 0.017294j,
            0.02935509 - 0.05580493j,
            0.09926288 - 0.01036311j,
            0.03238299 + 0.10770402j,
            0.03767363 - 0.02800021j,
            -0.13936493 - 0.08312529j,
            0.01296681 + 0.03194278j,
            0.02218824 + 0.02097366j,
            0.00285286 - 0.00593152j,
            0.00638718 - 0.00780582j,
            0.04389152 - 0.18596456j,
            -0.0092526 + 0.01061715j,
            0.02310208 + 0.0172228j,
            0.05268903 + 0.02864227j,
            -0.11634251 + 0.03911237j,
            0.04941317 - 0.05398884j,
            0.09468741 - 0.0121538j,
            0.00575399 + 0.01134964j,
            -0.02631801 - 0.02592898j,
            0.12460946 - 0.0605621j,
            -0.05448323 - 0.05280389j,
            -0.02899584 - 0.06253695j,
            -0.00722894 + 0.05356003j,
            -0.08055263 + 0.10940579j,
            -0.03533223 + 0.03726951j,
            -0.0153757 + 0.0995802j,
            0.02285402 + 0.00482406j,
            -0.09528935 + 0.03330792j,
            0.01244704 - 0.02841061j,
            0.01017852 + 0.00300564j,
            -0.09503368 - 0.02015217j,
            0.00262078 - 0.04339833j,
            0.00115694 + 0.00226246j,
            -0.15222472 - 0.07220082j,
            0.00258734 + 0.11948791j,
            -0.06004491 - 0.0483453j,
            -0.014552 - 0.07881396j,
            -0.05293484 + 0.04112639j,
            -0.05207777 + 0.06764286j,
            0.04795327 - 0.03470828j,
            0.01564814 + 0.03626594j,
            0.07170731 - 0.00205998j,
            0.05293314 + 0.02050252j,
            -0.03531672 - 0.1251812j,
            0.09938568 - 0.04892893j,
            0.00278706 + 0.06139628j,
            -0.16509461 + 0.06832783j,
            -0.03029048 - 0.01599165j,
            0.00372036 - 0.08173363j,
            0.06759556 - 0.07016625j,
            0.05138618 - 0.02627613j,
            -0.00171715 - 0.050284j,
            -0.04719134 - 0.06133206j,
            0.06241287 + 0.05981589j,
            -0.081195 - 0.02144467j,
            -0.12094764 - 0.06574337j,
            -0.03940359 - 0.06672962j,
            -0.03880635 - 0.02209286j,
            -0.03293082 - 0.1268082j,
            0.03014527 + 0.03315379j,
            0.056574 - 0.01222106j,
            0.02703015 - 0.0535755j,
            -0.01439755 + 0.06286608j,
            -0.02898274 - 0.03035343j,
            -0.04553986 - 0.02516058j,
            0.01158844 + 0.04956733j,
            -0.00579514 + 0.02324307j,
            0.14517702 + 0.0079295j,
            -0.02968546 + 0.02116155j,
            0.03477037 + 0.0387068j,
            -0.00724049 + 0.07496429j,
            0.00511774 - 0.01052191j,
            0.07513316 + 0.03230515j,
            0.06204672 - 0.059174j,
            0.01063188 - 0.01930268j,
            -0.01776556 - 0.04889393j,
            -0.04444004 - 0.05378935j,
            0.10684527 + 0.13903031j,
            0.03714073 + 0.00893685j,
            0.02064453 - 0.07201059j,
            0.03549685 - 0.05897168j,
            -0.04840973 + 0.057112j,
            -0.02052664 + 0.01598331j,
            -0.10280442 + 0.06637411j,
            -0.02438802 + 0.0156981j,
            -0.05275449 + 0.02767753j,
            -0.08307958 + 0.13891138j,
            -0.02315128 + 0.09589779j,
            0.01848979 + 0.06649691j,
            0.01622799 + 0.02499844j,
            0.04684269 - 0.02758248j,
            0.0700926 - 0.09119745j,
            0.00995687 + 0.13879115j,
            0.05625492 + 0.08726952j,
            -0.05290853 + 0.00332711j,
            -0.03858649 + 0.03475264j,
            0.09125975 + 0.0508854j,
            0.08494523 - 0.04141455j,
            0.16547981 - 0.06842714j,
            -0.00080189 - 0.11219863j,
            -0.05324175 + 0.0462714j,
            -0.12180439 + 0.05819656j,
            -0.19461921 + 0.03865142j,
            -0.09132539 + 0.0377531j,
            0.04244472 - 0.03889284j,
            0.03578853 - 0.06918352j,
            -0.07031619 - 0.07127664j,
            -0.08557901 - 0.07046565j,
            -0.08638655 + 0.01311052j,
            -0.04851828 + 0.00223239j,
            -0.10021305 - 0.02492763j,
            -0.04712397 - 0.0942173j,
            0.08954955 - 0.12210147j,
            0.02103819 - 0.03044837j,
            0.03741394 + 0.03125221j,
        ],
    )


@pytest.mark.parametrize("connector", (pq.NumpyConnector(), pq.JaxConnector()))
def test_LossyInterferometer_state_vector(connector):
    U = np.array(
        [
            [
                -0.17959207 - 0.29175972j,
                -0.64550941 - 0.02897055j,
                -0.023922 - 0.38854671j,
                -0.07908932 + 0.35617293j,
                -0.39779191 + 0.14902272j,
            ],
            [
                -0.36896208 + 0.19468375j,
                -0.11545557 + 0.20434514j,
                0.25548079 + 0.05220164j,
                -0.51002161 + 0.38442256j,
                0.48106678 - 0.25210091j,
            ],
            [
                0.25912844 + 0.16131742j,
                0.11886251 + 0.12632645j,
                0.69028213 - 0.25734432j,
                0.01276639 + 0.05841739j,
                0.03713264 + 0.57364845j,
            ],
            [
                -0.20314019 - 0.18973473j,
                0.59146854 + 0.28605532j,
                -0.11096495 - 0.26870144j,
                -0.47290354 - 0.0489408j,
                -0.42459838 + 0.01554643j,
            ],
            [
                -0.5021973 - 0.53474291j,
                0.24524545 - 0.0741398j,
                0.37786104 + 0.10225255j,
                0.46696955 + 0.10636677j,
                0.07171789 - 0.09194236j,
            ],
        ]
    )

    singular_values = np.array([0.9, 0.8, 0.7, 0.6, 0.5])

    lossy_interferometer_matrix = U @ np.diag(singular_values) @ U @ U.T

    with pq.Program() as program:
        pq.Q(all) | pq.StateVector([2, 1, 1, 0, 1])

        pq.Q(all) | pq.LossyInterferometer(lossy_interferometer_matrix)

    simulator = pq.SamplingSimulator(
        d=5, connector=connector, config=pq.Config(cutoff=6)
    )
    state = simulator.execute(program).state

    assert np.allclose(
        state.state_vector,
        [
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            0.0 + 0.0j,
            -0.00281817 + 0.00047234j,
            0.0030107 + 0.0030767j,
            -0.0071165 - 0.00804144j,
            0.00020587 + 0.00202449j,
            -0.00705328 - 0.01022077j,
            0.00072304 - 0.00290309j,
            -0.00221838 + 0.01224598j,
            0.00043436 - 0.00074296j,
            -0.00733162 + 0.01506173j,
            0.00599109 - 0.01216783j,
            -0.00709928 + 0.00651579j,
            0.0111612 - 0.02151122j,
            0.00088202 - 0.00158449j,
            -0.00989059 + 0.00340992j,
            0.00950506 - 0.02164517j,
            0.00007245 + 0.0006141j,
            0.00330376 - 0.00164677j,
            0.0007624 + 0.00029027j,
            0.00815626 + 0.0023636j,
            -0.00478007 + 0.00443738j,
            -0.00011534 - 0.00160736j,
            -0.02482592 - 0.0004706j,
            -0.00099919 + 0.00008541j,
            0.00076367 + 0.00016924j,
            -0.03252417 - 0.00721498j,
            -0.00744291 + 0.00973309j,
            -0.01729086 - 0.00048719j,
            -0.01235259 + 0.0171746j,
            0.00862545 - 0.00034692j,
            -0.02359351 - 0.01729088j,
            -0.00391357 + 0.00003685j,
            0.00029066 + 0.00013309j,
            0.01050288 + 0.00312311j,
            -0.00988854 - 0.02196587j,
            0.01520206 - 0.01773044j,
            -0.00015084 - 0.00250534j,
            0.00072269 + 0.00751015j,
            -0.00089424 - 0.00072759j,
            0.00216855 + 0.00342902j,
            -0.00271967 - 0.00749732j,
            0.00259268 + 0.0049375j,
            -0.0108486 + 0.00676383j,
            -0.00010457 - 0.00057391j,
            0.00127792 + 0.0036237j,
            -0.01471753 + 0.01781664j,
            0.01008493 + 0.01820964j,
            -0.00120967 - 0.015607j,
            0.01629768 + 0.00561355j,
            -0.00072571 + 0.000567j,
            0.00045079 - 0.01369123j,
            0.00960089 - 0.03020651j,
            -0.00053661 - 0.00012751j,
            -0.00060879 - 0.00224483j,
            0.00007918 - 0.00678013j,
            0.00065613 - 0.04869337j,
            0.01683377 - 0.00932129j,
            -0.00979048 + 0.01490572j,
            -0.00160943 + 0.0021533j,
            0.00904341 + 0.01219972j,
            -0.00271978 + 0.00109625j,
            -0.01849409 - 0.00089284j,
            0.00173941 + 0.00102961j,
            0.00729095 + 0.03415771j,
            0.01894997 - 0.00227724j,
            0.01315883 - 0.00813454j,
            -0.00003065 + 0.00012507j,
            0.00082674 + 0.00135548j,
            -0.00419386 + 0.03482251j,
            0.02080074 + 0.01010535j,
            0.04662135 + 0.00577662j,
            -0.00218697 + 0.00122333j,
            0.010754 - 0.00495878j,
            0.00048692 + 0.00073791j,
            0.00880394 - 0.00438944j,
            -0.02390813 + 0.00438465j,
            -0.00187081 - 0.00344828j,
            -0.02048361 + 0.00946342j,
            -0.00066058 + 0.0007222j,
            -0.00192496 - 0.00254394j,
            -0.00574156 + 0.01075394j,
            0.0145063 + 0.02003223j,
            0.00207145 + 0.00782771j,
            -0.00674893 + 0.00783833j,
            0.00442578 - 0.00494723j,
            0.00525254 + 0.00494692j,
            -0.03510743 - 0.01640001j,
            0.00040596 + 0.00050153j,
            0.00425541 - 0.00318008j,
            0.00548487 + 0.00057022j,
            -0.03766909 - 0.02208253j,
            0.01118593 - 0.01776277j,
            0.00320455 - 0.00852527j,
            -0.0016089 + 0.01012518j,
            -0.01426275 + 0.01584286j,
            -0.00533952 + 0.00330468j,
            -0.02457244 + 0.02085346j,
            -0.00224603 - 0.0030044j,
            -0.01522553 + 0.01252651j,
            -0.01216694 + 0.01296886j,
            -0.01488974 - 0.01207889j,
            0.00013844 - 0.00010394j,
            -0.00128497 - 0.00300191j,
            -0.00472499 + 0.00473263j,
            -0.0062335 + 0.01126144j,
            0.01666868 - 0.034334j,
            -0.01090621 - 0.00649936j,
            -0.00120187 + 0.00709132j,
            0.00719829 + 0.0051748j,
            0.01581881 - 0.01431871j,
            0.01197423 - 0.00552751j,
            0.00618452 + 0.01128755j,
            0.00537981 + 0.00863085j,
            -0.0048938 + 0.00001433j,
            0.0072979 - 0.00927218j,
            -0.00865039 - 0.00803563j,
            -0.00061948 + 0.00042168j,
            0.00339848 + 0.01127834j,
            -0.04768346 + 0.00678842j,
            -0.03091322 - 0.00822705j,
            -0.00764288 - 0.01804669j,
            -0.00001406 - 0.0000184j,
            -0.0006406 + 0.00023521j,
            0.0000544 + 0.00639943j,
            -0.05426451 - 0.00469253j,
            -0.05076466 - 0.01426528j,
            -0.00088494 - 0.00067758j,
        ],
    )

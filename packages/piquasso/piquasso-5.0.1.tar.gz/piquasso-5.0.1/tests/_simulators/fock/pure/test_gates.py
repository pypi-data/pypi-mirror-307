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

import numpy as np

import piquasso as pq


def test_beamsplitter_with_theta_pi_over_4():
    with pq.Program() as program:
        pq.Q(1) | pq.StateVector([1])

        pq.Q(0, 1) | pq.Beamsplitter(theta=np.pi / 4, phi=np.pi / 3)

    simulator = pq.PureFockSimulator(d=2, config=pq.Config(cutoff=3))

    state = simulator.execute(program).state

    assert np.allclose(
        state.fock_probabilities,
        [0, 0.5, 0.5, 0, 0, 0],
    )


def test_beamsplitter5050_equivalence():
    with pq.Program() as preparation:
        pq.Q() | pq.Vacuum()

        pq.Q(0) | pq.Displacement(r=0.1, phi=np.pi / 5)
        pq.Q(1) | pq.Squeezing(r=0.1, phi=np.pi / 5)
        pq.Q(0, 1) | pq.Beamsplitter(theta=np.pi / 7, phi=np.pi / 11)

    with pq.Program() as program_with_parametrized_beamsplitter:
        pq.Q() | preparation

        pq.Q(0, 1) | pq.Beamsplitter(theta=np.pi / 4, phi=0.0)

    with pq.Program() as program_with_50_50_beamsplitter:
        pq.Q() | preparation

        pq.Q(0, 1) | pq.Beamsplitter5050()

    simulator = pq.PureFockSimulator(d=2, config=pq.Config(cutoff=5))

    state_with_parametrized_beamsplitter = simulator.execute(
        program_with_parametrized_beamsplitter
    ).state

    state_with_50_50_beamsplitter = simulator.execute(
        program_with_50_50_beamsplitter
    ).state

    assert state_with_50_50_beamsplitter == state_with_parametrized_beamsplitter


def test_beamsplitter():
    with pq.Program() as program:
        pq.Q(1) | 1 * pq.StateVector([1])

        pq.Q(0, 1) | pq.Beamsplitter(theta=np.pi / 5, phi=np.pi / 6)

    simulator = pq.PureFockSimulator(d=2, config=pq.Config(cutoff=3))

    state = simulator.execute(program).state

    assert np.allclose(
        state.fock_probabilities,
        [0.0, 0.3454915, 0.6545085, 0.0, 0.0, 0.0],
    )


def test_beamsplitter_multiple_particles():
    with pq.Program() as program:
        pq.Q(1) | pq.StateVector([1]) / 2
        pq.Q(1) | pq.StateVector([2]) / 2
        pq.Q(0) | pq.StateVector([2]) / np.sqrt(2)

        pq.Q(0, 1) | pq.Beamsplitter(theta=np.pi / 5, phi=np.pi / 6)

    simulator = pq.PureFockSimulator(d=2, config=pq.Config(cutoff=3))

    state = simulator.execute(program).state

    assert np.isclose(sum(state.fock_probabilities), 1)
    assert np.allclose(
        state.fock_probabilities,
        [0.0, 0.08637288, 0.16362712, 0.32397979, 0.17929466, 0.24672554],
    )


def test_beamsplitter_leaves_vacuum_unchanged():
    with pq.Program() as program:
        pq.Q() | pq.StateVector([0, 0]) / 2
        pq.Q() | pq.StateVector([0, 1]) / np.sqrt(2)
        pq.Q() | pq.StateVector([0, 2]) / 2

        pq.Q(0, 1) | pq.Beamsplitter(theta=np.pi / 5, phi=np.pi / 6)

    simulator = pq.PureFockSimulator(d=2, config=pq.Config(cutoff=3))

    state = simulator.execute(program).state

    assert np.isclose(sum(state.fock_probabilities), 1)
    assert np.allclose(
        state.fock_probabilities,
        [0.25, 0.17274575, 0.32725425, 0.02984109, 0.11306356, 0.10709534],
    )


def test_multiple_beamsplitters():
    with pq.Program() as program:
        pq.Q(2) | pq.StateVector([1]) * 1

        pq.Q(0, 1) | pq.Beamsplitter(theta=np.pi / 4, phi=np.pi / 5)
        pq.Q(1, 2) | pq.Beamsplitter(theta=np.pi / 6, phi=1.5 * np.pi)

    simulator = pq.PureFockSimulator(d=3, config=pq.Config(cutoff=3))

    state = simulator.execute(program).state

    assert np.allclose(
        state.fock_probabilities,
        [0.0, 0.0, 0.25, 0.75, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    )


def test_multiple_beamsplitters_with_multiple_particles():
    with pq.Program() as program:
        pq.Q() | pq.StateVector([0, 0, 1]) / 2
        pq.Q() | pq.StateVector([0, 0, 2]) / 2
        pq.Q() | pq.StateVector([0, 1, 1]) / np.sqrt(2)

        pq.Q(0, 1) | pq.Beamsplitter(theta=np.pi / 4, phi=np.pi / 5)
        pq.Q(1, 2) | pq.Beamsplitter(theta=np.pi / 6, phi=1.5 * np.pi)

    simulator = pq.PureFockSimulator(d=3, config=pq.Config(cutoff=3))

    state = simulator.execute(program).state

    assert np.isclose(sum(state.fock_probabilities), 1)
    assert np.allclose(
        state.fock_probabilities,
        [0.0, 0.0, 0.0625, 0.1875, 0.0, 0.0625, 0.1875, 0.109375, 0.15625, 0.234375],
    )


def test_phaseshift():
    with pq.Program() as program:
        pq.Q() | pq.StateVector([0, 1]) / 2
        pq.Q() | pq.StateVector([0, 2]) / np.sqrt(2)
        pq.Q() | pq.StateVector([1, 1]) / 2

        pq.Q(0) | pq.Phaseshifter(phi=np.pi / 3)

    simulator = pq.PureFockSimulator(d=2, config=pq.Config(cutoff=3))

    state = simulator.execute(program).state

    assert np.isclose(sum(state.fock_probabilities), 1)
    assert np.allclose(
        state.fock_probabilities,
        [0.0, 0.0, 0.25, 0.0, 0.25, 0.5],
    )


def test_fourier():
    with pq.Program() as program:
        pq.Q() | pq.StateVector([0, 1]) / 2
        pq.Q() | pq.StateVector([0, 2]) / np.sqrt(2)
        pq.Q() | pq.StateVector([1, 1]) / 2

        pq.Q(0) | pq.Fourier()

    simulator = pq.PureFockSimulator(d=2, config=pq.Config(cutoff=3))

    state = simulator.execute(program).state

    assert np.isclose(sum(state.fock_probabilities), 1)
    assert np.allclose(
        state.fock_probabilities,
        [0.0, 0.0, 0.25, 0.0, 0.25, 0.5],
    )


def test_mach_zehnder():
    with pq.Program() as program:
        pq.Q() | pq.StateVector([0, 1]) / 2
        pq.Q() | pq.StateVector([0, 2]) / np.sqrt(2)
        pq.Q() | pq.StateVector([1, 1]) / 2

        pq.Q(0, 1) | pq.MachZehnder(int_=np.pi / 3, ext=np.pi / 4)

    simulator = pq.PureFockSimulator(d=2, config=pq.Config(cutoff=3))

    state = simulator.execute(program).state

    assert np.isclose(sum(state.fock_probabilities), 1)
    assert np.allclose(
        state.fock_probabilities,
        [0.0, 0.1875, 0.0625, 0.60463966, 0.09690689, 0.04845345],
    )


def test_beamsplitters_and_phaseshifters_with_multiple_particles():
    with pq.Program() as program:
        pq.Q() | pq.StateVector([0, 0, 1]) / 2
        pq.Q() | pq.StateVector([0, 0, 2]) / 2
        pq.Q() | pq.StateVector([0, 1, 1]) / np.sqrt(2)

        pq.Q(0) | pq.Phaseshifter(phi=np.pi / 3)
        pq.Q(1) | pq.Phaseshifter(phi=np.pi / 3)

        pq.Q(0, 1) | pq.Beamsplitter(theta=np.pi / 4, phi=4 * np.pi / 5)
        pq.Q(1, 2) | pq.Beamsplitter(theta=np.pi / 6, phi=3 * np.pi / 2)

    simulator = pq.PureFockSimulator(d=3, config=pq.Config(cutoff=3))

    state = simulator.execute(program).state

    assert np.isclose(sum(state.fock_probabilities), 1)
    assert np.allclose(
        state.fock_probabilities,
        [
            0.0,
            0.0,
            0.0625,
            0.1875,
            0.0,
            0.0625,
            0.1875,
            0.04308374,
            0.02366748,
            0.43324878,
        ],
    )


def test_interferometer():
    T = np.array(
        [
            [0.5, 0.53033009 + 0.53033009j, 0.21650635 + 0.375j],
            [-0.61237244 + 0.61237244j, 0.4330127, 0.24148146 + 0.06470476j],
            [0, -0.48296291 + 0.12940952j, 0.8660254],
        ]
    )

    with pq.Program() as program:
        pq.Q() | pq.StateVector([0, 0, 1]) / 2
        pq.Q() | pq.StateVector([0, 0, 2]) / 2
        pq.Q() | pq.StateVector([0, 1, 1]) / np.sqrt(2)

        pq.Q(0, 1, 2) | pq.Interferometer(matrix=T)

    simulator = pq.PureFockSimulator(d=3, config=pq.Config(cutoff=3))

    state = simulator.execute(program).state

    assert np.isclose(sum(state.fock_probabilities), 1)
    assert np.allclose(
        state.fock_probabilities,
        [
            0.0,
            0.046875,
            0.015625,
            0.1875,
            0.17307537,
            0.11538358,
            0.32090931,
            0.0192306,
            0.10696977,
            0.01443139,
        ],
    )


def test_kerr():
    xi = np.pi / 3

    with pq.Program() as program:
        pq.Q() | pq.StateVector([0, 2, 1])

        pq.Q(1) | pq.Kerr(xi=xi)

    simulator = pq.PureFockSimulator(d=3, config=pq.Config(cutoff=4))

    state = simulator.execute(program).state

    # TODO: Better way of presenting the resulting state.
    nonzero_elements = list(state.nonzero_elements)

    assert len(nonzero_elements) == 1

    assert np.isclose(nonzero_elements[0][0], -np.exp(1j * np.pi / 3))
    assert nonzero_elements[0][1] == (0, 2, 1)


def test_cross_kerr():
    with pq.Program() as program:
        pq.Q() | pq.StateVector([0, 2, 1])

        pq.Q(1, 2) | pq.CrossKerr(xi=np.pi / 2)

    simulator = pq.PureFockSimulator(d=3, config=pq.Config(cutoff=4))

    state = simulator.execute(program).state

    # TODO: Better way of presenting the resulting state.
    nonzero_elements = list(state.nonzero_elements)

    assert len(nonzero_elements) == 1

    assert np.isclose(nonzero_elements[0][0], -1)
    assert nonzero_elements[0][1] == (0, 2, 1)


def test_cubic_phase():
    with pq.Program() as program:
        pq.Q() | pq.Vacuum()

        pq.Q(0) | pq.CubicPhase(gamma=0.1)

    simulator = pq.PureFockSimulator(d=1, config=pq.Config(cutoff=5))
    state = simulator.execute(program).state

    nonzero_elements = list(state.nonzero_elements)

    assert len(nonzero_elements) == 5.0

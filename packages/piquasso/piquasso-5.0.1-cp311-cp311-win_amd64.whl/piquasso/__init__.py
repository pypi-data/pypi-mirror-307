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

"""The Piquasso module.

One can access all the instructions and states from here as attributes.
"""


# start delvewheel patch
def _delvewheel_patch_1_8_3():
    import os
    if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'piquasso.libs'))):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_8_3()
del _delvewheel_patch_1_8_3
# end delvewheel patch

from piquasso import cvqnn
from piquasso import fermionic

from piquasso.api.mode import Q
from piquasso.api.config import Config
from piquasso.api.instruction import (
    Instruction,
    Preparation,
    Gate,
    Measurement,
)
from piquasso.api.program import Program
from piquasso.api.state import State
from piquasso.api.computer import Computer
from piquasso.api.simulator import Simulator
from piquasso.api.utils import as_code

from piquasso._simulators.sampling import SamplingState, SamplingSimulator

from piquasso._simulators.gaussian import GaussianState, GaussianSimulator
from piquasso._simulators.fock import (
    FockState,
    PureFockState,
    BatchPureFockState,
    FockSimulator,
    PureFockSimulator,
)

from piquasso._simulators.connectors import (
    NumpyConnector,
    TensorflowConnector,
    JaxConnector,
)

from .instructions.preparations import (
    Vacuum,
    Mean,
    Covariance,
    Thermal,
    StateVector,
    DensityMatrix,
    Create,
    Annihilate,
)

from .instructions.gates import (
    GaussianTransform,
    Phaseshifter,
    Beamsplitter,
    Beamsplitter5050,
    MachZehnder,
    Fourier,
    Displacement,
    PositionDisplacement,
    MomentumDisplacement,
    Squeezing,
    QuadraticPhase,
    Squeezing2,
    Kerr,
    CrossKerr,
    ControlledX,
    ControlledZ,
    Interferometer,
    Graph,
    CubicPhase,
)

from .instructions.measurements import (
    ParticleNumberMeasurement,
    ThresholdMeasurement,
    HomodyneMeasurement,
    HeterodyneMeasurement,
    GeneraldyneMeasurement,
    PostSelectPhotons,
    ImperfectPostSelectPhotons,
)

from .instructions.channels import (
    DeterministicGaussianChannel,
    Attenuator,
    Loss,
    LossyInterferometer,
)

from .instructions.batch import (
    BatchPrepare,
    BatchApply,
)


__all__ = [
    # API
    "Program",
    "Q",
    "Config",
    "Instruction",
    "Preparation",
    "Gate",
    "Measurement",
    "State",
    "Computer",
    "Simulator",
    "as_code",
    # Simulators
    "GaussianSimulator",
    "SamplingSimulator",
    "FockSimulator",
    "PureFockSimulator",
    # Connectors
    "NumpyConnector",
    "TensorflowConnector",
    "JaxConnector",
    # States
    "GaussianState",
    "SamplingState",
    "FockState",
    "PureFockState",
    "BatchPureFockState",
    # Preparations
    "Vacuum",
    "Mean",
    "Covariance",
    "Thermal",
    "StateVector",
    "DensityMatrix",
    "Create",
    "Annihilate",
    # Gates
    "GaussianTransform",
    "Phaseshifter",
    "Beamsplitter",
    "Beamsplitter5050",
    "MachZehnder",
    "Fourier",
    "Displacement",
    "PositionDisplacement",
    "MomentumDisplacement",
    "Squeezing",
    "QuadraticPhase",
    "Squeezing2",
    "Kerr",
    "CrossKerr",
    "CubicPhase",
    "ControlledX",
    "ControlledZ",
    "Interferometer",
    "Graph",
    # Measurements
    "ParticleNumberMeasurement",
    "ThresholdMeasurement",
    "HomodyneMeasurement",
    "HeterodyneMeasurement",
    "GeneraldyneMeasurement",
    "PostSelectPhotons",
    "ImperfectPostSelectPhotons",
    # Channels
    "DeterministicGaussianChannel",
    "Attenuator",
    "Loss",
    "LossyInterferometer",
    # Batch
    "BatchPrepare",
    "BatchApply",
    # Modules
    "cvqnn",
    "fermionic",
]

__version__ = "5.0.1"
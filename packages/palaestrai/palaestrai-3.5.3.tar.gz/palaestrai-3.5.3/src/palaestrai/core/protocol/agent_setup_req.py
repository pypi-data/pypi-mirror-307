from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from palaestrai.agent import SensorInformation, ActuatorInformation


@dataclass
class AgentSetupRequest:
    """Initializes the setup of an :class:`Agent`

    * Sender: :class:`SimulationController`
    * Receiver: :class:`AgentConductor`

    Parameters
    ----------
    sender_simulation_controller : str
        ID of the sending :class:`SimulationController`
    receiver_agent_conductor : str
        ID of the receiving :class:`AgentConductor`
    experiment_run_id : str
        ID of the experiment run the agent participates in
    experiment_run_instance_id : str
        ID of the ::`ExperimentRun` object instance
    experiment_run_phase : int
        Current phase number of the experiment run
    configuration : dict
        The complete agent configuration
    sensors : list of :class:`SensorInformation`
        List of :class:`SensorInformation` objects for the sensors available
        to the agent
    actuators : list of :class:`ActuatorInformation`
        List of of :class:`ActuatorInformation` objects for the
        actuators available to the agent
    rollout_worker_uid : str
        Unique ID of the agent we're setting up (e.g., a :class:`Muscle`).
        This UID is *generated* and used only internally (i.e., in the
        major domo broker) to distinguish several :class:`Muscle`s with the
        same name (e.g., for multi-worker setups).
    muscle_name : str, optional
        Name of the :class:`Agent` (if any). This is the user-defined name
        from the :class:`ExperimentRun` file. This should actually never be
        ``None``, but since this is checked in the :class:`ExperimentRun` file
        and the MDP does not require the Muscle's *name* (as opposed to its
        internal UID) to be set, this is defined as being optional here.
    """

    sender_simulation_controller: str
    receiver_agent_conductor: str
    experiment_run_id: str
    experiment_run_instance_id: str
    experiment_run_phase: int
    configuration: Dict
    sensors: List[SensorInformation]
    actuators: List[ActuatorInformation]
    rollout_worker_uid: str
    muscle_name: Optional[str]

    @property
    def sender(self):
        return self.sender_simulation_controller

    @property
    def receiver(self):
        return self.receiver_agent_conductor

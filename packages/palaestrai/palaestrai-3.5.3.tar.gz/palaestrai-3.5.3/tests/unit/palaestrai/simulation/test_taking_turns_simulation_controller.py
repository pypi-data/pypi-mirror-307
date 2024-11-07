from collections import defaultdict
from unittest.async_case import IsolatedAsyncioTestCase
from unittest.mock import patch, AsyncMock, MagicMock

import numpy as np

from palaestrai.core.protocol import (
    SimulationStartRequest,
    SimulationStartResponse,
    EnvironmentSetupRequest,
    EnvironmentSetupResponse,
    EnvironmentStartRequest,
    EnvironmentStartResponse,
    AgentSetupRequest,
    AgentSetupResponse,
    AgentUpdateRequest,
    AgentUpdateResponse,
    EnvironmentUpdateRequest,
    EnvironmentUpdateResponse,
    SimulationShutdownRequest,
    ShutdownRequest,
    ShutdownResponse,
)

from palaestrai.core import BasicState
from palaestrai.agent import (
    Agent,
    SensorInformation,
    ActuatorInformation,
    RewardInformation,
)
from palaestrai.simulation import TakingTurnsSimulationController
from palaestrai.experiment import EnvironmentTerminationCondition

from palaestrai.types import Mode, Discrete, Box, SimTime


class TestTakingTurnsSimulationController(IsolatedAsyncioTestCase):
    def test_unassigned_sensors_actuators(self):
        sc = TakingTurnsSimulationController(
            termination_conditions=[],
            environment_conductor_ids=[],
            agent_conductor_ids=["ac1", "ac2", "ac3"],
            agents={
                "ac1": {  # All sensors/actuators: Ok.
                    "sensors": [
                        "myenv.0",
                        "myenv.1",
                        "myenv.2",
                        "myenv.3",
                        "myenv.4",
                    ],
                    "actuators": [
                        "myenv.0",
                        "myenv.1",
                        "myenv.2",
                        "myenv.3",
                        "myenv.4",
                    ],
                },
                "ac2": {
                    "sensors": [
                        "myenv.0",  # Ok
                        "1sensor_without_envid",  # No env ID
                        "myenv.snesor_with_typo",  # Typo in sensor
                    ],
                    "actuators": [
                        "myemv.4",  # Typo in env
                        "myenv.6",  # Does not exist.
                    ],
                },
                "ac3": {  # Only a subset of available sensors/actuators, ok.
                    "sensors": ["myenv.0", "myenv.4"],
                    "actuators": ["myenv.0", "myenv.1", "myenv.4"],
                },
            },
            mode=Mode.TEST,  # Pun intended.
        )

        _sensors = [
            SensorInformation(0, Discrete(1), f"myenv.{i}") for i in range(5)
        ]
        _actuators = [
            ActuatorInformation(0, Discrete(1), f"myenv.{i}") for i in range(5)
        ]
        sc._sensors_available.update(
            {sensor.uid: sensor for sensor in _sensors}
        )
        sc._actuators_available.update(
            {actuator.uid: actuator for actuator in _actuators}
        )

        self.assertDictEqual(
            sc._unassigned_sensors_actuators(),
            {
                "ac2": (
                    {"1sensor_without_envid", "myenv.snesor_with_typo"},
                    {"myemv.4", "myenv.6"},
                )
            },
        )

    @patch(
        "palaestrai.core.event_state_machine.MajorDomoWorker",
        return_value=AsyncMock(
            transceive=AsyncMock(
                side_effect=[
                    SimulationStartRequest(
                        sender_run_governor_id="rg_id",
                        receiver_simulation_controller_id="sc_id",
                        experiment_run_id="er_id",
                        experiment_run_instance_id="er_i_id",
                        experiment_run_phase_id="er_p_id",
                        experiment_run_phase=47,
                        experiment_run_phase_configuration={},
                    ),
                    # SimulationStopRequest(sender="rg_id", receiver="sc_id"),
                ]
            )
        ),
    )
    @patch(
        "palaestrai.core.event_state_machine.MajorDomoClient",
        return_value=AsyncMock(
            send=AsyncMock(
                side_effect=[
                    EnvironmentSetupResponse(
                        sender_environment_conductor="ec1_id",
                        receiver_simulation_controller="sc_id",
                        environment_id="env1_id",
                        experiment_run_id="er_id",
                        experiment_run_instance_id="er_i_id",
                        experiment_run_phase=47,
                        environment_type="myenv1",
                        environment_parameters={},
                    ),
                    EnvironmentSetupResponse(
                        sender_environment_conductor="ec2_id",
                        receiver_simulation_controller="sc_id",
                        environment_id="env2_id",
                        experiment_run_id="er_id",
                        experiment_run_instance_id="er_i_id",
                        experiment_run_phase=47,
                        environment_type="myenv2",
                        environment_parameters={},
                    ),
                    EnvironmentStartResponse(
                        sender_environment="env1_id",
                        receiver_simulation_controller="sc_id",
                        experiment_run_id="er_id",
                        experiment_run_instance_id="er_i_id",
                        experiment_run_phase=47,
                        sensors=[
                            SensorInformation(
                                0, Discrete(1), f"myenv1.DiscSens-{i}"
                            )
                            for i in range(5)
                        ],
                        actuators=[
                            ActuatorInformation(
                                0, Discrete(1), f"myenv1.DiscAct-{i}"
                            )
                            for i in range(5)
                        ],
                    ),
                    EnvironmentStartResponse(
                        sender_environment="env2_id",
                        receiver_simulation_controller="sc_id",
                        experiment_run_id="er_id",
                        experiment_run_instance_id="er_i_id",
                        experiment_run_phase=47,
                        sensors=[
                            SensorInformation(
                                np.array([0.0], dtype=np.float32),
                                Box(low=[-float(i)], high=[float(i)]),
                                f"myenv2.BoxSens-{i}",
                            )
                            for i in range(5)
                        ],
                        actuators=[
                            ActuatorInformation(
                                np.array([0.0], dtype=np.float32),
                                Box(
                                    low=np.array([-float(i + 1.0)]),
                                    high=np.array([float(i + 1.0)]),
                                ),
                                f"myenv2.BoxAct-{i}",
                            )
                            for i in range(5)
                        ],
                    ),
                    AgentSetupResponse(
                        sender_agent_conductor="ac1_id",
                        receiver_simulation_controller="sc_id",
                        experiment_run_id="er_id",
                        experiment_run_instance_id="er_i_id",
                        experiment_run_phase=47,
                        agent_id="ag1_id",
                    ),
                    AgentSetupResponse(
                        sender_agent_conductor="ac2_id",
                        receiver_simulation_controller="sc_id",
                        experiment_run_id="er_id",
                        experiment_run_instance_id="er_i_id",
                        experiment_run_phase=47,
                        agent_id="ag2_id",
                    ),
                ]
            )
        ),
    )
    async def test_simulation_start_request(self, mock_client, mock_worker):
        ttsc = TakingTurnsSimulationController(
            termination_conditions=[],
            environment_conductor_ids=["ec1_id", "ec2_id"],
            agent_conductor_ids=["ac1_id", "ac2_id"],
            agents={
                "ac1_id": {  # All sensors/actuators: Ok.
                    "name": "ag1_id",
                    "brain": {"name": "ag1_Brain", "params": {}},
                    "muscle": {"name": "ag1_id", "params": {}},
                    "sensors": [f"myenv1.DiscSens-{i}" for i in range(5)],
                    "actuators": [f"myenv1.DiscAct-{i}" for i in range(5)],
                },
                "ac2_id": {
                    "name": "ag2_id",
                    "brain": {"name": "ag2_Brain", "params": {}},
                    "muscle": {"name": "ag2_id", "params": {}},
                    "sensors": [f"myenv2.BoxSens-{i}" for i in range(5)],
                    "actuators": [f"myenv2.BoxAct-{i}" for i in range(5)],
                },
            },
            mode=Mode.TEST,  # Pun intended.
        )
        ttsc._simulate = AsyncMock(
            side_effect=ttsc.stop
        )  # Don't simulate, just set up.
        await ttsc.run()
        # only take the mock_calls of first client as they all are the same client
        setup_client_calls = next(iter(ttsc.__esm__._mdp_clients.values()))[
            0
        ].mock_calls
        self.assertEqual(
            len(ttsc._environment_conductor_ids) * 2
            + len(ttsc._agent_conductor_ids),
            len(setup_client_calls),
        )
        self.assertEqual(
            [
                EnvironmentSetupRequest,
                EnvironmentSetupRequest,
                EnvironmentStartRequest,
                EnvironmentStartRequest,
                AgentSetupRequest,
                AgentSetupRequest,
            ],
            [x.args[1].__class__ for x in setup_client_calls],
        )
        self.assertIsInstance(
            ttsc.__esm__._mdp_worker.transceive.mock_calls[1].args[0],
            SimulationStartResponse,
        )
        ttsc._simulate.assert_called()

    @patch(
        "palaestrai.core.event_state_machine.MajorDomoClient",
        return_value=AsyncMock(
            send=AsyncMock(
                side_effect=[
                    AgentUpdateResponse(
                        sender_rollout_worker_id="ag1_id",
                        receiver_simulation_controller_id="sc_id",
                        experiment_run_id="er_id",
                        experiment_run_instance_id="er_i_id",
                        experiment_run_phase=47,
                        actuator_information=[
                            ActuatorInformation(
                                0, Discrete(1), f"myenv1.DiscAct-{i}"
                            )
                            for i in range(5)
                        ],
                        sensor_information=[],
                    ),
                    EnvironmentUpdateResponse(
                        sender_environment_id="ec1_id",
                        receiver_simulation_controller_id="sc_id",
                        experiment_run_id="er_id",
                        experiment_run_instance_id="er_i_id",
                        experiment_run_phase=47,
                        simtime=None,
                        done=False,
                        sensors=[
                            SensorInformation(
                                1, Discrete(4), f"myenv1.DiscSens-{i}"
                            )
                            for i in range(5)
                        ],
                        rewards=[
                            RewardInformation(
                                np.array([1.0], dtype=np.float32),
                                Box(
                                    low=[0.0],
                                    high=[10.0],
                                ),
                                "rew1",
                            )
                        ],
                    ),
                    EnvironmentUpdateResponse(
                        sender_environment_id="ec2_id",
                        receiver_simulation_controller_id="sc_id",
                        experiment_run_id="er_id",
                        experiment_run_instance_id="er_i_id",
                        experiment_run_phase=47,
                        simtime=None,
                        done=False,
                        sensors=[
                            SensorInformation(
                                np.array([1.0], dtype=np.float32),
                                Box(low=[0.0], high=[1.0]),
                                f"myenv2.BoxSens-{i}",
                            )
                            for i in range(5)
                        ],
                        rewards=[
                            RewardInformation(
                                np.array([7.0], dtype=np.float32),
                                Box(
                                    low=[0.0],
                                    high=[10.0],
                                ),
                                "rew2",
                            )
                        ],
                    ),
                    AgentUpdateResponse(
                        sender_rollout_worker_id="ag2_id",
                        receiver_simulation_controller_id="sc_id",
                        experiment_run_id="er_id",
                        experiment_run_instance_id="er_i_id",
                        experiment_run_phase=47,
                        actuator_information=[
                            ActuatorInformation(
                                np.array([0.0], dtype=np.float32),
                                Box(low=[-float(i)], high=[float(i)]),
                                f"myenv1.BoxAct-{i}",
                            )
                            for i in range(5)
                        ],
                        sensor_information=[],
                    ),
                    EnvironmentUpdateResponse(
                        sender_environment_id="ec1_id",
                        receiver_simulation_controller_id="sc_id",
                        experiment_run_id="er_id",
                        experiment_run_instance_id="er_i_id",
                        experiment_run_phase=47,
                        simtime=None,
                        done=True,
                        sensors=[
                            SensorInformation(
                                1, Discrete(2), f"myenv1.DiscSens-{i}"
                            )
                            for i in range(5)
                        ],
                        rewards=[
                            RewardInformation(
                                np.array([10.0], dtype=np.float32),
                                Box(
                                    low=[0.0],
                                    high=[10.0],
                                ),
                                "rew1",
                            )
                        ],
                    ),
                    EnvironmentUpdateResponse(
                        sender_environment_id="ec2_id",
                        receiver_simulation_controller_id="sc_id",
                        experiment_run_id="er_id",
                        experiment_run_instance_id="er_i_id",
                        experiment_run_phase=47,
                        simtime=None,
                        done=False,
                        sensors=[
                            SensorInformation(
                                [1.0],
                                Box(low=[0.0], high=[1.0]),
                                f"myenv2.BoxSens-{i}",
                            )
                            for i in range(5)
                        ],
                        rewards=[
                            RewardInformation(
                                np.array([8.0], dtype=np.float32),
                                Box(
                                    low=[0.0],
                                    high=[10.0],
                                ),
                                "rew2",
                            )
                        ],
                    ),
                    AgentUpdateResponse(
                        sender_rollout_worker_id="ZombieCow-1",
                        receiver_simulation_controller_id="sc_id",
                        experiment_run_id="er_id",
                        experiment_run_instance_id="er_i_id",
                        experiment_run_phase=47,
                        actuator_information=[],
                        sensor_information=[],
                    ),
                    AgentUpdateResponse(
                        sender_rollout_worker_id="ZombieCow-2",
                        receiver_simulation_controller_id="sc_id",
                        experiment_run_id="er_id",
                        experiment_run_instance_id="er_i_id",
                        experiment_run_phase=47,
                        actuator_information=[],
                        sensor_information=[],
                    ),
                ]
            )
        ),
    )
    async def test_simulate(self, mock_client):
        ttsc = TakingTurnsSimulationController(
            termination_conditions=[],
            environment_conductor_ids=["ec1_id", "ec2_id"],
            agent_conductor_ids=["ac1_id", "ac2_id"],
            agents={
                "ac1_id": {  # All sensors/actuators: Ok.
                    "name": "Zombie Herd No. 1",
                    "brain": {"name": "zombie_cows:Brain", "params": {}},
                    "muscle": {"name": "zombie_cows:Muscle", "params": {}},
                    "sensors": [f"myenv1.DiscSens-{i}" for i in range(5)],
                    "actuators": [f"myenv1.DiscAct-{i}" for i in range(5)],
                },
                "ac2_id": {
                    "name": "Zombie Herd No. 2",
                    "brain": {"name": "zombie_cows:Brain", "params": {}},
                    "muscle": {"name": "zombie_cows:Muscle", "params": {}},
                    "sensors": [f"myenv1.BoxSens-{i}" for i in range(5)],
                    "actuators": [f"myenv1.BoxAct-{i}" for i in range(5)],
                },
            },
            mode=Mode.TEST,  # Pun intended.
        )
        ttsc._state = BasicState.RUNNING
        ttsc._agents = {
            ac_id: Agent(
                uid=ag["name"],
                actuators=[],
                sensors=[],
                brain_classname="zombie_cows:Brain",
                brain_params={},
                brain=None,
                muscle_classname="zombie_cows:Muscle",
                muscles={f"ZombieCow-{i+1}": None},
                muscle_params={},
            )
            for i, (ac_id, ag) in enumerate(ttsc._agent_configurations.items())
        }
        ttsc._active_environments = {"myenv1", "myenv2"}
        ttsc._termination_conditions = [EnvironmentTerminationCondition()]
        ttsc._request_termination = MagicMock()
        await ttsc._simulate()
        mock_client.assert_called()
        # only take the mock_calls of first client as they all are the same client
        simulation_send_calls = next(iter(ttsc.__esm__._mdp_clients.values()))[
            0
        ].send.mock_calls
        self.assertIsInstance(
            simulation_send_calls[0].args[1], AgentUpdateRequest
        )
        self.assertEqual(
            simulation_send_calls[0].args[1].receiver, "ZombieCow-1"
        )
        self.assertIsInstance(
            simulation_send_calls[1].args[1], EnvironmentUpdateRequest
        )
        self.assertIsInstance(
            simulation_send_calls[2].args[1], EnvironmentUpdateRequest
        )
        self.assertIn(
            "myenv1",
            [
                r.receiver
                for r in [
                    simulation_send_calls[1].args[1],
                    simulation_send_calls[2].args[1],
                ]
            ],
        )
        self.assertIn(
            "myenv2",
            [
                r.receiver
                for r in [
                    simulation_send_calls[1].args[1],
                    simulation_send_calls[2].args[1],
                ]
            ],
        )
        self.assertIsInstance(
            simulation_send_calls[3].args[1], AgentUpdateRequest
        )
        self.assertEqual(
            simulation_send_calls[3].args[1].receiver, "ZombieCow-2"
        )
        self.assertIsInstance(
            simulation_send_calls[4].args[1], EnvironmentUpdateRequest
        )
        self.assertIsInstance(
            simulation_send_calls[5].args[1], EnvironmentUpdateRequest
        )
        self.assertIsInstance(
            simulation_send_calls[6].args[1], AgentUpdateRequest
        )
        self.assertIsInstance(
            simulation_send_calls[7].args[1], AgentUpdateRequest
        )

    def test_process_environment_update(self):
        ttsc = TakingTurnsSimulationController(
            termination_conditions=[],
            environment_conductor_ids=["ec1_id", "ec2_id"],
            agent_conductor_ids=["ac1_id", "ac2_id"],
            agents={
                "ac1_id": {  # All sensors/actuators: Ok.
                    "name": "ag1_id",
                    "brain": {"name": "ag1_Brain", "params": {}},
                    "muscle": {"name": "ag1_id", "params": {}},
                    "sensors": [f"myenv1.DiscSens-{i}" for i in range(5)],
                    "actuators": [f"myenv1.DiscAct-{i}" for i in range(5)],
                },
                "ac2_id": {
                    "name": "ag2_id",
                    "brain": {"name": "ag2_Brain", "params": {}},
                    "muscle": {"name": "ag2_id", "params": {}},
                    "sensors": [f"myenv1.BoxSens-{i}" for i in range(5)],
                    "actuators": [f"myenv1.BoxAct-{i}" for i in range(5)],
                },
            },
            mode=Mode.TEST,  # Pun intended.
        )
        ttsc._state = BasicState.RUNNING
        ttsc._agents = {
            ac_id: Agent(
                uid=ag["name"],
                actuators=[],
                sensors=[],
                brain=None,
                brain_params={},
                brain_classname="",
                muscles={},
                muscle_params={},
                muscle_classname="",
            )
            for ac_id, ag in ttsc._agent_configurations.items()
        }
        ttsc._active_environments = {"myenv1", "myenv2"}
        ttsc._termination_conditions = [EnvironmentTerminationCondition()]
        ttsc._request_termination = MagicMock()
        ttsc._simtimes = MagicMock()

        rewards_per_agent = defaultdict(list)
        env_updates = [
            EnvironmentUpdateResponse(
                sender_environment_id="ec1_id",
                receiver_simulation_controller_id="sc_id",
                experiment_run_id="er_id",
                experiment_run_instance_id="er_i_id",
                experiment_run_phase=47,
                simtime=None,
                done=False,
                sensors=[
                    SensorInformation(i, Discrete(6), f"myenv1.DiscSens-{i}")
                    for i in range(5)
                ],
                rewards=[
                    RewardInformation(
                        np.array([10.0], dtype=np.float32),
                        Box(
                            low=[0.0],
                            high=[10.0],
                        ),
                        "rew1",
                    )
                ],
            ),
            EnvironmentUpdateResponse(
                sender_environment_id="ec1_id",
                receiver_simulation_controller_id="sc_id",
                experiment_run_id="er_id",
                experiment_run_instance_id="er_i_id",
                experiment_run_phase=47,
                simtime=None,
                done=True,
                sensors=[
                    SensorInformation(2, Discrete(3), f"myenv1.DiscSens-{i}")
                    for i in range(5)
                ],
                rewards=[
                    RewardInformation(
                        np.array([10.0], dtype=np.float32),
                        Box(
                            low=[0.0],
                            high=[10.0],
                        ),
                        "rew2",
                    )
                ],
            ),
        ]
        agent = list(ttsc._agents.values())[0]
        current_sensor_readings, terminated = ttsc._process_environment_update(
            [env_updates[0]], rewards_per_agent, agent
        )
        self.assertTrue(ttsc._simtimes.update.called)
        self.assertFalse(terminated)

        self.assertEqual(len(current_sensor_readings), 5)
        for i, sensor_reading in enumerate(current_sensor_readings):
            self.assertEqual(sensor_reading.value, i)
        self.assertTrue(agent.uid in rewards_per_agent)
        self.assertEqual(rewards_per_agent[agent.uid][0].uid, "rew1")

        ttsc._simtimes = MagicMock()
        agent = list(ttsc._agents.values())[1]
        current_sensor_readings, terminated = ttsc._process_environment_update(
            [env_updates[1]], rewards_per_agent, agent
        )
        self.assertTrue(ttsc._simtimes.update.called)
        self.assertTrue(terminated)
        self.assertEqual(ttsc._state, BasicState.STOPPING)

        self.assertEqual(len(current_sensor_readings), 5)
        for sensor_reading in current_sensor_readings:
            self.assertEqual(sensor_reading.value, 2)
        self.assertTrue(agent.uid in rewards_per_agent)
        self.assertEqual(rewards_per_agent[agent.uid][0].uid, "rew2")

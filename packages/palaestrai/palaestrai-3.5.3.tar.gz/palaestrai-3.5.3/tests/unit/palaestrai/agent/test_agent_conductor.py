import unittest
from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch
from uuid import uuid4
from warnings import catch_warnings

from palaestrai.agent.actuator_information import ActuatorInformation
from palaestrai.agent.agent_conductor import AgentConductor
from palaestrai.agent.dummy_brain import DummyBrain
from palaestrai.agent.file_brain_dumper import FileBrainDumper
from palaestrai.agent import Learner
from palaestrai.agent.sensor_information import SensorInformation
from palaestrai.agent.store_brain_dumper import StoreBrainDumper
from palaestrai.core.protocol import (
    AgentSetupRequest,
    AgentSetupResponse,
    ShutdownRequest,
)


class TestAgentConductor(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.agent_params = {
            "name": "defender",
            "brain": {
                "name": "palaestrai.agent.dummy_brain:DummyBrain",
                "params": {},
            },
            "muscle": {
                "name": "palaestrai.agent.dummy_muscle:DummyMuscle",
                "params": {},
            },
            "objective": {
                "name": "palaestrai.agent.dummy_objective:DummyObjective",
                "params": {"params": 1},
            },
            "sensors": [SensorInformation(0, MagicMock(), "TestSensor-1")],
            "actuators": [
                ActuatorInformation(0, MagicMock(), "TestActuator-1")
            ],
        }

        self.ac = AgentConductor(self.agent_params, 0, "Some AgentConductor")
        self.ac._objective = MagicMock()
        self.ac._experiment_info = MagicMock()
        self.setup_req = AgentSetupRequest(
            receiver_agent_conductor=self.ac.uid,
            sender_simulation_controller="0",
            experiment_run_id="1",
            experiment_run_instance_id="SomeInstance",
            experiment_run_phase=42,
            configuration=self.agent_params,
            rollout_worker_uid="worker-1",
            sensors=[
                SensorInformation(0, MagicMock(), "TestSensor-1"),
                SensorInformation(0, MagicMock(), "TestSensor-2"),
            ],
            actuators=[
                ActuatorInformation(0, MagicMock(), "TestActuator-1"),
                ActuatorInformation(0, MagicMock(), "TestActuator-2"),
            ],
            muscle_name="TestAgent",
        )
        self.setup_req_empty = AgentSetupRequest(
            receiver_agent_conductor=self.ac.uid,
            sender_simulation_controller="0",
            experiment_run_instance_id="SomeExperimentRunInstance",
            experiment_run_phase=47,
            configuration=self.agent_params,
            experiment_run_id="1",
            rollout_worker_uid="2",
            sensors=list(),
            actuators=list(),
            muscle_name="TestAgent",
        )
        self.shutdown_req = ShutdownRequest(
            sender="Somebody", receiver=self.ac.uid, experiment_run_id="1"
        )

    @patch("palaestrai.agent.agent_conductor.aiomultiprocess.Process")
    def test_init_brain(self, mockaio):
        type(self.ac._experiment_info).experiment_run_uid = MagicMock(
            return_value="TestExperiment"
        )
        type(self.ac._experiment_info).experiment_run_phase = PropertyMock(
            return_value=0
        )
        self.ac._init_brain(self.setup_req.sensors, self.setup_req.actuators)

        self.assertEqual(mockaio.call_count, 1)
        self.assertIsInstance(self.ac._learner, Learner)
        self.assertIsInstance(self.ac._learner._brain, DummyBrain)
        self.assertEqual(len(self.ac._learner._brain.sensors), 2)
        self.assertEqual(len(self.ac._learner._brain.actuators), 2)

    @patch("palaestrai.agent.agent_conductor.aiomultiprocess.Process")
    def test_init_muscle(self, mockaio):
        type(self.ac._experiment_info).experiment_run_uid = MagicMock(
            return_value="TestExperiment"
        )
        type(self.ac._experiment_info).experiment_run_phase = PropertyMock(
            return_value=0
        )
        self.ac._learner = MagicMock()
        self.ac._init_muscle(str(uuid4()))

        self.assertEqual(mockaio.call_count, 1)
        self.assertEqual(len(self.ac._rollout_workers), 1)
        self.assertEqual(len(self.ac._processes), 1)

    @patch("palaestrai.agent.agent_conductor.aiomultiprocess.Process")
    def test_handle_agent_setup(self, mockaio):
        self.ac._init_brain = MagicMock()
        self.ac._init_muscle = MagicMock()

        rsp = self.ac._handle_agent_setup(self.setup_req)
        self.ac._init_brain.assert_called_once()
        self.ac._init_muscle.assert_called()
        self.assertIsInstance(rsp, AgentSetupResponse)

    @patch("palaestrai.agent.agent_conductor.aiomultiprocess.Process")
    async def test_handle_shutdown(self, mockaio):
        self.ac._learner_process = AsyncMock()
        self.ac._processes.append(AsyncMock())
        await self.ac._handle_shutdown(self.shutdown_req)

        for task in self.ac._processes:
            self.assertEqual(task.join.call_count, 1)
        self.assertEqual(self.ac._learner_process.join.call_count, 1)

    @patch(f"{AgentConductor.__module__}.asyncio")
    async def test_housekeeping_setup(self, mock_asyncio):
        mock_transceive_task = AsyncMock()
        mock_transceive_task.result = MagicMock(
            return_value=AgentSetupRequest(
                sender_simulation_controller="sim-1",
                receiver_agent_conductor="ac-1",
                experiment_run_id="run-1",
                experiment_run_instance_id="run-1-instance",
                experiment_run_phase=47,
                rollout_worker_uid="ag-1",
                sensors=list(),
                actuators=list(),
                configuration=dict(),
                muscle_name="agent",
            )
        )

        mock_asyncio.wait = AsyncMock(
            return_value=([mock_transceive_task], list())
        )
        mock_asyncio.create_task = MagicMock(return_value=mock_transceive_task)
        self.ac._worker = MagicMock()

        request = await self.ac._housekeeping(None)

        self.assertIsInstance(request, AgentSetupRequest)
        mock_asyncio.create_task.assert_called_once()
        mock_asyncio.wait.assert_called_once()

    @patch(f"{AgentConductor.__module__}.asyncio")
    async def test_housekeeping_shutdown(self, mock_asyncio):
        mock_transceive_task = AsyncMock()
        mock_transceive_task.result = MagicMock(
            return_value=ShutdownRequest(
                sender="Somebody",
                receiver=self.ac.uid,
                experiment_run_id="run-1",
            )
        )
        mock_muscle_task = AsyncMock()
        mock_muscle_task.join = MagicMock()
        mock_muscle_task.exitcode.return_value = 0
        mock_muscle_task.is_alive = MagicMock(return_value=True)
        mock_brain_task = AsyncMock()
        mock_brain_task.join = MagicMock()
        mock_brain_task.exitcode.return_value = 0
        mock_brain_task.is_alive = MagicMock(return_value=True)

        self.ac._processes.append(mock_muscle_task)
        self.ac._learner_process = mock_brain_task

        mock_asyncio.wait = AsyncMock(
            return_value=([mock_transceive_task], list())
        )
        mock_asyncio.create_task = MagicMock(return_value=mock_transceive_task)
        self.ac._worker = MagicMock()

        request = await self.ac._housekeeping(None)

        self.assertIsInstance(request, ShutdownRequest)
        self.assertEqual(3, mock_asyncio.create_task.call_count)
        mock_asyncio.wait.assert_called_once()

    @patch(f"{AgentConductor.__module__}.asyncio")
    async def test_housekeeping_ungraceful_death(self, mock_asyncio):
        mock_transceive_task = AsyncMock()
        mock_transceive_task.result = MagicMock(
            return_value=ShutdownRequest(
                sender="The Dude",
                receiver=self.ac.uid,
                experiment_run_id="run-1",
            )
        )
        mock_muscle_task = AsyncMock()
        mock_muscle_task.join = MagicMock()
        mock_muscle_task.exitcode.return_value = 1
        mock_muscle_task.is_alive = MagicMock(return_value=False)
        mock_brain_task = AsyncMock()
        mock_brain_task.join = MagicMock()
        mock_brain_task.exitcode.return_value = 0
        mock_brain_task.is_alive = MagicMock(return_value=True)

        self.ac._processes.append(mock_muscle_task)
        self.ac._learner_process = mock_brain_task

        mock_asyncio.wait = AsyncMock(
            return_value=([mock_transceive_task], list())
        )
        mock_asyncio.create_task = MagicMock(return_value=mock_transceive_task)
        self.ac._worker = MagicMock()

        with self.assertRaises(RuntimeError):
            with self.assertLogs(
                "palaestrai.agent.agent_conductor", level="WARNING"
            ) as cm:
                await self.ac._housekeeping(None)

        # self.assertIsInstance(request, ShutdownRequest)
        self.assertEqual(3, mock_asyncio.create_task.call_count)
        mock_asyncio.wait.assert_called_once()
        self.assertIn("dead tasks", cm.output[0])

    @patch(f"{AgentConductor.__module__}.asyncio")
    async def test_housekeeping_signal_received(self, mock_asyncio):
        def raise_system_exit():
            raise SystemExit()

        mock_transceive_task = AsyncMock()
        mock_transceive_task.result = MagicMock(
            return_value=ShutdownRequest(
                sender="The Dude",
                receiver=self.ac.uid,
                experiment_run_id="run-1",
            )
        )
        mock_muscle_task = AsyncMock()
        mock_muscle_task.join = MagicMock()
        mock_muscle_task.exitcode.return_value = 0
        mock_muscle_task.is_alive = MagicMock(return_value=True)
        mock_brain_task = AsyncMock()
        mock_brain_task.join = MagicMock()
        mock_brain_task.exitcode.return_value = 0
        mock_brain_task.is_alive = MagicMock(return_value=True)

        self.ac._processes.append(mock_muscle_task)
        self.ac._learner_process = mock_brain_task

        mock_asyncio.wait = AsyncMock(
            side_effect=lambda x, return_when: raise_system_exit()
        )
        mock_asyncio.create_task = MagicMock(return_value=mock_transceive_task)
        self.ac._worker = MagicMock()

        with self.assertRaises(SystemExit):
            with self.assertLogs(
                "palaestrai.agent.agent_conductor", level="WARNING"
            ) as cm:
                await self.ac._housekeeping(None)

        self.assertEqual(3, mock_asyncio.create_task.call_count)
        mock_asyncio.wait.assert_called_once()
        self.assertIn("SIGINT/SIGTERM", cm.output[0])

    @patch("palaestrai.agent.agent_conductor.aiomultiprocess.Process")
    async def test_run(self, mockaio):
        self.ac._worker = AsyncMock()
        setup_msg = self.setup_req_empty
        shutdown_msg = self.shutdown_req
        self.ac._housekeeping = AsyncMock(
            side_effect=[setup_msg, shutdown_msg, shutdown_msg]
        )

        self.ac._handle_shutdown = AsyncMock()
        await self.ac.run()

        self.assertEqual(2, self.ac._housekeeping.call_count)

    def test_load_brain_dumpers(self):
        type(self.ac._experiment_info).experiment_run_uid = MagicMock(
            return_value="TestExperiment"
        )
        type(self.ac._experiment_info).experiment_run_phase = PropertyMock(
            return_value=0
        )

        dumpers = self.ac._load_brain_dumpers()

        self.assertEqual(2, len(dumpers))
        self.assertIsInstance(dumpers[0], FileBrainDumper)
        self.assertIsInstance(dumpers[1], StoreBrainDumper)

    def test_implicit_brain_load_not_in_phase_0(self):
        type(self.ac._experiment_info).experiment_run_uid = MagicMock(
            return_value="TestExperiment"
        )
        type(self.ac._experiment_info).experiment_run_phase = PropertyMock(
            return_value=0
        )
        dumpers = self.ac._load_brain_dumpers()
        self.assertTrue(len(dumpers) > 0)
        self.assertIsNone(dumpers[0]._brain_source)

    def test_implicit_brain_load(self):
        type(self.ac._experiment_info).experiment_run_uid = MagicMock(
            return_value="TestExperiment"
        )
        type(self.ac._experiment_info).experiment_run_phase = PropertyMock(
            return_value=1
        )
        dumpers = self.ac._load_brain_dumpers()
        self.assertTrue(len(dumpers) > 0)
        self.assertIsNotNone(dumpers[0]._brain_source)
        self.assertEqual(dumpers[0]._brain_source.experiment_run_phase, 0)

    def test_load_brain_malformed_config(self):
        type(self.ac._experiment_info).experiment_run_uid = MagicMock(
            return_value="TestExperiment"
        )
        type(self.ac._experiment_info).experiment_run_phase = PropertyMock(
            return_value=0
        )
        self.ac._config["load"] = ["agent", "12341234", 0]

        with catch_warnings(record=True) as cm:
            dumpers = self.ac._load_brain_dumpers()

            self.assertEqual(1, len(cm))
            self.assertTrue(issubclass(cm[-1].category, UserWarning))
            self.assertEqual(2, len(dumpers))


if __name__ == "__main__":
    unittest.main()

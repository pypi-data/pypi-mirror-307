import unittest
from unittest.mock import MagicMock, AsyncMock, call, patch
from uuid import uuid4

import time

from palaestrai.core import BasicState
from palaestrai.core.protocol import (
    EnvironmentSetupRequest,
    EnvironmentSetupResponse,
    ShutdownRequest,
    ShutdownResponse,
)
from palaestrai.environment.environment_conductor import EnvironmentConductor


class _MockEnv:
    async def run(self):
        time.sleep(0.1)
        exit(0)


class _MockDyingProcess:
    def __init__(self):
        self.uid = "The Dreaded Castle of Aaaaaaaaah"

    async def run(self):
        exit(23)


class TestEnvironmentConductor(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.addCleanup(patch.stopall)
        self.env_cond = EnvironmentConductor(
            {
                "environment": {
                    "name": (
                        "palaestrai.environment.dummy_environment:"
                        "DummyEnvironment"
                    ),
                    "uid": "0815",
                    "params": {"discrete": False},
                },
            },
            123,
            uuid4(),
        )

    async def test_one_process_per_environment(self):
        msg_setup = EnvironmentSetupRequest(
            experiment_run_id="run away",
            experiment_run_instance_id="run away instance",
            experiment_run_phase=47,
            receiver_environment_conductor_id="the boss",
            sender_simulation_controller_id="the servant",
        )

        self.assertIsNone(self.env_cond._environment_process)
        self.env_cond.handle_environment_setup_request(msg_setup)
        self.assertIsNotNone(self.env_cond._environment_process)
        prc = self.env_cond._environment_process
        self.env_cond.handle_environment_setup_request(msg_setup)
        self.assertEqual(prc, self.env_cond._environment_process)
        prc.terminate()
        await prc.join()

    @patch(
        "palaestrai.core.event_state_machine.MajorDomoWorker",
        return_value=unittest.mock.AsyncMock(
            transceive=unittest.mock.AsyncMock(
                side_effect=[
                    EnvironmentSetupRequest(
                        experiment_run_id="run away",
                        experiment_run_instance_id="run away instance",
                        experiment_run_phase=47,
                        receiver_environment_conductor_id="the boss",
                        sender_simulation_controller_id="the servant",
                    ),
                    ShutdownRequest(
                        sender="the boss",
                        receiver="the servant",
                        experiment_run_id="run away",
                    ),
                    None,
                ]
            )
        ),
    )
    async def test_run_shutdown(self, _):
        self.env_cond._environment = MagicMock(uid="0815")
        self.env_cond._load_environment = MagicMock()
        self.env_cond._init_environment = MagicMock()
        await self.env_cond.run()
        self.assertEqual(self.env_cond._state, BasicState.FINISHED)

    @patch(
        "palaestrai.core.event_state_machine.MajorDomoWorker",
        return_value=unittest.mock.AsyncMock(
            transceive=unittest.mock.AsyncMock(
                side_effect=[
                    EnvironmentSetupRequest(
                        experiment_run_id="run away",
                        experiment_run_instance_id="run away instance",
                        experiment_run_phase=47,
                        receiver_environment_conductor_id="the servant",
                        sender_simulation_controller_id="the boss",
                    ),
                    EnvironmentSetupRequest(
                        experiment_run_id="run away",
                        experiment_run_instance_id="run away instance",
                        experiment_run_phase=47,
                        receiver_environment_conductor_id="the servant",
                        sender_simulation_controller_id="the boss",
                    ),
                    ShutdownRequest(
                        sender="the boss",
                        receiver="the servant",
                        experiment_run_id="run away",
                    ),
                    None,
                ]
            )
        ),
    )
    async def test_setup_conductor(self, mock_worker):
        msg_setup_response = EnvironmentSetupResponse(
            sender_environment_conductor=self.env_cond.uid,
            receiver_simulation_controller="the boss",
            environment_id="0815",
            experiment_run_id="run away",
            experiment_run_instance_id="run away instance",
            experiment_run_phase=47,
            environment_type=self.env_cond._environment_configuration[
                "environment"
            ]["name"],
            environment_parameters=self.env_cond._environment_configuration[
                "environment"
            ]["params"],
        )
        msg_shutdown_response = ShutdownResponse(
            sender=self.env_cond.uid,
            receiver="the boss",
            experiment_run_id="run away",
        )

        calls = (
            call(None, skip_recv=False),
            call(msg_setup_response, skip_recv=False),
            call(msg_setup_response, skip_recv=False),
            call(msg_shutdown_response, skip_recv=True),
        )

        self.env_cond._environment = MagicMock(uid="0815")
        self.env_cond._load_environment = MagicMock()
        self.env_cond._init_environment = MagicMock()
        await self.env_cond.run()
        self.env_cond.__esm__._mdp_worker.transceive.assert_has_awaits(calls)

    @patch(
        "palaestrai.core.event_state_machine.MajorDomoWorker",
        return_value=unittest.mock.AsyncMock(
            transceive=unittest.mock.AsyncMock(
                side_effect=[
                    EnvironmentSetupRequest(
                        experiment_run_id="run away",
                        experiment_run_instance_id="run away instance",
                        experiment_run_phase=47,
                        receiver_environment_conductor_id="the boss",
                        sender_simulation_controller_id="the servant",
                    ),
                    ShutdownRequest(
                        sender="the boss",
                        receiver="the servant",
                        experiment_run_id="run away",
                    ),
                    None,
                ]
            )
        ),
    )
    async def test_dying_environment_process(self, _):
        self.env_cond._load_environment = MagicMock()
        self.env_cond._environment = _MockDyingProcess()
        await self.env_cond.run()
        self.assertIsNotNone(self.env_cond._environment_process)


if __name__ == "__main__":
    unittest.main()

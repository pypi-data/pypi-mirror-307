from __future__ import annotations
from typing import Union, Optional, TYPE_CHECKING

import sys
import signal
import logging
from uuid import uuid4

import aiomultiprocess
from numpy.random import RandomState

from palaestrai.util import seeding, spawn_wrapper
from palaestrai.core import EventStateMachine as ESM
from palaestrai.core import BasicState, RuntimeConfig
from palaestrai.core.protocol import (
    EnvironmentSetupRequest,
    EnvironmentSetupResponse,
    ShutdownRequest,
    ShutdownResponse,
)
from palaestrai.util.dynaloader import load_with_params
from palaestrai.util.exception import PrematureTaskDeathError

if TYPE_CHECKING:
    import multiprocessing
    from palaestrai.environment import Environment

LOG = logging.getLogger(__name__)


@ESM.monitor(is_mdp_worker=True)
class EnvironmentConductor:
    """The environment conductor creates new environment instances.

    There could be multiple simulation runs and each would need a
    separate environment. The environment conductor controls the
    creation of those new environment instances.

    Parameters
    ----------
    env_cfg : dict
        Dictionary with parameters needed by the environment
    seed : uuid4
        Random seed for recreation
    uid : uuid4
        Unique identifier

    """

    def __init__(self, env_cfg, seed: int, uid=None):
        self._uid: str = uid if uid else "EnvironmentConductor-%s" % uuid4()
        self.seed: int = seed
        self.rng: RandomState = seeding.np_random(self.seed)[0]
        self._environment_configuration = env_cfg
        self._state = BasicState.PRISTINE

        self._environment: Optional[Environment] = None
        self._environment_process: Optional[aiomultiprocess.Process] = None

        LOG.debug("%s created.", self)

    @property
    def uid(self) -> str:
        return str(self._uid)

    def _load_environment(self):
        """Loads the ::`Environment` and necessary dependent classes."""
        env_name = None
        env_params = {}
        try:
            env_name = self._environment_configuration["environment"]["name"]
            env_uid = self._environment_configuration["environment"].get(
                "uid", f"Environment-{uuid4()}"
            )
            env_params = self._environment_configuration["environment"][
                "params"
            ]
        except KeyError:
            LOG.critical(
                "%s could not load environment: Configuration not present. "
                'Key "environment" is missing in environment configuration. '
                "The configuration currently contains: %s",
                self,
                self._environment_configuration,
            )
            raise
        env_params.update(
            {
                "uid": env_uid,
                "broker_uri": f"tcp://127.0.0.1:{RuntimeConfig().executor_bus_port}",
                "seed": self.rng.randint(0, sys.maxsize),
            }
        )

        LOG.debug(
            "%s loading Environment '%s' with params '%s'.",
            self,
            env_name,
            env_params,
        )
        try:
            self._environment = load_with_params(env_name, env_params)
        except ValueError as e:
            LOG.critical(
                "%s could not load environment '%s': %s. Perhaps a typo in "
                "your configuration? %s",
                self,
                env_name,
                e,
                self._environment_configuration["environment"],
            )
            raise e

        if "state_transformer" in self._environment_configuration:
            self._environment._state_transformer = load_with_params(
                self._environment_configuration["state_transformer"]["name"],
                self._environment_configuration["state_transformer"]["params"],
            )
            LOG.debug(
                "%s loaded %s for %s",
                self,
                self._environment._state_transformer,
                self._environment,
            )
        if "reward" in self._environment_configuration:
            self._environment.reward = load_with_params(
                self._environment_configuration["reward"]["name"],
                self._environment_configuration["reward"]["params"],
            )
            LOG.debug(
                "%s loaded %s for %s",
                self,
                self._environment.reward,
                self._environment,
            )

    @ESM.spawns
    def _init_environment(self):
        """Initialize a new environment.

        Creates a new environment instance with its own UID.

        Returns
        -------
        str
            The unique identifier of the new environment
        """
        try:
            env_process = aiomultiprocess.Process(
                name=f"Environment-{self.uid}",
                target=spawn_wrapper,
                args=(
                    f"Environment-{self.uid}",
                    RuntimeConfig().to_dict(),
                    self._environment.run,
                ),
            )
            env_process.start()
        except Exception as e:
            LOG.critical(
                "%s encountered a fatal error while executing %s: %s. "
                "Judgement day is nigh!",
                self,
                self._environment,
                e,
            )
            raise e
        return env_process

    def setup(self):
        self._state = BasicState.RUNNING
        self.mdp_service = self.uid
        LOG.info("%s commencing run: creating better worlds.", self)

    @ESM.on(EnvironmentSetupRequest)
    def handle_environment_setup_request(self, request):
        LOG.debug(
            "%s received EnvironmentSetupRequest(experiment_run_id=%s).",
            self,
            request.experiment_run_id,
        )
        self._load_environment()
        LOG.info(
            "%s loaded %s, starting subprocess...",
            self,
            self._environment,
        )
        if self._environment_process is None:
            self._environment_process = self._init_environment()
        ssci = request.sender_simulation_controller_id
        return EnvironmentSetupResponse(
            sender_environment_conductor=self.uid,
            receiver_simulation_controller=ssci,
            environment_id=self._environment.uid,
            experiment_run_id=request.experiment_run_id,
            experiment_run_instance_id=request.experiment_run_instance_id,
            experiment_run_phase=request.experiment_run_phase,
            environment_type=self._environment_configuration["environment"][
                "name"
            ],
            environment_parameters=self._environment_configuration[
                "environment"
            ].get("params", dict()),
        )

    @ESM.on(ShutdownRequest)
    def handle_shutdown_request(self, request: ShutdownRequest):
        self._state = BasicState.STOPPING
        self.stop()  # type: ignore[attr-defined]
        return ShutdownResponse(
            sender=self.uid,
            receiver=request.sender,
            experiment_run_id=request.experiment_run_id,
            experiment_run_instance_id=request.experiment_run_instance_id,
            experiment_run_phase=request.experiment_run_phase,
        )

    @ESM.on(signal.SIGCHLD)
    def _handle_child(
        self, process: Union[aiomultiprocess.Process, multiprocessing.Process]
    ):
        if process.exitcode != 0:
            self._state = BasicState.ERROR
            LOG.critical(
                "Call Arthur Dent! "
                "The vogons demolished environment process %s "
                "(exited prematurely with rc %s)",
                process,
                process.exitcode,
            )

    def teardown(self):
        self._state = BasicState.FINISHED
        LOG.debug("%s completed shutdown.", self)

    def __str__(self):
        return f"{self.__class__.__name__}(id=0x{id(self):x}, uid={self.uid})"

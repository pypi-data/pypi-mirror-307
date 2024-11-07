"""This module contains the class :class:`AgentConductor` that
stores all information the agents need about an actuator.

"""

from __future__ import annotations
from typing import TYPE_CHECKING, Union, Optional, List, Dict

from collections import namedtuple

import signal
import logging
import asyncio
import warnings
import setproctitle
import aiomultiprocess
from uuid import uuid4
from copy import deepcopy

from palaestrai.core import MajorDomoWorker, RuntimeConfig
from palaestrai.core.protocol import (
    AgentSetupRequest,
    AgentSetupResponse,
    ShutdownRequest,
    ShutdownResponse,
)
from palaestrai.util import spawn_wrapper
from palaestrai.util.dynaloader import load_with_params, ErrorDuringImport
from palaestrai.util.exception import TasksNotFinishedError
from .brain import Brain
from palaestrai.types import ExperienceLocation
from .brain_dumper import BrainDumper, BrainLocation
from .muscle import Muscle
from .learner import Learner
from .rollout_worker import RolloutWorker

if TYPE_CHECKING:
    from palaestrai.agent import Objective

LOG = logging.getLogger(__name__)


ExperimentRunInfo = namedtuple(
    "ExperimentRunInfo",
    ["experiment_run_uid", "experiment_run_phase"],
    defaults=(None, None),
)


async def _run_rollout_brain(learner: Learner):
    """This method starts the rollout brain in a new process and with this the monitoring by the ESM.

    It takes care of proper
    installment of signal handlers, setting of the proctitle, and most
    importantly, error handling. This method should be wrapped in the
    :py:func:`palaestrai.util.spawn_wrapper` function, which, in turn, is the
    target of an :py:func:`aiomultiprocess.Process.run` call.

    Parameters
    ----------
    learner : Learner
        The :class:`Learner` instance that should be run.

    Returns
    -------
    Any
        Whatever the ::`~Learner.run` method returns.
    """
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGABRT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    setproctitle.setproctitle("palaestrAI[Brain-%s]" % learner.uid[-6:])
    try:
        # noinspection PyUnresolvedReferences
        return await learner.run()  # type: ignore[attr-defined]
    except Exception as e:
        LOG.critical(
            "%s died from a fatal wound to the head: %s",
            learner,
            e,
        )
        raise


async def _run_rollout_worker(worker: RolloutWorker):
    """This method starts the rollout muscles in new processes and with this the monitoring by the ESM.

    It takes care of proper installment of signal handlers,
    setting of the proctitle, and most importantly, error handling.
    This method should be wrapped in the
    :py:func:`palaestrai.util.spawn_wrapper` function, which, in turn, is the
    target of an :py:func:`aiomultiprocess.Process.run` call.

    Parameters
    ----------
    worker : RolloutWorker
        The :class:`~RolloutWorker` instance that runs

    Returns
    -------
    Any
        Whatever ::`~RolloutMuscle.run` returns
    """
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGABRT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    setproctitle.setproctitle("palaestrAI[Muscle-%s]" % worker.uid[-6:])
    try:
        # noinspection PyUnresolvedReferences
        return await worker.run()  # type: ignore[attr-defined]
    except Exception as e:
        LOG.critical(
            "%s suffers from dystrophy: %s",
            worker,
            worker.uid,
            e,
        )
        raise


class AgentConductor:
    """This creates a new agent conductor (AC).

    The AC receives an agent config, which contains all information for
    the brain and the muscle. Additional information, like the current
    run ID, are part of the AgentSetupRequest.

    Parameters
    ----------
    agent_config: dict
        A *dict* containing information, how to instantiate brain and
        muscle.
    seed: int
        The random seed for this agent conductor.
    uid : str
        The uid (a unique string) for this agent conductor object.
    """

    def __init__(
        self,
        agent_config: dict,
        seed: int,
        uid=None,
    ):
        self._seed = seed
        self._config = agent_config
        self._uid = str(uid) if uid else "AgentConductor-%s" % uuid4()

        self._objective: Optional[Objective] = None
        self._learner: Optional[Learner] = None
        self._rollout_workers: Dict[str, RolloutWorker] = {}

        self._worker = None
        self._learner_process = None
        self._experiment_info: Optional[ExperimentRunInfo] = None
        self._processes: List[aiomultiprocess.Process] = []

    def _handle_sigintterm(self, signum, frame):
        LOG.info(
            "AgentConductor(id=0x%x, uid=%s) "
            "interrupted by signal %s in frame %s",
            id(self),
            self.uid,
            signum,
            frame,
        )
        raise SystemExit()

    @property
    def uid(self):
        """Unique, opaque ID of the agent conductor object"""
        return self._uid

    @property
    def worker(self):
        """Getter for the :py:class:`MajorDomoWorker` object

        This method returns (possibly lazily creating) the current
        :py:class:`MajorDomoWorker` object. It creates this worker on demand.
        It is not safe to call this method between forks, as forks copy
        the context information for the worker which is process-depentent.

        :rtype: MajorDomoWorker
        """
        if self._worker is None:
            self._worker = MajorDomoWorker(
                f"tcp://127.0.0.1:{RuntimeConfig().executor_bus_port}",
                self.uid,
            )
        return self._worker

    def _load_objective(self) -> Objective:
        try:
            objective = load_with_params(
                self._config["objective"]["name"],
                self._config["objective"].get("params", {}),
            )
        except (ModuleNotFoundError, ErrorDuringImport, AttributeError) as e:
            LOG.exception("%s could not load objective: %s, aborting", self, e)
            raise
        return objective

    def _load_brain(self, actuators, sensors) -> Brain:
        params = self._config["brain"].get("params", {})
        try:
            brain: Brain = load_with_params(
                self._config["brain"]["name"], params
            )
        except TypeError:
            params.update(
                {
                    "seed": self._seed,
                    "sensors": sensors,
                    "actuators": actuators,
                }
            )
            try:
                brain = load_with_params(self._config["brain"]["name"], params)
                warnings.warn(
                    "Brain constructors with explicit 'muscle_connection', "
                    "'sensors', 'actuators', and 'seed' parameters are "
                    "deprecated in favor of simpler constructors. Please "
                    "just remove them, palaestrAI will take care of the rest.",
                    DeprecationWarning,
                )
            except Exception as e:  # Catch-all for any user code error
                LOG.exception("%s could not load Brain: %s, aborting", self, e)
                raise
        brain._seed = self._seed
        brain._sensors = sensors
        brain._actuators = actuators
        brain._dumpers = self._load_brain_dumpers()
        return brain

    def _init_brain(self, sensors, actuators):
        """Initialize the brain process.

        Each agent, which is represented by an individual conductor,
        has one brain process. This function initializes the brain
        process.

        The agent conductor allocates the port for the brain-muscle
        interconnection. For this, it binds to a random port given from the OS.
        It passes the port to the brain and closes the socket; the Brain will
        then re-open the socket as ZMQ socket. That works because sockets are
        refcounted and the ref count goes to 0 when the ::`Brain` closes the
        socket before re-opening it. The agent conductor then uses the port
        number (not the socket itself) to pass it to the ::`Muscle` objects,
        which then know where to find their ::`Brain`.

        Parameters
        ----------
        sensors : List[SensorInformation]
            List of available sensors.
        actuators : List[ActuatorInformation]
            List of available actuators.

        Returns
        -------
        str
            The listen URI of the brain.
        """

        brain: Brain = self._load_brain(actuators, sensors)
        self._learner: Learner = Learner(brain, f"{self.uid}.Brain")

        self._learner._experience_locations = [
            ExperienceLocation(
                agent_name=eloc.get("agent", self.uid),
                experiment_run_uid=eloc.get(
                    "experiment_run", self._experiment_info.experiment_run_uid
                ),
                experiment_run_phase=eloc.get(
                    "phase",
                    max(0, self._experiment_info.experiment_run_phase - 1),
                ),
            )
            for eloc in self._config.get("replay", [])
        ]

        try:
            self._learner_process = aiomultiprocess.Process(
                name=f"{self.uid}.Brain",
                target=spawn_wrapper,
                args=(
                    self.uid,
                    RuntimeConfig().to_dict(),
                    _run_rollout_brain,
                    [self._learner],
                ),
            )
            self._learner_process.start()

            LOG.debug("%s started %s", self, self._learner)
        except Exception as e:
            LOG.critical(
                "AgentConductor(id=0x%x, uid=%s) "
                "encountered a fatal error while executing "
                "Brain(id=%s): %s",
                id(self),
                self.uid,
                self._learner.uid,
                e,
            )
            raise

    def _init_muscle(self, uid: str):
        """Function to initialize a new muscle

        Each agent consists of one ::`~Brain` and at least one ::`~Muscle`.
        Muscles are the inference/rollout workers that act within an
        environment, gathering experiences. Each muscle has a unique name;
        usually, this is the name of the agent in the environment.

        Muscles relay their experiences to their ::`~Brain`, which learns
        from the experiences and updates the inference model of the muscle.
        Thus, an "agent" entitity actually consists of one learner (Brain),
        one or more inference workers (Muscles), and this
        ::`~AgentConductor` that ties it all together.

        This method is responsible for loading the ::`~Muscle` class and
        starting the respective sub-process.

        Parameters
        ----------
        uid : str
            Unique identifier of this :class:`RolloutWorker`
        """

        assert self._learner is not None
        assert self._objective is not None
        try:
            params = deepcopy(self._config["muscle"]["params"])
        except KeyError:
            params = {}

        muscle: Muscle = load_with_params(
            self._config["muscle"]["name"], params
        )
        muscle._uid = self._config["name"]
        muscle._model_loaders = self._load_brain_dumpers()

        rollout_worker = RolloutWorker(
            muscle=muscle,
            objective=self._objective,
            uid=uid,
            brain_uid=self._learner.uid,
        )
        self._rollout_workers[uid] = rollout_worker

        try:
            agent_process = aiomultiprocess.Process(
                name=uid,
                target=spawn_wrapper,
                args=(
                    uid,
                    RuntimeConfig().to_dict(),
                    _run_rollout_worker,
                    [rollout_worker],
                ),
            )
            agent_process.start()
            LOG.debug("%s started process for %s.", self, rollout_worker)
            self._processes.append(agent_process)
        except Exception as e:
            LOG.exception(
                "%s encountered a fatal error while executing %s: %s",
                self,
                rollout_worker,
                str(e),
                e,
            )
            raise

    async def run(self):
        """Monitors agents and facilitates information interchange

        This method is the main loop for the :py:class:`AgentConductor`. It
        monitors the :py:class:`Brain` object and :py:class:`Muscle` instances
        of the agent (i.e., the processes) and transceives/routes messages.

        """
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGABRT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        setproctitle.setproctitle(
            "palaestrAI[AgentConductor-%s]" % self._uid[-6:]
        )

        signal.signal(signal.SIGINT, self._handle_sigintterm)
        signal.signal(signal.SIGTERM, self._handle_sigintterm)
        LOG.info(
            "AgentConductor(id=0x%x, uid=%s) commencing run: "
            "Today's solutions to tomorrow's problems",
            id(self),
            self.uid,
        )
        proceed = True
        request = None
        reply = None
        while proceed:
            try:
                request = await self._housekeeping(reply)
            except TasksNotFinishedError:
                continue
            except SystemExit:
                break

            if isinstance(request, AgentSetupRequest):
                reply = self._handle_agent_setup(request)

            if isinstance(request, ShutdownRequest):
                await self._handle_shutdown(request)
                break

        LOG.debug(
            "AgentConductor(id=0x%x, uid=%s) sending "
            "ShutdownResponse(experiment_run_id=%s)",
            id(self),
            self.uid,
            request.experiment_run_id,
        )
        reply = ShutdownResponse(
            sender=self.uid,
            receiver=request.sender,
            experiment_run_id=self._experiment_info.experiment_run_uid,
            experiment_run_instance_id=request.experiment_run_instance_id,
            experiment_run_phase=self._experiment_info.experiment_run_phase,
        )
        try:
            await self.worker.transceive(reply, skip_recv=True)
        except SystemExit:
            pass  # If they really want to, we can skip that, too.
        LOG.info(
            "AgentConductor(id=0x%x, uid=%s) completed shutdown: "
            "ICH, AC, BIN NUN TOD, ADJÖ [sic].",
            id(self),
            self.uid,
        )

    async def _housekeeping(self, reply):
        """Keep the household clean and lively.

        In this method, replies are send and requests are received.
        Furthermore, the AC sees over his child tasks (muscles and
        brain).

        Parameters
        ----------
        reply:
            The next reply to send

        Returns
        -------
        request
            The request received during transceiving.

        """
        LOG.debug(
            "AgentConductor(id=0x%x, uid=%s) starts housekeeping. "
            "Everything needs to be in proper order.",
            id(self),
            self.uid,
        )
        try:
            transceive_task = asyncio.create_task(
                self.worker.transceive(reply)
            )
            muscle_tasks = [
                asyncio.create_task(p.join()) for p in self._processes
            ]
            brain_tasks = (
                [asyncio.create_task(self._learner_process.join())]
                if self._learner_process
                else []
            )
            tasks_done, tasks_pending = await asyncio.wait(
                [transceive_task] + muscle_tasks + brain_tasks,
                return_when=asyncio.FIRST_COMPLETED,
            )
            if not tasks_done:
                # This shouldn't happen, but you never know.
                raise TasksNotFinishedError()

            terminated_workers = [
                p
                for p in self._processes + [self._learner_process]
                if p is not None and not p.is_alive() and p.exitcode != 0
            ]
            if terminated_workers:
                # I don't think the other tasks should end like this?
                LOG.critical(
                    "AgentConductor(id=0x%x, uid=%s) "
                    "has suffered from prematurely dead tasks: %s",
                    id(self),
                    self.uid,
                    [p.name for p in terminated_workers],
                )
                signal.signal(signal.SIGINT, signal.SIG_DFL)
                signal.signal(signal.SIGABRT, signal.SIG_DFL)
                signal.signal(signal.SIGTERM, signal.SIG_DFL)
                raise RuntimeError(
                    "AgentConductor(id=0x%x, uid=%s) "
                    "has dead tasks at hands: %s"
                    % (
                        id(self),
                        self.uid,
                        [p.name for p in terminated_workers],
                    )
                )
            if transceive_task not in tasks_done:
                await transceive_task
            request = transceive_task.result()
        except SystemExit as e:
            LOG.warning(
                "AgentConductor(id=0x%x, uid=%s) "
                "stopping due to SIGINT/SIGTERM",
                id(self),
                self.uid,
            )
            raise e

        LOG.debug(
            "AgentConductor(id=0x%x, uid=%s) got a %s. "
            "Let's see how we handle this one.",
            id(self),
            self.uid,
            request,
        )

        return request

    def _handle_agent_setup(self, request: AgentSetupRequest):
        """Handle the agent setup request.

        One setup request will result in one new muscle created.
        The brain will be created if necessary.

        Parameters
        ----------
        request: :class:`.AgentSetupRequest`
            The agent setup request with information for the muscle to
            be created.

        Returns
        -------
        :class:`.AgentSetupResponse`
            The response for the simulation controller.

        """
        if request.receiver_agent_conductor != self.uid:
            return

        self._experiment_info = ExperimentRunInfo(
            experiment_run_uid=request.experiment_run_id,
            experiment_run_phase=request.experiment_run_phase,
        )

        self._objective = self._load_objective()
        if self._learner is None:
            self._init_brain(request.sensors, request.actuators)
        self._init_muscle(request.rollout_worker_uid)  # type: ignore[arg-type]

        return AgentSetupResponse(
            sender_agent_conductor=self.uid,
            receiver_simulation_controller=request.sender,
            experiment_run_id=request.experiment_run_id,
            experiment_run_instance_id=request.experiment_run_instance_id,
            experiment_run_phase=request.experiment_run_phase,
            agent_id=request.rollout_worker_uid,
        )

    def _load_brain_dumpers(self):
        """Loads all ::`~BrainDumper` descendants

        Through introspection, all classes that are descendants of
        ::`~BrainDumper` will be loaded. They have to be imported here in
        order for this to work.
        """
        lcfg = dict(
            agent=self.uid,
            experiment_run=self._experiment_info.experiment_run_uid,
            phase=max(0, self._experiment_info.experiment_run_phase - 1),
        )
        user_cfg = self._config.get("load", {})
        if not isinstance(user_cfg, dict):
            warnings.warn(
                f"{str(self)} received malformed `load` configuration:"
                f" {user_cfg}. Continuing with defaults.",
                UserWarning,
            )
            user_cfg = {}

        lcfg.update(user_cfg)

        # Prohibit loading the same agent from the same phase and the same
        # experiment run. Reason is that this will query Brains from previous
        # instances, effectively continuing the training. This voids our
        # reproducibility claim. So we reset the load config to an empty dict
        # if this is the case:
        if (
            lcfg["experiment_run"] == self._experiment_info.experiment_run_uid
            and lcfg["phase"] == self._experiment_info.experiment_run_phase
        ):
            lcfg = {}

        previous_location = (
            BrainLocation(
                agent_name=lcfg["agent"],
                experiment_run_uid=lcfg["experiment_run"],
                experiment_run_phase=lcfg["phase"],
            )
            if lcfg
            else None
        )
        current_location = BrainLocation(
            agent_name=self._config["name"],
            experiment_run_uid=self._experiment_info.experiment_run_uid,
            experiment_run_phase=self._experiment_info.experiment_run_phase,
        )

        dumpers = []
        for subclazz in BrainDumper.__subclasses__():
            try:
                obj = subclazz(
                    dump_to=current_location, load_from=previous_location
                )
                dumpers.append(obj)
            except TypeError as e:
                LOG.warning(
                    "%s could not register brain dumper %s: %s, skipping",
                    self,
                    subclazz,
                    e,
                )
        LOG.debug("%s loaded %d dumpers: %s", self, len(dumpers), dumpers)
        return dumpers

    async def _handle_shutdown(self, _):
        """Handle the shutdown request for this agent conductor.

        It is expected that all muscles and the brain of this
        agent conductor already received a shutdown request. Therefore,
        all this method does is to wait(join) for the processes.

        Parameters
        ----------
        request: :class:`.ShutdownRequest`
            The shutdown request
        """
        for task in self._processes:
            await task.join()
        await self._learner_process.join()

    def __str__(self):
        return (
            f"AgentConductor(id={id(self)}, uid={self.uid}, learner="
            f"{self._learner}, workers={self._rollout_workers})"
        )

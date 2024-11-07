from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Any,
    Sequence,
    Dict,
    Optional,
    List,
    Set,
    Union,
)
from abc import ABC


import uuid
import logging
import asyncio
from asyncio import Future
from collections import defaultdict
from itertools import product, chain

from palaestrai.agent import Agent
from palaestrai.core import BasicState
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
    ErrorIndicator,
    SimulationControllerTerminationRequest,
    SimulationControllerTerminationResponse,
    EnvironmentResetRequest,
    EnvironmentResetResponse,
    EnvironmentResetNotificationRequest,
    EnvironmentResetNotificationResponse,
    AgentShutdownRequest,
    AgentShutdownResponse,
    EnvironmentShutdownRequest,
    EnvironmentShutdownResponse,
    ShutdownRequest,
    ShutdownResponse,
    SimulationShutdownRequest,
    SimulationShutdownResponse,
)

# from palaestrai.util.exception import SimulationSetupError
from palaestrai.types import SimTime
from palaestrai.core import EventStateMachine as ESM
from palaestrai.util.dynaloader import load_with_params

if TYPE_CHECKING:
    from palaestrai.types import Mode
    from palaestrai.experiment import TerminationCondition
    from palaestrai.agent import (
        SensorInformation,
        ActuatorInformation,
        RewardInformation,
    )

LOG = logging.getLogger("palaestrai.simulation.SimulationController")


@ESM.monitor(is_mdp_worker=True)
class SimulationControllerBase(ABC):
    """Base class for all simulation execution strategies

    This ABC implements the common code for all simulation execution
    strategies.
    It provides the code for handling the setup phase of :class:`Environment`s
    and :class:`Agent`s.

    A concrete simulation controller needs to implement the
    :method:`~.simulate` method and register methods to handle the update
    responses from :class:`RolloutWorker` and :class:`Environment` classes.


    Parameters
    ----------
    agent_conductor_ids : Sequence[str]
        Unique IDs (service IDs) of all :class:`~AgentConductor`s
        this simulation controller talks to
    environment_conductor_ids : Sequence[str]
        Unique IDs (service IDs) of all :class:`~EnvironmentConductor`s
        this simulation controller talks to
    agents : Dict[str, Any]
        Configuration of all :class:`~Agent`s that participate in this
        simulation
    mode : palaestrai.types.Mode
        Mode of the simulation, e.g., training or testing
    termination_conditions : Dict[str, Any]
        Configuration of simulation :class:`~TerminationCondition`s.
        A termination condition indicates when a simulation should end, e.g.,
        when the environment terminates. The simulation controller instanciates
        all termination conditions.

    Attributes
    ----------
    uid : str
        Unique ID of this simulation controller (MDP service ID).
        Auto-generated upon instanciation.
    """

    def __init__(
        self,
        agent_conductor_ids: Sequence[str],
        environment_conductor_ids: Sequence[str],
        agents: Dict[str, Dict],
        mode: Mode,
        termination_conditions: Sequence[Dict[str, Any]],
        *args,
        **kwargs,
    ):  # *args, **kwargs for compatibility
        self.uid = f"{self.__class__.__name__}-{str(uuid.uuid4())[-6:]}"
        self._state = BasicState.PRISTINE

        # UIDs:
        self._run_governor_uid: str = str()
        self._agent_conductor_ids = set(agent_conductor_ids)
        self._environment_conductor_ids = set(environment_conductor_ids)
        self._termination_condition_configurations = termination_conditions

        # Identification of the experiment run:
        self._experiment_run_id: str = str()
        self._experiment_run_instance_id: str = str()
        self._experiment_run_phase: int = 0
        self._mode = mode

        # Configuration (list of agents, sensors available, etc.):
        self._agents: Dict[str, Agent] = {}
        self._agent_configurations: Dict[str, Dict] = agents
        self._agents_requested: List[AgentUpdateRequest] = []
        self._agents_ready: List[
            Union[
                AgentSetupResponse,
                AgentUpdateResponse,
                EnvironmentResetNotificationResponse,
            ]
        ] = []
        self._sensors_available: Dict[str, SensorInformation] = {}
        self._actuators_available: Dict[str, ActuatorInformation] = {}
        self._termination_conditions: List[TerminationCondition] = []
        self._environment_conductor_map: Dict[str, str] = {}
        self._active_environments: Set[str] = set()
        self._conductors_shut_down: List[ShutdownResponse] = []

        # Current state of the simulation
        self._simtimes: Dict[str, SimTime] = defaultdict(SimTime)
        self._environment_update_responses: List[EnvironmentUpdateResponse] = (
            []
        )

        # Futures for synchronization:
        self._future_init: Future
        self._future_agents_environments_end: Future
        self._future_conductors_end: Future
        self._future_agent_actions: Future
        self._future_environment_status: Future

    def setup(self):
        self._state = BasicState.PRISTINE
        self._load_termination_conditions()
        self._future_init = asyncio.get_running_loop().create_future()
        self.mdp_service = self.uid
        LOG.info("Simulation controller is ready: Follow the white rabbit.")

    def _load_termination_conditions(self):
        """Load (instanciate) all termination conditions

        Raises an exception if a termination condition could not be loaded,
        which needs to be handled by the caller.
        """
        try:
            self._termination_conditions = [
                load_with_params(cond["name"], cond["params"])
                for cond in self._termination_condition_configurations
            ]
        except Exception as e:
            LOG.exception("%s could not load termination condition", self)
            raise

    @ESM.on(SimulationStartRequest)
    async def _handle_simulation_start_request(
        self, request: SimulationStartRequest
    ) -> Union[SimulationStartResponse, ErrorIndicator]:
        LOG.info(
            "Starting simulation for "
            "experiment run %s, phase %s (#%d) in mode %s: "
            "Knock, knock -- the matrix has you.",
            request.experiment_run_id,
            request.experiment_run_phase_id,
            request.experiment_run_phase,
            self._mode,
        )
        self._state = BasicState.INITIALIZING
        self._run_governor_uid = request.sender_run_governor_id
        self._experiment_run_id = request.experiment_run_id
        self._experiment_run_instance_id = request.experiment_run_instance_id
        self._experiment_run_phase = request.experiment_run_phase

        _ = self._send_environment_setup_requests()

        try:
            await self._future_init
            self._state = BasicState.INITIALIZED
        except Exception:
            self._state = BasicState.ERROR

            # TODO: Send a exception response in future to handle shutdown
            async def _raise():
                raise self._future_init.exception()

            asyncio.get_running_loop().create_task(_raise())
            return ErrorIndicator(
                self.uid,
                request.sender,
                str(self._future_init.exception()),
                self._future_init.exception(),
            )
        await self._start_simulation_task()
        return SimulationStartResponse(
            sender_simulation_controller=self.uid,
            receiver_run_governor=request.sender_run_governor_id,
        )

    @ESM.requests
    def _send_environment_setup_requests(self):
        LOG.info(
            "Reqesting setup of environments: %s",
            self._environment_conductor_ids,
        )
        return [
            EnvironmentSetupRequest(
                receiver_environment_conductor_id=ec_id,
                sender_simulation_controller_id=self.uid,
                experiment_run_phase=self._experiment_run_phase,
                experiment_run_id=self._experiment_run_id,
                experiment_run_instance_id=self._experiment_run_instance_id,
            )
            for ec_id in self._environment_conductor_ids
        ]

    @ESM.on(EnvironmentSetupResponse)
    async def _handle_environment_setup_response(
        self, response: EnvironmentSetupResponse
    ):
        LOG.debug(
            "%s environment (#%s) started for "
            "experiment run %s, phase (#%s): "
            "Kcnok, kcnok -- the matrix returned.",
            self,
            response.environment_id,
            response.experiment_run_id,
            response.experiment_run_phase,
        )
        self._environment_conductor_map[response.environment_id] = (
            response.sender_environment_conductor
        )

        _ = self._try_start_environments()

    @ESM.requests
    def _try_start_environments(self):
        if self._environment_conductor_ids != set(
            self._environment_conductor_map.values()
        ):
            return []
        return [
            EnvironmentStartRequest(
                sender_simulation_controller=self.uid,
                receiver_environment=env_id,
                experiment_run_id=self._experiment_run_id,
                experiment_run_instance_id=self._experiment_run_instance_id,
                experiment_run_phase=self._experiment_run_phase,
            )
            for env_id in self._environment_conductor_map.keys()
        ]

    @ESM.on(EnvironmentStartResponse)
    async def _handle_environment_start_response(
        self, response: EnvironmentStartResponse
    ):
        self._sensors_available.update(
            {sensor.uid: sensor for sensor in response.sensors}
        )
        self._actuators_available.update(
            {actuator.uid: actuator for actuator in response.actuators}
        )
        self._simtimes[response.sender_environment] = response.simtime
        self._active_environments |= {response.sender_environment}
        _ = self._try_setup_agents()

    @ESM.requests
    def _try_setup_agents(self):
        if self._active_environments != set(
            self._environment_conductor_map.keys()
        ):
            return []

        unassigned = self._unassigned_sensors_actuators()
        if unassigned:
            LOG.critical(
                "%s"
                "found sensor/actuator assignments in the definition of "
                "ExperimentRun(id=%s), which could not be matched with the "
                "sensors/actuators actually provided by the environments: %s.",
                self,
                self.experiment_run_id,
                unassigned,
            )
            self._future_init.set_exception(
                # TODO: Debug why SimulationSetupError is not working
                RuntimeError(
                    # experiment_run_id=self._experiment_run_id,
                    # message=
                    "Sensor/actuator assignments not possible: %s"
                    % (unassigned)
                )
            )
            return []

        requests = []
        for acuid in self._agent_conductor_ids:
            conf = self._agent_configurations[acuid]
            agent_name = conf["name"] if "name" in conf else None
            rollout_worker_uid = f"{acuid}.Muscle-{str(uuid.uuid4())[-6:]}"

            agent = Agent(
                uid=agent_name,
                brain=None,
                brain_classname=conf["brain"]["name"],
                brain_params=conf["brain"]["params"],
                muscle_classname=conf["muscle"]["name"],
                muscle_params=conf["muscle"]["params"],
                muscles={rollout_worker_uid: None},
                sensors=[
                    self._sensors_available[sen_uid]
                    for sen_uid in self._sensors_available.keys()
                    if sen_uid in conf["sensors"]
                ],
                actuators=[
                    self._actuators_available[act_uid]
                    for act_uid in self._actuators_available.keys()
                    if act_uid in conf["actuators"]
                ],
            )
            LOG.info("Requesting setup of Agent %s.", agent_name)
            LOG.debug(
                "Agent '%s' has UID '%s'; sensors: %s; actuators: %s",
                agent_name,
                agent.uid,
                agent.sensors,
                agent.actuators,
            )
            self._agents[acuid] = agent
            requests += [
                AgentSetupRequest(
                    sender_simulation_controller=self.uid,
                    receiver_agent_conductor=acuid,
                    experiment_run_id=self._experiment_run_id,
                    experiment_run_instance_id=self._experiment_run_instance_id,
                    experiment_run_phase=self._experiment_run_phase,
                    rollout_worker_uid=rollout_worker_uid,
                    muscle_name=agent.uid,
                    sensors=agent.sensors,
                    actuators=agent.actuators,
                    configuration=conf,
                )
            ]
        return requests

    @ESM.on(AgentSetupResponse)
    def _handle_agent_setup_response(self, response: AgentSetupResponse):
        self._agents_ready.append(response)
        sum_rollout_workers_requested = sum(
            len(agent.muscles.keys()) for agent in self._agents.values()
        )
        LOG.info(
            "Rollout worker %s for agent %s is set up (worker %d/%d).",
            response.agent_id,
            response.sender_agent_conductor,
            len(self._agents_ready),
            sum_rollout_workers_requested,
        )
        if len(self._agents_ready) == sum_rollout_workers_requested:
            self._future_init.set_result(True)

    async def _start_simulation_task(self):
        self._future_agents_environments_end = (
            asyncio.get_running_loop().create_future()
        )
        self._future_conductors_end = (
            asyncio.get_running_loop().create_future()
        )
        self._state = BasicState.RUNNING
        self._simulation_task = asyncio.create_task(self._simulate())
        self._simulation_task.add_done_callback(self._handle_simulation_end)

    async def _simulate(self):
        self._state = BasicState.RUNNING
        current_sensor_readings = list(self._sensors_available.values())
        rewards_per_agent = defaultdict(list)

        LOG.info("Starting simulation.")
        while self._state == BasicState.RUNNING:
            # Iterate over agents in the order in which they were loaded,
            # which, in turn, is given by the order in which they are defined
            # in the experiment run file. Python's dict is guaranteed to
            # remember the order in which items were added to it (since 3.7).
            for i, agent in enumerate(self._agents.values()):
                # Let the current agent act:
                self._future_agent_actions = (
                    asyncio.get_running_loop().create_future()
                )
                self._agents_ready.clear()
                self._agents_requested = [
                    self._request_agent_actions(
                        agent,
                        TakingTurnsSimulationController._filter_sensors_for_agent(
                            current_sensor_readings, agent
                        ),
                        rewards_per_agent[agent.uid],
                        done=False,
                    )
                ]
                await self._future_agent_actions

                # Check for a termination signal from the agent,
                # then apply  the setpoints to the environments, and
                # advance state:
                response: AgentUpdateResponse = (
                    # The result is a list, but only a single items is in it
                    # right now. We need the list as such later when each agent
                    # gets one last update.
                    self._future_agent_actions.result()[0]
                )
                terminations = {
                    tc: tc.check_termination(response)
                    for tc in self._termination_conditions
                }
                if any(terminations.values()):
                    LOG.info(
                        "Action from rollout worker %s triggers "
                        "termination conditions(s) %s, "
                        "stopping this episode.",
                        response.sender,
                        [
                            tc
                            for tc, triggers in terminations.items()
                            if triggers
                        ],
                    )
                    self._state = BasicState.STOPPING
                    break  # Break from agent iteration loop
                self._future_environment_status = (
                    asyncio.get_running_loop().create_future()
                )
                self._environment_update_responses.clear()
                _ = self._request_environment_updates(response.actuators)
                await self._future_environment_status

                # Get environments states
                env_updates: List[EnvironmentUpdateResponse] = (
                    self._future_environment_status.result()
                )
                self._simtimes.update(
                    {
                        eu.sender_environment_id: eu.simtime
                        for eu in env_updates
                    }
                )
                current_sensor_readings = [
                    si
                    for si in chain.from_iterable(
                        eu.sensors for eu in env_updates
                    )
                ]

                # Rewards returned here are from the previous agent's actions:
                rewards_per_agent[
                    self._agents[
                        list(self._agents.keys())[(i - 1) % len(self._agents)]
                    ].uid
                ] = [
                    reward
                    for reward in chain.from_iterable(
                        eu.rewards for eu in env_updates
                    )
                ]

                # Does any of the environments lead to termination of the
                # current phase?
                if any(
                    tc.check_termination(msg)
                    for tc, msg in product(
                        self._termination_conditions, env_updates
                    )
                ):
                    LOG.info(
                        "Environment(s) '%s' end(s) the simulation.",
                        [
                            e.sender_environment_id
                            for e in env_updates
                            if e.done
                        ],
                    )
                    self._state = BasicState.STOPPING
                    break  # Break from agent iteration loop
        LOG.debug(
            "%s: the simulation has ended, updating agents one last time.",
            self,
        )
        self._future_agent_actions = asyncio.get_running_loop().create_future()
        self._agents_ready.clear()
        self._agents_requested = [
            self._request_agent_actions(
                agent=agent,
                sensor_readings=TakingTurnsSimulationController._filter_sensors_for_agent(
                    current_sensor_readings, agent
                ),
                rewards=rewards_per_agent[agent.uid],
                done=True,
            )
            for agent in self._agents.values()
        ]
        await self._future_agent_actions
        _ = self._request_termination(
            environment_done=any(
                tc.check_termination(msg)
                for tc, msg in product(
                    self._termination_conditions,
                    self._future_environment_status.result(),
                )
            ),
            last_reward=[
                reward
                for reward in chain.from_iterable(
                    eu.rewards
                    for eu in self._future_environment_status.result()
                )
            ],
        )

    def _handle_simulation_end(self, task: asyncio.Task):
        if task.exception() is not None:
            LOG.critical(
                "%s: Simulation exited with error: %s",
                self,
                task.exception(),
                exc_info=task.exception(),
            )

    def _unassigned_sensors_actuators(self):
        """Sanity check of sensors/actuators between agents and environments

        Sensors and actuators are returned from an ::`Environment` as part of
        the ::`EnvironmentSetupResponse`. The configuration of an experiment
        run contains a mapping of these sensors/actuators to agents. This
        method checks whether the mapping is correct. It catches typos or
        sensors specified that are not present in an environment.

        Returns
        -------

        Dict[str, Tuple[Set, Set]]
            For an agent, a Tuple containing the list of unmatched sensors,
            and the list of unmatched actuators. E.g.,
            ``{"my_agent": (["snesor_with_typo"], [])}``
        """
        result = dict()
        all_sensor_ids = set(self._sensors_available.keys())
        all_actuator_ids = set(self._actuators_available.keys())
        for acuid, conf in self._agent_configurations.items():
            agent_assigned_sensor_ids = set(conf["sensors"])
            agent_assigned_actuator_ids = set(conf["actuators"])
            missing_sensors = agent_assigned_sensor_ids - all_sensor_ids
            missing_actuators = agent_assigned_actuator_ids - all_actuator_ids
            if missing_sensors or missing_actuators:
                result[acuid] = (missing_sensors, missing_actuators)
        return result

    @staticmethod
    def _filter_sensors_for_agent(
        current_sensor_readings: List[SensorInformation], agent: Agent
    ) -> List[SensorInformation]:
        return [
            r
            for r in current_sensor_readings
            if r.uid in [s.uid for s in agent.sensors]
        ]

    @ESM.requests
    def _request_agent_actions(
        self,
        agent: Agent,
        sensor_readings: List[SensorInformation],
        rewards: List[RewardInformation],
        done: bool,
    ) -> List[AgentUpdateRequest]:
        return [
            AgentUpdateRequest(
                sender_simulation_controller_id=self.uid,
                receiver_rollout_worker_id=rollout_worker_uid,
                experiment_run_id=self._experiment_run_id,
                experiment_run_instance_id=self._experiment_run_instance_id,
                experiment_run_phase=self._experiment_run_phase,
                sensors=sensor_readings,
                actuators=agent.actuators,
                rewards=rewards,
                simtimes=self._simtimes,
                is_terminal=done,
                mode=self._mode,
            )
            for rollout_worker_uid in agent.muscles.keys()
        ]

    @ESM.on(AgentUpdateResponse)
    def _handle_agent_update(self, response: AgentUpdateResponse):
        self._agents_ready += [response]
        if len(self._agents_requested) == len(self._agents_ready):
            self._future_agent_actions.set_result(self._agents_ready)

    @ESM.requests
    def _request_environment_updates(
        self, setpoints: List[ActuatorInformation]
    ):
        LOG.debug(
            "%s posting setpoints "
            "and requesting new state from environments %s",
            self,
            self._active_environments,
        )
        return [
            EnvironmentUpdateRequest(
                sender_simulation_controller=self.uid,
                receiver_environment=env_uid,
                experiment_run_id=self._experiment_run_id,
                experiment_run_instance_id=self._experiment_run_instance_id,
                experiment_run_phase=self._experiment_run_phase,
                actuators=[
                    s for s in setpoints if s.uid.split(".")[0] == env_uid
                ],
            )
            for env_uid in self._active_environments
        ]

    @ESM.on(EnvironmentUpdateResponse)
    def _handle_environment_update(self, response: EnvironmentUpdateResponse):
        self._environment_update_responses += [response]
        LOG.debug("%s got update from environment %s.", self, response.sender)
        if len(self._environment_update_responses) == len(
            self._active_environments
        ):
            self._future_environment_status.set_result(
                self._environment_update_responses
            )

    @ESM.on(SimulationShutdownRequest)
    async def _handle_external_stop_request(
        self, request: SimulationShutdownRequest
    ):
        LOG.info("Shutting down the simulation due to external request")
        self._state = BasicState.STOPPING
        await self._future_agents_environments_end
        await self._future_conductors_end
        self.stop()  # type: ignore[attr-defined]
        return SimulationShutdownResponse(
            sender=self.uid,
            receiver=request.sender,
            experiment_run_id=self._experiment_run_id,
            experiment_run_instance_id=self._experiment_run_instance_id,
            experiment_run_phase=self._experiment_run_phase,
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(uid={self.uid}, agents="
            f"{self._agents}, environments={self._active_environments})"
        )

    @ESM.requests
    def _request_termination(self, environment_done: bool, last_reward):
        return SimulationControllerTerminationRequest(
            sender_simulation_controller_id=self.uid,
            receiver_run_governor_id=self._run_governor_uid,
            experiment_run_id=self._experiment_run_id,
            environment_terminated=environment_done,
            additional_results=None,
            last_reward=last_reward,
        )

    @ESM.on(SimulationControllerTerminationResponse)
    async def _handle_termination_response(
        self, response: SimulationControllerTerminationResponse
    ):
        if response.restart:
            # Do not shut down, everything stays intact, but gets reset:
            LOG.info("Restarting simulation...")
            await self._restart()
            return
        if response.complete_shutdown:
            LOG.info("Performing full shutdown...")
            await self._shutdown(include_conductors=True)
            return
        # We don't restart, but its not a complete shutdown either:
        # instruct the conductors to stop environments and agents, but
        # the conductors themselves should stay alive for a warm reset.
        LOG.info("Performing partial shutdown...")
        await self._shutdown(include_conductors=False)

    async def _shutdown(self, include_conductors: bool):
        for agent in self._agents.values():
            _ = self._request_agent_shutdown(agent)
        for env in self._active_environments:
            _ = self._request_environment_shutdown(env)
        await self._future_agents_environments_end
        self._state = self._future_agents_environments_end.result()
        if include_conductors:
            for uid in (
                self._agent_conductor_ids | self._environment_conductor_ids
            ):
                LOG.debug("%s requesting shutdown of conductor %s", self, uid)
                _ = self._request_conductor_shutdown(uid)
            await self._future_conductors_end
        self._state = BasicState.FINISHED

    async def _restart(self):
        self._sensors_available.clear()
        self._actuators_available.clear()
        self._active_environments.clear()
        self._future_init = asyncio.get_running_loop().create_future()
        for env_uid in self._environment_conductor_map.keys():
            LOG.debug(
                "%s: Requesting reset of environment '%s'", self, env_uid
            )
            _ = self._request_environment_reset(env_uid)
        await self._future_init

        self._agents_ready.clear()
        self._future_init = asyncio.get_running_loop().create_future()
        for agent in self._agents.values():
            LOG.debug("%s: Requesting reset of agent '%s'", self, agent.uid)
            _ = self._request_agent_reset(agent)
        await self._future_init

        # We can continue, now
        await self._start_simulation_task()

    @ESM.requests
    def _request_environment_reset(self, env_uid):
        return EnvironmentResetRequest(
            sender_simulation_controller_id=self.uid,
            receiver_environment_id=env_uid,
        )

    @ESM.on(EnvironmentResetResponse)
    def _handle_environment_reset_response(
        self, response: EnvironmentResetResponse
    ):
        if response.create_new_instance:
            LOG.error(
                "Environment '%s' requests that we create a new "
                "instance, but this feature is not yet implemented.",
                response.sender_environment_id,
            )
            return
        self._active_environments |= {response.sender_environment_id}
        self._sensors_available.update(
            {sensor.uid: sensor for sensor in response.sensors}
        )
        self._actuators_available.update(
            {actuator.uid: actuator for actuator in response.actuators}
        )
        if len(self._active_environments) == len(
            self._environment_conductor_map
        ):
            self._future_init.set_result(self._active_environments)

    @ESM.requests
    def _request_agent_reset(self, agent: Agent):
        return EnvironmentResetNotificationRequest(
            sender_simulation_controller_id=self.uid,
            receiver_agent_id=agent.uid,
        )

    @ESM.on(EnvironmentResetNotificationResponse)
    def _handle_environment_reset_notification_response(
        self, response: EnvironmentResetNotificationResponse
    ):
        self._agents_ready += [response]
        if len(self._agents_ready) == len(self._agents):
            self._future_init.set_result(self._agents_ready)

    @ESM.requests
    def _request_agent_shutdown(self, agent: Agent):
        return [
            AgentShutdownRequest(
                sender=self.uid,
                receiver=rollout_worker_uid,
                experiment_run_id=self._experiment_run_id,
                experiment_run_phase=self._experiment_run_phase,
                experiment_run_instance_id=self._experiment_run_instance_id,
            )
            for rollout_worker_uid in agent.muscles.keys()
        ]

    @ESM.on(AgentShutdownResponse)
    def _handle_agent_shutdown_response(self, response: AgentShutdownResponse):
        acuid, agent = next(
            (k, v)
            for k, v in self._agents.items()
            if response.sender in v.muscles
        )
        del self._agents[acuid]
        if len(self._agents) == 0 and len(self._active_environments) == 0:
            self._future_agents_environments_end.set_result(
                BasicState.STOPPING
            )

    @ESM.requests
    def _request_environment_shutdown(self, environment_uid: str):
        return EnvironmentShutdownRequest(
            sender=self.uid,
            receiver=environment_uid,
            experiment_run_id=self._experiment_run_id,
            experiment_run_instance_id=self._experiment_run_instance_id,
            experiment_run_phase=self._experiment_run_phase,
        )

    @ESM.on(EnvironmentShutdownResponse)
    def _handle_environment_shutdown_response(
        self, response: EnvironmentShutdownResponse
    ):
        self._active_environments -= {response.environment_id}
        if len(self._agents) == 0 and len(self._active_environments) == 0:
            self._future_agents_environments_end.set_result(
                BasicState.STOPPING
            )

    @ESM.requests
    def _request_conductor_shutdown(self, conductor_uid: str):
        return ShutdownRequest(
            sender=self.uid,
            receiver=conductor_uid,
            experiment_run_id=self._experiment_run_id,
            experiment_run_instance_id=self._experiment_run_instance_id,
            experiment_run_phase=self._experiment_run_phase,
        )

    @ESM.on(ShutdownResponse)
    def _handle_shutdown_response(self, response: ShutdownResponse):
        self._conductors_shut_down += [response]
        if len(self._conductors_shut_down) == len(
            self._agent_conductor_ids
        ) + len(self._environment_conductor_ids):
            self._future_conductors_end.set_result(BasicState.FINISHED)

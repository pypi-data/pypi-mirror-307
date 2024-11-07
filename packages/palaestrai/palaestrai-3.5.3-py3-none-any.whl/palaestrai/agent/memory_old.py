from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Set, Union, Iterable

import numpy as np
import pandas
import pandas as pd

from .actuator_information import ActuatorInformation
from .reward_information import RewardInformation
from .sensor_information import SensorInformation

LOG = logging.getLogger(__name__)


@dataclass
class MuscleMemory:
    """Collected data from one muscle

    Attributes
    ----------

    sensor_readings : pd.DataFrame
        Column-wise (original) sensor readings as they are provided by the
        environments. Each sensor name is a column; the
        :class:`SensorInformation` objects are stored as-is.
    actuator_setpoints : pd.DataFrame
        Column-wise (original) actuator setpoints. Each actuator name is a
        column; this data frame stores the :class:`ActuatorInformation`
        objects as-is.
    rewards : pd.DataFrame
        Column-wise environment rewards; stores the :class:`RewardInformation`
        objects as-is, with each reward having its own column
    observations : Optional[np.ndarray]
        Transformed observations: Any data :class:`Muscle` and :class:`Brain`
        want to store
    actions : Optional[np.ndarray]
        Transformed observations: Any data :class:`Muscle` and :class:`Brain`
        want to store
    objective : Optional[np.ndarray]
        Result of calling the agent's objective function
    dones : np.ndarray
        Whether the simulation was done at the respective time index or not.
    additional_data : pd.DataFrame
        Any additional data a :class:`Muscle` shares with is :class:`Brain`
    """

    _sensor_readings: pd.DataFrame
    _actuator_setpoints: pd.DataFrame
    _rewards: pd.DataFrame
    dones: np.ndarray
    observations: Optional[np.ndarray] = None
    actions: Optional[np.ndarray] = None
    objective: Optional[np.ndarray] = None
    _additional_data: pd.DataFrame = field(default_factory=pd.DataFrame)

    @property
    def sensor_readings(self):
        return self._sensor_readings.drop("_gidx", axis=1, errors="ignore")

    @property
    def actuator_setpoints(self):
        return self._actuator_setpoints.drop("_gidx", axis=1, errors="ignore")

    @property
    def rewards(self):
        return self._rewards.drop("_gidx", axis=1, errors="ignore")

    @property
    def additional_data(self):
        return self._additional_data.drop("_gidx", axis=1, errors="ignore")

    @property
    def _valid_rewards(self):
        """Returns those reward entries that are neither null, NaN or []."""
        return self._rewards[
            (
                ~self._rewards.isnull().any(axis=1)
                & ~self._rewards.isin([[]]).any(axis=1)
            )
        ]

    @property
    def valid_rewards(self):
        """Returns those reward entries that are neither null, NaN or []."""
        return self._valid_rewards.drop("_gidx", axis=1, errors="ignore")

    def __len__(self):
        """Number of usable entries in this particular muscle memory

        "Usable" entries are entries that have at least sensor inputs,
        actuator setpoints, and related rewards.
        """
        return min(
            len(self.sensor_readings),
            len(self.actuator_setpoints),
            len(self.valid_rewards),
        )

    def tail(self, n=1):
        """Returns the last *n* entries in this memory

        This method returns a subset of this MuscleMemory's data, containing
        the last *n* full entries. "Full" entries are those for which
        sensor readings, actuator setpoints, and rewards exist.
        """
        length = len(self._valid_rewards)
        start = max(0, length - n + 1)
        indexes = self._valid_rewards.indexes[start:length]
        return MuscleMemory(
            _sensor_readings=self._sensor_readings[indexes],
            _actuator_setpoints=self._actuator_setpoints[indexes],
            _rewards=self._rewards[indexes],
            dones=self.dones[indexes],
            observations=(
                self.observations[indexes] if self.observations else None
            ),
            actions=(self.actions[indexes] if self.actions else None),
            objective=(self.objective[indexes] if self.objective else None),
            _additional_data=(
                self._additional_data[indexes]
                if not self._additional_data.empty
                else None
            ),
        )

    @staticmethod
    def concat(memories: Iterable[MuscleMemory]):
        """Concatenate a number of ::`MuscleMemory`s

        All attributes are concatenated in order.
        """

        # Make sure to keep semantics with the NumPy arrays:

        all_observations = [
            m.observations for m in memories if m.observations is not None
        ]
        all_actions = [m.actions for m in memories if m.actions is not None]
        all_objectives = [
            m.objective for m in memories if m.objective is not None
        ]

        return MuscleMemory(
            _sensor_readings=pd.concat(
                [m._sensor_readings for m in memories], ignore_index=True
            ),
            _actuator_setpoints=pd.concat(
                [m._actuator_setpoints for m in memories], ignore_index=True
            ),
            _rewards=pd.concat(
                [m._rewards for m in memories], ignore_index=True
            ),
            dones=np.concatenate([m.dones for m in memories]),
            observations=(
                np.concatenate(all_observations) if all_observations else None
            ),
            actions=np.concatenate(all_actions) if all_actions else None,
            objective=(
                np.concatenate(all_objectives) if all_objectives else None
            ),
            _additional_data=pd.concat(
                [
                    m._additional_data
                    for m in memories
                    if m._additional_data is not None
                ]
                + [pd.DataFrame()],
                ignore_index=True,
            ),
        )


class Memory:
    """An in-memory data structure to store experinences in a ::`~Brain`.

    Each agent needs a memory to store experiences, regardless of the training
    algorithm that is used. This class represents this memory. It is an
    in-memory data strcture that uses pandas DataFrames for its public API.
    The memory stores observations, actions, rewards given from the
    envrionment, and the internal reward of the agent (objective value). The
    memory is passed to an :class:`~Objective` to calculate the objective value
    from rewards.

    Parameters
    ----------

    size_limit : int = 1e6
        Maximum size the memory is allowed to grow to until old entries are
        overwritten by new ones.
    """

    def __init__(self, size_limit: int = int(1e6)):
        self.size_limit = size_limit
        self._data: Dict[str, MuscleMemory] = {}
        self._index = pd.DataFrame(columns=["_gidx", "tag"])

    @property
    def tags(self) -> Set[str]:
        """All tags known to this memory"""
        return set(self._data.keys())

    def data_for(self, muscle: str) -> MuscleMemory:
        """Returns the specific memory (data) for one particular tag"""
        return self._data[muscle]

    def __getitem__(self, tags):
        """Retrieves the (concatenated) :class:`MuscleMemory` for all tags."""
        return MuscleMemory.concat([self.data_for(tag) for tag in tags])

    @property
    def sensor_readings(self) -> pd.DataFrame:
        """All known sensor readings accross all tags"""
        return self[self.tags].sensor_readings

    @property
    def actuator_setpoints(self) -> pd.DataFrame:
        """All known actuator setpoints accross all tags"""
        return self[self.tags].actuator_setpoints

    @property
    def rewards(self) -> pd.DataFrame:
        """All known rewards accross all tags"""
        return self[self.tags].rewards

    @property
    def dones(self) -> np.ndarray:
        """All known end-of-episode flags accross all tags"""
        return self[self.tags].dones

    @property
    def observations(self) -> np.ndarray:
        """All known observations accross all tags"""
        return self[self.tags].observations

    @property
    def actions(self) -> np.ndarray:
        """All known actions accross all tags"""
        return self[self.tags].observations

    @property
    def objective(self) -> np.ndarray:
        """All known objective values accross all tags"""
        return self[self.tags].objective

    @property
    def additional_data(self) -> Optional[pandas.DataFrame]:
        """All known addtional data accross all tags"""
        return self[self.tags].additional_data

    @staticmethod
    def _info_to_df(
        df: pd.DataFrame,
        data: Union[
            List[SensorInformation],
            List[ActuatorInformation],
            List[RewardInformation],
        ],
        gidx: int,
    ) -> pd.DataFrame:
        if not data:
            return df
        data_dict = {d.uid: [d.value] for d in data}
        data_dict["_gidx"] = [gidx]
        return pd.concat(
            [
                df,
                pd.DataFrame.from_dict(data_dict),
            ],
            ignore_index=True,
        )

    def append(
        self,
        muscle_uid: str,
        sensor_readings: Optional[List[SensorInformation]] = None,
        actuator_setpoints: Optional[List[ActuatorInformation]] = None,
        rewards: Optional[List[RewardInformation]] = None,
        done: bool = False,
        observations: Optional[np.ndarray] = None,
        actions: Optional[np.ndarray] = None,
        objective: Optional[np.ndarray] = None,
        additional_data: Optional[Dict] = None,
    ):
        """Stores a new item in the agent's memory (append)

        An agent has experiences throughout its existence. The memory stores
        those by appending them.
        The memory stores at least those pieces of information that come from
        an environment, which are:

        * sensor readings
        * actuator setpoints (as issued by the agent)
        * rewards
        * whether the simulation has terminated (is "done")

        Readings, setpoints, and rewards are stored in their palaestrAI-native
        objects: :class:`SensorInformation`, :class:`ActuatorInformation`, and
        :class:`RewardInformation`.
        Additionally, an agent (i.e., its muscle) may store its own view in
        terms of transformed values.

        Parameters
        ----------

        muscle_uid : str
            UID of the agent (:class:`Muscle`) whose experiences we store
        sensor_readings : List[SensorInformation]
            A muscle's sensor readings as provided by the environment
        actuator_setpoints : List[ActuatorInformation]
            A muscle's setpoints as provided to an environment
        rewards : List[RewardInformation]
            Rewards issued by the environment. It is not necessary that
            sensor readings, setpoints, and rewards belong to the same
            time step; usually, rewards at a time step ``t`` belong to the
            sensor readings and actions from ``t-1``. This memory class
            correctly correlates rewards to the previous readings/actions.
        done : bool = False
            Whether this was the last action executed in the environment
        observations : Optional[np.ndarray] = None
            Observations the :class:`Muscle` wants to share with its
            :class:`Brain`, e.g., transformed/scaled values
        actions: Optional[np.ndarray] = None,
            Action-related data a :class:`Muscle` emitted, such as
            probabilities, or other data. Can be fed directly to the
            corresponding :class:`Brain`, as with ``observations``
        objective: Optional[np.ndarray] = None
            The agent's objective value describing its own goal. Optional,
            because the agent might not calculate such a value separately.
        additional_data : Optional[Dict] = None
            Any additional data a :class:`Muscle` wants to store
        """

        if sensor_readings is None:
            sensor_readings = []
        if actuator_setpoints is None:
            actuator_setpoints = []
        if rewards is None:
            rewards = []

        try:
            gidx = int(self._index.iloc[-1]["_gidx"]) + 1
        except IndexError:
            gidx = 0
        self._index = pd.concat(
            [self._index, pd.DataFrame({"_gidx": [gidx], "tag": [muscle_uid]})]
        )

        memory_item = MuscleMemory(
            _sensor_readings=Memory._info_to_df(
                pd.DataFrame(), sensor_readings, gidx
            ),
            _actuator_setpoints=Memory._info_to_df(
                pd.DataFrame(), actuator_setpoints, gidx
            ),
            _rewards=Memory._info_to_df(pd.DataFrame(), rewards, gidx),
            dones=np.array([done]),
            observations=(
                np.array([observations]) if observations is not None else None
            ),
            actions=np.array([actions]) if actions is not None else None,
            objective=np.array([objective]) if objective is not None else None,
            _additional_data=(
                pd.DataFrame({k: [v] for k, v in additional_data})
                if additional_data
                else None
            ),
        )
        if muscle_uid in self._data:
            self._data[muscle_uid] = MuscleMemory.concat(
                [self._data[muscle_uid], memory_item]
            )
        else:
            self._data[muscle_uid] = memory_item

        if len(self) > self.size_limit:
            self.truncate(self.size_limit)

    def tail(self, n=1):
        """Returns the n last full entries

        This method returns a nested data frame that returns the n last entries
        from the memory. This method constructs a multi-indexed data frame,
        i.e., a dataframe that contains other dataframes. You access each
        value through the hierarchy, e.g.,

            df = memory.tail(10)
            df.observations.uid.iloc[-1]

        Parameters
        ----------

        n : int = 1
            How many data items to return, counted from the latest addition.
            Defaults to 1.

        Returns
        -------

        pd.DataFrame :
            A nested (i.e., multi-indexed) data frame. The data frame contains
            *all* entries where the
            (observations, actions, rewards, objective)
            quadruplet is fully set. I.e., you can be sure that the all
            indexes correspond to each other, and that calling ``iloc``
            with an index really gives you the n-th observation, action, and
            reward for it.
            However, if for whatever reason the environment returned an
            empty reward, this will also be included. This is in contrast to
            the ::`~.sample` method, which will return only entries with where
            an associated reward is also present.
        """
        full_memory = self[self.tags]
        rewards = full_memory._valid_rewards.merge(
            self._index,
            on="_gidx",
            left_index=False,
            right_index=False,
        ).sort_values(by=["_gidx"])
        length = len(rewards)
        start = max(0, length - n)
        gidxes = rewards.iloc[start:length]._gidx
        indexes = list(gidxes.index)
        return MuscleMemory(
            _sensor_readings=full_memory._sensor_readings.iloc[indexes],
            _actuator_setpoints=full_memory._actuator_setpoints.iloc[indexes],
            _rewards=full_memory._rewards.iloc[indexes],
            dones=full_memory.dones[indexes],
            observations=(
                full_memory.observations[indexes]
                if full_memory.observations is not None
                and len(full_memory.observations) >= len(indexes)
                else None
            ),
            actions=(
                full_memory.actions[indexes]
                if full_memory.actions is not None
                and len(full_memory.actions) >= len(indexes)
                else None
            ),
            objective=(
                full_memory.objective[indexes]
                if full_memory.objective is not None
                and len(full_memory.objective) >= len(indexes)
                else None
            ),
            _additional_data=(
                full_memory._additional_data[indexes]
                if not full_memory._additional_data.empty
                and len(full_memory._additional_data) >= len(indexes)
                else None
            ),
        )

    def sample(self, num: int):
        """Returns a number of random samples from the memory.

        This method constructs a multi-indexed data frame, i.e., a dataframe
        that contains other dataframes. You access each value through the
        hierarchy, e.g.,

            df = memory.sample(10)
            df.observations.uid[19]

        Please bear in mind that the index is constructed from random sampling
        and is not contiguous, zero-based. If you really want the n-th item,
        use ``iloc`` instead. E.g.,

            df.observations.some_sensor.iloc[0]

        Parameters
        ----------
        num : int
            How many random samples should be drawn from the memory

        Returns
        -------
        pandas.DataFrame
            A multi-index pandas DataFrame with the main keys
            ``observations``, ``actions``, ``rewards``, and
            ``internal_rewards``.
        """

        # Make sure we return only valid entries: If no reward is given, then
        # we should not return that respective entries, as it does not make
        # sense to act without reward information.

        num = abs(num)
        full_memory = self[self.tags]
        indexes = full_memory.valid_rewards.sample(
            n=num, axis=0, replace=(num > len(full_memory))
        ).index
        return MuscleMemory(
            _sensor_readings=full_memory._sensor_readings.iloc[indexes],
            _actuator_setpoints=full_memory._actuator_setpoints.iloc[indexes],
            _rewards=full_memory._rewards.iloc[indexes],
            dones=full_memory.dones[indexes],
            observations=(
                full_memory.observations[indexes]
                if full_memory.observations is not None
                and len(full_memory.observations) > 0
                else None
            ),
            actions=(
                full_memory.actions[indexes]
                if full_memory.actions is not None
                and len(full_memory.actions) > 0
                else None
            ),
            objective=(
                full_memory.objective[indexes]
                if full_memory.objective is not None
                and len(full_memory.objective) > 0
                else None
            ),
            _additional_data=(
                full_memory._additional_data.iloc[indexes]
                if not full_memory._additional_data.empty
                and len(full_memory._additional_data) >= len(indexes)
                else None
            ),
        )

    def truncate(self, n: int):
        """Truncates the memory: Only the last *n* entries are retained.

        Parameters
        ----------
        n : int
            How many of the most recent entries should be retained. Negative
            values of n are treated as ``abs(n)``.
        """
        n = abs(n)
        if len(self._index) <= n:
            return
        idx_to_delete = self._index.iloc[0 : len(self._index) - n]
        # self._index = self._index.iloc[len(self._index)-n:]
        for mem in self._data.values():
            locidx_to_delete = mem._rewards[
                mem._rewards["_gidx"].isin(idx_to_delete["_gidx"])
            ]  # The deletables specifically in this memory
            if len(locidx_to_delete) == 0:
                continue  # Avoid unnecessary copy operations
            idx_to_keep = np.asarray(
                [~mem._rewards["_gidx"].isin(locidx_to_delete["_gidx"])]
            ).nonzero()[1]
            mem._sensor_readings = mem._sensor_readings.iloc[idx_to_keep]
            mem._actuator_setpoints = mem._actuator_setpoints.iloc[idx_to_keep]
            mem._rewards = mem._rewards.iloc[idx_to_keep]
            mem.dones = mem.dones[idx_to_keep]
            if mem._additional_data is not None and len(
                mem._additional_data
            ) >= len(idx_to_keep):
                mem._additional_data = mem._additional_data.iloc[idx_to_keep]
            if mem.observations is not None and len(mem.observations) >= len(
                idx_to_keep
            ):
                mem.observations = mem.observations[idx_to_keep]
            if mem.actions is not None and len(mem.actions) >= len(
                idx_to_keep
            ):
                mem.actions = mem.actions[idx_to_keep]
            if mem.objective is not None and len(mem.objective) >= len(
                idx_to_keep
            ):
                mem.objective = mem.objective[idx_to_keep]

    def __len__(self) -> int:
        """Returns the number of fully usable entries in the memory.

        "Fully usable entries" are those returned by, e.g., ::`~sample()`.
        I.e., the quadruplet of (observation, action, reward, objective).
        """
        return sum(len(m) for m in self._data.values())

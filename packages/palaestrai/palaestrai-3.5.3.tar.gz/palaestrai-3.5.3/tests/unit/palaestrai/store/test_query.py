from __future__ import annotations

from pathlib import Path
from typing import List
from unittest import TestCase
from tempfile import TemporaryDirectory

import pandas as pd
from pandas import Timestamp

from palaestrai.store import Session
import palaestrai.store.query as palq
from palaestrai.core import RuntimeConfig


class QueryTest(TestCase):
    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        RuntimeConfig().reset()
        RuntimeConfig().load(
            {"store_uri": f"sqlite:///{self._tmpdir.name}/palaestrai.db"}
        )

        self._dbh = Session()

        fixtures_file_path = (
            Path(__file__).parent
            / ".."
            / ".."
            / ".."
            / "fixtures"
            / "dummy_run_data.sql"
        ).absolute()
        with open(fixtures_file_path, "r") as fp:
            self._dbh.connection().connection.executescript(fp.read())

    def test_experiments_and_runs_configurations(self):
        res = palq.experiments_and_runs_configurations(self._dbh)
        self.assertEqual(2, len(res))
        self.assertTrue(
            res.experiment_run_phase_mode.isin(["train", "test"]).all()
        )

    def test_like_dataframe(self):
        erc = palq.experiments_and_runs_configurations(self._dbh)
        # Try to get data only about the test phase:
        actions = palq.muscle_actions(
            self._dbh,
            like_dataframe=erc[erc.experiment_run_phase_mode == "test"],
            predicate=lambda query: query.limit(100),
        )
        self.assertTrue(len(actions) > 1)
        self.assertTrue(actions.index[-1] > 10)
        self.assertTrue(
            actions.agent_name.isin(["Agent One", "Agent Two"]).all()
        )

    def test_get_max_experiment_run_instance_id(self):
        experiment_name = "Dummy Experiment record for ExperimentRun "
        experiment_run_uid = "Dummy experiment run where the agents take turns"

        (
            experiment_run_instance_id,
            _,
        ) = palq.get_max_experiment_run_instance_uid(
            self._dbh, experiment_name + experiment_run_uid, experiment_run_uid
        )

        self.assertEqual(
            experiment_run_instance_id, "e78b714a-8fad-411c-a0c7-bdc665fb92ad"
        )

    def test_select_agent(self):
        experiment_name = "Dummy Experiment record for ExperimentRun "
        experiment_run_uid = "Dummy experiment run where the agents take turns"

        (
            experiment_run_instance_uid,
            erc,
        ) = palq.get_max_experiment_run_instance_uid(
            self._dbh, experiment_name + experiment_run_uid, experiment_run_uid
        )

        experiment_ids = [str(erc.experiment_id.iloc[0])]
        experiment_run_uids = [str(erc.experiment_run_uid.iloc[0])]
        experiment_run_instance_uids = [
            str(erc.experiment_run_instance_uid.iloc[0])
        ]
        experiment_run_phase_uids = ["First Phase"]

        erc = palq.agents_configurations(
            self._dbh,
            experiment_ids=experiment_ids,
            experiment_run_uids=experiment_run_uids,
            experiment_run_instance_uids=experiment_run_instance_uids,
            experiment_run_phase_uids=experiment_run_phase_uids,
        )

        self.assertListEqual(
            erc.agent_name.to_list(), ["Agent Two", "Agent One"]
        )

    def test_select_muscle_actions(self):
        experiment_name = "Dummy Experiment record for ExperimentRun "
        experiment_run_uid = "Dummy experiment run where the agents take turns"

        (
            experiment_run_instance_uid,
            erc,
        ) = palq.get_max_experiment_run_instance_uid(
            self._dbh, experiment_name + experiment_run_uid, experiment_run_uid
        )

        experiment_ids = [str(erc.experiment_id.iloc[0])]
        experiment_run_uids = [str(erc.experiment_run_uid.iloc[0])]
        experiment_run_instance_uids = [
            str(erc.experiment_run_instance_uid.iloc[0])
        ]
        experiment_run_phase_uids = ["First Phase"]
        agent_uids = ["Agent One"]

        erc = palq.muscle_actions(
            self._dbh,
            experiment_ids=experiment_ids,
            experiment_run_uids=experiment_run_uids,
            experiment_run_instance_uids=experiment_run_instance_uids,
            experiment_run_phase_uids=experiment_run_phase_uids,
            agent_uids=agent_uids,
        )

        sensor_readings = erc.muscle_sensor_readings.iloc[0]
        sensor_reading_values = [
            sensor_reading.value for sensor_reading in sensor_readings
        ]
        self.assertListEqual(sensor_reading_values, [0, 0, 0, 0, 0])

        muscle_actuator_setpoints = erc.muscle_actuator_setpoints.iloc[0]
        muscle_actuator_setpoint_values = [
            muscle_actuator_setpoint.value
            for muscle_actuator_setpoint in muscle_actuator_setpoints
        ]
        self.assertListEqual(muscle_actuator_setpoint_values, [0, 0, 0, 0, 0])
        self.assertEqual(erc.muscle_action_objective.iloc[0], 1.0)

    def test_latest_muscle_action_values(self):
        experiment_name = "Dummy Experiment record for ExperimentRun "
        experiment_run_uid = "Dummy experiment run where the agents take turns"
        experiment_run_phase_uids = ["First Phase"]
        agent_uids = ["Agent One"]
        erc = palq.latest_muscle_action_values(
            self._dbh,
            experiment_name=experiment_name,
            experiment_run_uid=experiment_run_uid,
            experiment_run_phase_uids=experiment_run_phase_uids,
            agent_uids=agent_uids,
        )
        _asserted_values = {
            "myenv.0": [0, 0],
            "myenv.1": [0, 0],
            "myenv.2": [0, 0],
            "myenv.3": [0, 0],
            "myenv.4": [0, 0],
        }

        _setpoints_dict = erc.muscle_actuator_setpoints.iloc[0]

        for uid in _setpoints_dict.keys():
            self.assertEqual(_setpoints_dict[uid], _asserted_values[uid][0])

        _sensor_readings_dict = erc.muscle_sensor_readings.iloc[0]

        for uid in _sensor_readings_dict.keys():
            self.assertEqual(
                _sensor_readings_dict[uid], _asserted_values[uid][1]
            )

        self.assertEqual(erc.muscle_action_rewards.iloc[0]["Reward"], 1)

        first_simtime_ticks = erc.muscle_action_simtime_ticks.iloc[0]
        self.assertEqual(first_simtime_ticks, 306180)

        first_simtime_timestamp = erc.muscle_action_simtime_timestamp.iloc[0]
        self.assertEqual(first_simtime_timestamp, "2020-01-29 10:03:00+01:00")

        first_muscle_action_walltime = erc.muscle_action_walltime.iloc[0]
        self.assertEqual(
            str(first_muscle_action_walltime), "2023-11-02 10:52:49.002541"
        )
        self.assertEqual(erc.muscle_action_objective.iloc[0], 1.0)

    def test_latest_muscle_action_values_non_empty_multi_index(self):
        experiment_name = "Dummy Experiment record for ExperimentRun "
        experiment_run_uid = "Dummy experiment run where the agents take turns"
        experiment_run_phase_uids = ["First Phase"]
        agent_uids = ["Agent One"]
        erc = palq.latest_muscle_action_values_non_empty_multi_index(
            self._dbh,
            experiment_name=experiment_name,
            experiment_run_uid=experiment_run_uid,
            experiment_run_phase_uids=experiment_run_phase_uids,
            agent_uids=agent_uids,
        )

        self._assert_list_eq_for_all_sub_cols(
            erc.muscle_sensor_readings,
            [0, 1, 3, 5, 7, 9] * 2,
        )
        self._assert_list_eq_for_all_sub_cols(
            erc.muscle_action_rewards,
            [1, 3, 5, 7, 9, 9, 1, 3, 5, 7, 9, 9],
        )
        self._assert_list_eq_for_all_sub_cols(
            erc.muscle_actuator_setpoints, list(range(12))
        )
        self._assert_list_eq_for_all_sub_cols(
            erc.muscle_action_objective,
            [1] + [0] * 11,
        )
        self._assert_list_eq_for_all_sub_cols(
            erc.agent_uid,
            ["Agent One"] * 12,
        )
        self._assert_list_eq_for_all_sub_cols(
            erc.experiment_run_phase_uid,
            ["First Phase"] * 12,
        )
        self._assert_list_eq_for_all_sub_cols(
            erc.muscle_action_simtime_ticks,
            [
                306180,
                306300,
                306420,
                306540,
                306660,
                306720,
                306960,
                307080,
                307200,
                307320,
                307440,
                307500,
            ],
        )
        self._assert_list_eq_for_all_sub_cols(
            erc.muscle_action_simtime_timestamp,
            [
                "2020-01-29 10:03:00+01:00",
                "2020-01-29 10:05:00+01:00",
                "2020-01-29 10:07:00+01:00",
                "2020-01-29 10:09:00+01:00",
                "2020-01-29 10:11:00+01:00",
                "2020-01-29 10:12:00+01:00",
                "2020-01-29 10:16:00+01:00",
                "2020-01-29 10:18:00+01:00",
                "2020-01-29 10:20:00+01:00",
                "2020-01-29 10:22:00+01:00",
                "2020-01-29 10:24:00+01:00",
                "2020-01-29 10:25:00+01:00",
            ],
        )
        self._assert_list_eq_for_all_sub_cols(
            erc.muscle_action_walltime,
            [
                Timestamp("2023-11-02 10:52:49.002541"),
                Timestamp("2023-11-02 10:52:55.361936"),
                Timestamp("2023-11-02 10:52:55.468274"),
                Timestamp("2023-11-02 10:52:55.577098"),
                Timestamp("2023-11-02 10:52:55.739840"),
                Timestamp("2023-11-02 10:52:55.878890"),
                Timestamp("2023-11-02 10:52:56.057142"),
                Timestamp("2023-11-02 10:52:56.209354"),
                Timestamp("2023-11-02 10:52:56.357183"),
                Timestamp("2023-11-02 10:52:56.503656"),
                Timestamp("2023-11-02 10:52:56.654768"),
                Timestamp("2023-11-02 10:52:56.822018"),
            ],
        )

    def _assert_list_eq_for_all_sub_cols(
        self, erc_col: pd.DataFrame, asserted_values: List
    ):
        for column in erc_col.columns:
            self.assertListEqual(
                list(erc_col[column]),
                asserted_values,
            )

*** Settings ***
Documentation   Test Dummy Run
...
...             Exercises the fully dummy run, checking for all sorts of
...             details of the run execution. It does not check for results
...             storage explicitly, but will make sure that all log outputs
...             indicate a safe, successful and complete execution of the
...             dummy experiment run.

Library         String
Library         Process
Library         OperatingSystem
Library         ${CURDIR}${/}ConfigFileModifier.py
Resource        ${CURDIR}${/}..${/}fixtures${/}convenient_test_methods_library.resource
Suite Teardown  Clean Files
Suite Setup     Create Config Files

*** Keywords ***
Clean Files
    Remove File                     ${TEMPDIR}${/}stdout_dummy_experiment.txt
    Remove File                     ${TEMPDIR}${/}stderr_dummy_experiment.txt
    Remove File                     ${db_file_path}
    remove file                     ${runtime_config_file}
    ${test_var_to_access_from_resource}    Set Variable    test_var

Create Config Files
    ${result} =                     Run Process   palaestrai  runtime-config-show-default  stdout=${TEMPDIR}${/}palaestrai-default-runtime-dummyrun.conf.yml
    ${queueidx} =                   Get Variable Value  ${PABOTQUEUEINDEX}  0
    ${LOGPORT}                      Evaluate    str(24243 + random.randrange(1000 * (${PABOTQUEUEINDEX}+1)))
    ${EXECUTORPORT}                 Evaluate    str(24242 - random.randrange(1000 * (${PABOTQUEUEINDEX}+1)))
    ${conf} =                       Replace String  ${result.stdout}  4242  ${EXECUTORPORT}
    ${conf} =                       Replace String  ${conf}  4243  ${LOGPORT}
    ${conf} =                       Replace String  ${conf}  palaestrai.db  palaestrai-dummyrun.db
    Set Suite Variable              $runtime_config_file  ${TEMPDIR}${/}dummyrun-test-${LOGPORT}${EXECUTORPORT}.conf.yml
    Create File                     ${runtime_config_file}.old  ${conf}
    ${db_file_path} =               prepare_for_sqlite_store_test   ${runtime_config_file}.old  ${runtime_config_file}  ${TEMPDIR}
    Set Suite Variable              $db_file_path
    Log File                        ${runtime_config_file}

*** Test Cases ***
# Debug:
#   Robot stacktrace: https://github.com/MarketSquare/robotframework-stacktrace
#   Cmd:
#     pabot --command robot --listener RobotStackTracer -t "Run dummy experiment" --end-command --outputdir ./test_reports/system tests/system/test_dummy_run.robot
Run dummy experiment
    [Timeout]                       300
    ${stdout_file}    ${stderr_file} =    Create Std Files    stage_name=system    log_name=create_database
    ${contain_error} =              Create Database    stdout_file=${stdout_file}    stderr_file=${stderr_file}    runtime_config_file=${runtime_config_file}
    Should Be True                  not ${contain_error}

    ${stdout_file}    ${stderr_file} =    Create Std Files    stage_name=system    log_name=run_experiment
    ${contain_error} =              Run Experiment    stdout_file=${stdout_file}    stderr_file=${stderr_file}    experiment_file=${CURDIR}${/}..${/}fixtures${/}dummy_run.yml    runtime_config_file=${runtime_config_file}    timeout_time=5 min
    Should Be True                  not ${contain_error}

    ${file_contains_string} =       Log Contains String    test_string=set up 2 AgentConductor object(s)    log_file=${stdout_file}
    Should Be True                  ${file_contains_string}

    ${brain_dir}                    Set Variable    ${EXECDIR}${/}_outputs${/}brains/Yo-ho, a dummy experiment run for me!
    File Should Exist               ${brain_dir}${/}0${/}mighty_defender.bin
    File Should Exist               ${brain_dir}${/}0${/}evil_attacker.bin
    File Should Exist               ${brain_dir}${/}1${/}mighty_defender.bin
    File Should Exist               ${brain_dir}${/}1${/}evil_attacker.bin

Run dummy experiment with Taking Turns Simulation Controller
    [Timeout]                       300
    ${stdout_file}    ${stderr_file} =    Create Std Files    stage_name=system    log_name=create_database
    ${contain_error} =              Create Database    stdout_file=${stdout_file}    stderr_file=${stderr_file}    runtime_config_file=${runtime_config_file}
    Should Be True                  not ${contain_error}

    ${stdout_file}    ${stderr_file} =    Create Std Files    stage_name=system    log_name=run_experiment
    ${contain_error} =              Run Experiment    stdout_file=${stdout_file}    stderr_file=${stderr_file}    experiment_file=${CURDIR}${/}..${/}fixtures${/}dummy_run_taking_turns.yml    runtime_config_file=${runtime_config_file}    timeout_time=5 min
    Should Be True                  not ${contain_error}

    ${query_cmd}                    Set Variable    sqlite3 ${db_file_path} "WITH last_erp(id) AS (SELECT MAX(id) FROM experiment_run_phases), ma AS (SELECT *, LAG(muscle_actions.agent_id, 1, 0) OVER (ORDER BY muscle_actions.id) AS previous_agent_id FROM muscle_actions, last_erp JOIN agents ON muscle_actions.agent_id \= agents.id JOIN main.experiment_run_phases erp ON agents.experiment_run_phase_id \= erp.id WHERE erp.id \= last_erp.id) SELECT SUM(ma.agent_id \= ma.previous_agent_id) AS consecutive_updates FROM ma GROUP BY ma.experiment_run_phase_id;"
    ${stdout_file}                  Set Variable    ${TEMPDIR}${/}log_dummy_exp_ttsc_stdout.txt
    ${stderr_file}                  Set Variable    ${TEMPDIR}${/}log_dummy_exp_ttsc_stderr.txt

    ${stdout_file}    ${stderr_file} =    Create Std Files    stage_name=system    log_name=query_ttsc
    ${process_alias} =              Get Current Test Name Str
    ${contain_error} =              Run General Cmd    general_cmd=${query_cmd}    stdout_file=${stdout_file}    stderr_file=${stderr_file}    exec_dir=${EXECDIR}    process_alias=${process_alias}    timeout_time=2 min
    Should Be True                  not ${contain_error}

    ${result_stdout}                Get File    ${stdout_file}
    Should Be Equal As Integers    ${result_stdout}    0
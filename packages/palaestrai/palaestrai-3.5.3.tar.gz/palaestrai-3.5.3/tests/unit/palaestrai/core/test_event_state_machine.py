import asyncio
import multiprocessing
import os
import signal
import unittest
import unittest.mock
import weakref
from collections import defaultdict
from typing import List, Optional, Coroutine
from unittest.mock import patch

import time

from palaestrai.core.event_state_machine import EventStateMachine as ESM


class _MockRequest(unittest.mock.Mock):
    def __init__(self, service: Optional[str] = None):
        super().__init__()
        self.receiver = service or unittest.mock.Mock()


class _MockResponse(unittest.mock.Mock):
    def __init__(self):
        super().__init__()


class _MockProcessStartRequest(unittest.mock.Mock):
    def __init__(self):
        super().__init__()


class _MockShutdownRequest(unittest.mock.Mock):
    def __init__(self):
        super().__init__()
        self.receiver = unittest.mock.Mock()


class _MockShutdownResponse(unittest.mock.Mock):
    def __init__(self):
        super().__init__()


@ESM.monitor(is_mdp_worker=True)
class _Dummy:
    def __init__(self):
        self.is_set_up = False
        self.has_entered = False
        self.should_start_process = False
        self.is_torn_down = False
        self.process = None
        self.requests = 0
        self.responses = 0

    async def setup(self):
        self.is_set_up = True
        self.mdp_service = "Foo"

    @ESM.enter
    async def _enter(self):
        self.has_entered = True

    def teardown(self):
        self.is_torn_down = True

    @staticmethod
    def waiting_process():
        time.sleep(0.1)

    @staticmethod
    def crashing_process():
        _Dummy.waiting_process()
        raise RuntimeError("Test error, you can safely ignore this. :^)")

    @property
    def mdp_client_name(self):
        return ""

    @ESM.spawns
    def start_waiting_process(self):
        p = multiprocessing.Process(target=_Dummy.waiting_process)
        p.start()
        return p

    @ESM.spawns
    def start_crashing_process(self):
        p = multiprocessing.Process(target=_Dummy.crashing_process)
        p.start()
        return p

    @ESM.on(signal.SIGCHLD)
    def handle_terminating_process(self, process):
        self.process = process

    @ESM.requests
    def send_mock_request(self, service: Optional[str] = None):
        return _MockRequest(service)

    @ESM.on(_MockResponse)
    async def handle_mock_response(self, _):
        self.responses += 1

    @ESM.on(_MockRequest)
    async def handle_mock_request(self, _):
        self.requests += 1

    @ESM.on(_MockProcessStartRequest)
    async def _handle_start_process_request(self, _):
        self.requests += 1
        self.should_start_process = True
        _ = self.start_waiting_process()

    @ESM.on(_MockShutdownRequest)
    async def handle_shutdown_request(self, _):
        self.requests += 1
        self.stop()
        return _MockShutdownResponse()


class EventStateMachineTest(unittest.IsolatedAsyncioTestCase):
    async def test_wraps_class(self):
        dummy = _Dummy()
        self.assertIsNotNone(dummy.__esm__)

    async def test_gets_esm(self):
        dummy = _Dummy()
        esm1 = dummy.__esm__
        esm2 = dummy.__esm__
        self.assertEqual(esm1, esm2)
        self.assertEqual(esm1, ESM.esm_for(dummy))
        self.assertIn(
            (os.getpid(), weakref.ref(dummy)), ESM._monitored_objects
        )

    async def test_adds_run(self):
        dummy = _Dummy()
        self.assertTrue(getattr(dummy, "run"))
        self.assertTrue(getattr(dummy, "stop"))

    async def test_runs(self):
        dummy = _Dummy()
        asyncio.create_task(dummy.run())
        await asyncio.sleep(0.1)
        self.assertFalse(dummy.__esm__._future.done())
        dummy.stop()
        self.assertTrue(dummy.__esm__._future.done())

    async def test_monitor_process(self):
        dummy = _Dummy()
        _ = dummy.start_waiting_process()
        self.assertEqual(len(dummy.__esm__._monitored_processes), 1)
        await asyncio.wait(dummy.__esm__._monitored_processes.values())
        self.assertIsNotNone(dummy.process)
        self.assertTrue(not dummy.process.is_alive())

    @patch(
        "palaestrai.core.event_state_machine.MajorDomoClient.send",
        return_value=_MockResponse(),
    )
    async def test_sends_request_handles_response(self, send):
        dummy = _Dummy()
        _ = dummy.send_mock_request()
        self.assertTrue(len(dummy.__esm__._tasks) >= 2)
        await asyncio.wait(
            dummy.__esm__._tasks, return_when=asyncio.FIRST_COMPLETED
        )  # This is the "send_request" coro
        await asyncio.wait(
            dummy.__esm__._tasks, return_when=asyncio.FIRST_COMPLETED
        )  # This is the "_wait_for_response" coro
        await asyncio.wait(
            dummy.__esm__._tasks,
            return_when=asyncio.FIRST_COMPLETED,
            timeout=1.0,
        )  # This is the handler coro

        send.assert_awaited()
        self.assertTrue(dummy.responses == 1)

    async def test_multiple_services_send_requests_in_parallel(self):
        dummy = _Dummy()

        # barrier to hold responses until they are ready
        barrier = asyncio.Event()

        async def wait_for_barrier(*_):
            await barrier.wait()
            return _MockResponse()

        with patch(
            "palaestrai.core.event_state_machine.MajorDomoClient.send",
            side_effect=wait_for_barrier,
        ) as send:

            services = ["🦆", "🐉", "🐋", "🐉"]
            [dummy.send_mock_request(service) for service in services]
            await asyncio.wait(dummy.__esm__._tasks, timeout=1.0)

            # send was called for each unique service but we got no response
            self.assertEqual(send.call_count, 3)
            self.assertEqual(dummy.responses, 0)

            barrier.set()
            await asyncio.wait(dummy.__esm__._tasks, timeout=1.0)
            # for every request we got a response
            self.assertEqual(send.call_count, 4)
            self.assertEqual(dummy.responses, 4)

    async def test_catches_error_even_when_waiting_for_other_event(self):
        dummy = _Dummy()

        async def sleep_before_response(*_):
            await asyncio.sleep(1)
            return _MockResponse()

        with patch(
            "palaestrai.core.event_state_machine.MajorDomoClient.send",
            side_effect=sleep_before_response,
        ):
            _ = dummy.start_crashing_process()
            _ = dummy.send_mock_request()
            self.assertEqual(len(dummy.__esm__._tasks), 2)
            await asyncio.wait(
                dummy.__esm__._tasks, return_when=asyncio.FIRST_COMPLETED
            )  # Wait for our crashing process to finish

            # Check that the process handler has been fired, even if
            # we are still waiting for the sender:

            self.assertIsNotNone(dummy.process)
            self.assertEqual(dummy.process.exitcode, 1)
            self.assertTrue(len(dummy.__esm__._tasks) >= 2)

    async def test_adds_mdp_service_property(self):
        dummy = _Dummy()
        self.assertIn("mdp_service", dir(dummy))
        self.assertIsNone(dummy.mdp_service)

    @patch(
        "palaestrai.core.event_state_machine.MajorDomoWorker",
        return_value=unittest.mock.AsyncMock(
            transceive=unittest.mock.AsyncMock(
                side_effect=[_MockShutdownRequest(), None]
            )
        ),
    )
    async def test_handles_worker_receive(self, mock_mdp_worker):
        dummy = _Dummy()
        dummy.mdp_service = "Foobar"
        transceivers: List[asyncio.Task] = [
            task
            for task in dummy.__esm__._tasks
            if task.get_name() == "Transceiver"
        ]
        self.assertIsNotNone(dummy.__esm__._mdp_worker)
        self.assertEqual(1, len(transceivers))
        await asyncio.wait(transceivers, timeout=2.0)
        self.assertTrue(transceivers[0].done())

    @patch(
        "palaestrai.core.event_state_machine.MajorDomoWorker",
        return_value=unittest.mock.AsyncMock(
            transceive=unittest.mock.AsyncMock(
                side_effect=[
                    _MockRequest(),
                    _MockProcessStartRequest(),
                    _MockShutdownRequest(),
                    None,
                ]
            )
        ),
    )
    async def test_full_run(self, mock_mdp_worker):
        dummy = _Dummy()
        await dummy.run()
        self.assertTrue(dummy.is_set_up)
        self.assertTrue(dummy.has_entered)
        self.assertTrue(dummy.should_start_process)
        self.assertIsNotNone(dummy.process)
        self.assertTrue(dummy.is_torn_down)
        self.assertEqual(dummy.requests, 3)


if __name__ == "__main__":
    unittest.main()

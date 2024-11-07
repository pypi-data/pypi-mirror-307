from __future__ import annotations

from palaestrai.core.protocol import EnvironmentUpdateResponse
from palaestrai.experiment import TerminationCondition


class EnvironmentTerminationCondition(TerminationCondition):
    """Terminates the current phase when an ::`~Environment` terminates

    This :class:`~TerminationCondition` examines updates from an
    :class:`~Environment` and checks whether the environment itself signals
    termination.
    """

    def check_termination(self, message, component=None):
        """Checks for environment termination

        Parameters
        ----------
        message : Any
            Examines :class:`~EnvironmentUpdateResponse` messages for
            ::`~EnvironmentUpdateResponse.is_teminal`.
        component : Any
            unused

        Returns
        -------
        bool
            ``True`` if ``message.is_terminal``.
        """
        return isinstance(message, EnvironmentUpdateResponse) and message.done

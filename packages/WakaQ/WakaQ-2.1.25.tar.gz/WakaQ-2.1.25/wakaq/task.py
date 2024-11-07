from datetime import timedelta

from .queue import Queue


class Task:
    __slots__ = [
        "name",
        "fn",
        "wakaq",
        "queue",
        "soft_timeout",
        "hard_timeout",
        "max_retries",
    ]

    def __init__(self, fn=None, wakaq=None, queue=None, soft_timeout=None, hard_timeout=None, max_retries=None):
        self.fn = fn
        self.name = fn.__name__
        self.wakaq = wakaq
        if queue:
            self.queue = Queue.create(queue, queues_by_name=self.wakaq.queues_by_name)
        else:
            self.queue = None

        self.soft_timeout = soft_timeout.total_seconds() if isinstance(soft_timeout, timedelta) else soft_timeout
        self.hard_timeout = hard_timeout.total_seconds() if isinstance(hard_timeout, timedelta) else hard_timeout

        if self.soft_timeout and self.hard_timeout and self.hard_timeout <= self.soft_timeout:
            raise Exception(
                f"Task hard timeout ({self.hard_timeout}) can not be less than or equal to soft timeout ({self.soft_timeout})."
            )

        self.max_retries = int(max_retries) if max_retries else None

        self.fn.delay = self._delay
        self.fn.broadcast = self._broadcast

    def _delay(self, *args, **kwargs):
        """Run task in the background."""

        queue = kwargs.pop("queue", None) or self.queue
        eta = kwargs.pop("eta", None)

        if self.wakaq.synchronous_mode:
            return self.fn(*args, **kwargs)

        if eta:
            self.wakaq._enqueue_with_eta(self.name, queue, args, kwargs, eta)
        else:
            self.wakaq._enqueue_at_end(self.name, queue, args, kwargs)

    def _broadcast(self, *args, **kwargs) -> int:
        """Run task in the background on all workers.

        Only runs the task once per worker parent daemon, no matter the worker's concurrency.

        Returns the number of workers the task was sent to.
        """

        return self.wakaq._broadcast(self.name, args, kwargs)

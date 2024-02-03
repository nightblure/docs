import abc
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import threading
import time
from collections import deque
from dataclasses import dataclass
from enum import Enum
from threading import Thread
from typing import Callable


class EventHandlerRunStrategy(Enum):
    DEFAULT = 'default'
    THREAD = 'thread'
    COROUTINE = 'coroutine'
    THREAD_POOL = 'thread_pool'


class EventBase:
    handler_run_strategy = EventHandlerRunStrategy.DEFAULT


class AbstractEventHandlerRunStrategy(abc.ABC):
    def __init__(self, handler: Callable[[EventBase], None]):
        self.handler = handler

    @abc.abstractmethod
    def run_handler(self, e: EventBase):
        raise NotImplementedError()


EVENT_HANDLER_RUN_STRATEGY_TO_STRATEGY_CLS_TYPING = dict[
    EventHandlerRunStrategy,
    type(AbstractEventHandlerRunStrategy)
]

EVENT_TO_HANDLERS_TYPING = dict[
    type[EventBase],
    Callable | tuple[Callable] | list[Callable]
]


class EventHandlerRunDefaultStrategy(AbstractEventHandlerRunStrategy):
    def run_handler(self, e: EventBase):
        self.handler(e)


class EventHandlerRunThreadStrategy(AbstractEventHandlerRunStrategy):
    THREAD_NAME_PREFIX = 'EVENT_HANDLER_THREAD'

    def run_handler(self, e: EventBase):
        thread_name = f'{self.THREAD_NAME_PREFIX}_{datetime.now(tz=timezone.utc)}'
        thread = Thread(target=self.handler, name=thread_name, args=(e,))
        thread.start()


class EventHandlerRunCoroutineStrategy(AbstractEventHandlerRunStrategy):
    async def run_handler(self, e: EventBase):
        task = asyncio.create_task(self.handler(e))
        await task


class EventHandlerRunThreadPoolStrategy(AbstractEventHandlerRunStrategy):
    def run_handler(self, e: EventBase):
        with ThreadPoolExecutor() as executor:
            future = executor.submit(self.handler, e)
            _ = future.result()


@dataclass
class ThreadEvent(EventBase):
    name: str
    handler_run_strategy = EventHandlerRunStrategy.THREAD


@dataclass
class CoroutineEvent(EventBase):
    name: str
    handler_run_strategy = EventHandlerRunStrategy.COROUTINE


@dataclass
class ThreadPoolEvent(EventBase):
    name: str
    handler_run_strategy = EventHandlerRunStrategy.THREAD_POOL


@dataclass
class DefaultEvent(EventBase):
    name: str
    handler_run_strategy = EventHandlerRunStrategy.THREAD_POOL


def default_handler(e: DefaultEvent):
    print('success handling', e.name)


def thread_handler(e: ThreadEvent):
    time.sleep(5)
    print('success handling', e.name)


async def coro_handler(e: CoroutineEvent):
    time.sleep(10)
    print('success handling', e.name)


def thpool_handler(e: ThreadPoolEvent):
    print('success handling', e.name)


EVENT_TO_HANDLERS: EVENT_TO_HANDLERS_TYPING = {
    DefaultEvent: default_handler,
    ThreadEvent: thread_handler,
    ThreadPoolEvent: thpool_handler,
    CoroutineEvent: coro_handler
}


class EventsBus:
    EVENT_HANDLER_RUN_STRATEGY_TO_STRATEGY_CLS: EVENT_HANDLER_RUN_STRATEGY_TO_STRATEGY_CLS_TYPING = (
        {
            EventHandlerRunStrategy.DEFAULT: EventHandlerRunDefaultStrategy,
            EventHandlerRunStrategy.THREAD: EventHandlerRunThreadStrategy,
            # EventHandlerRunStrategy.COROUTINE: EventHandlerRunCoroutineStrategy,
            EventHandlerRunStrategy.THREAD_POOL: EventHandlerRunThreadPoolStrategy
        }
    )

    def __init__(
            self,
            event_to_handlers: EVENT_TO_HANDLERS_TYPING
    ):
        self.queue: deque[EventBase] = deque()
        self.event_to_handlers = event_to_handlers
        self._stop = True
        self.thread = Thread(target=self.__run_events_handling)

    def publish(self, e: EventBase):
        self.queue.appendleft(e)

    def stop(self):
        self._stop = True

    def run(self):
        self._stop = False
        self.thread.start()

    @property
    def active_threads_count(self):
        thread_strategy_class = (
            self.EVENT_HANDLER_RUN_STRATEGY_TO_STRATEGY_CLS[EventHandlerRunStrategy.THREAD]
        )

        bus_active_threads = [
            t for t in threading.enumerate()
            if t.name.startswith(thread_strategy_class.THREAD_NAME_PREFIX)
        ]

        return len(bus_active_threads)

    def __run_events_handling(self):
        print('Start events handling...')

        while not self._stop:
            if len(self.queue) == 0:
                continue

            e = self.queue.pop()

            handlers = self.event_to_handlers[type(e)]

            if not isinstance(handlers, list) and not isinstance(handlers, tuple):
                handlers = [handlers]

            handler_run_strategy_cls: type(AbstractEventHandlerRunStrategy) = (
                self.EVENT_HANDLER_RUN_STRATEGY_TO_STRATEGY_CLS[e.handler_run_strategy]
            )

            for handler in handlers:
                strategy_instance = handler_run_strategy_cls(handler)
                strategy_instance.run_handler(e)

            # print('Events queue is empty')
            time.sleep(1)

        print('Stop events handling')


def main():
    bus = EventsBus(
        event_to_handlers=EVENT_TO_HANDLERS
    )
    bus.run()

    try:
        while True:
            cmd = input()
            print('')

            if cmd == 'stop':
                bus.stop()
                break

            if cmd == 'def':
                e = DefaultEvent(name='default event')
                bus.publish(e)

            if cmd == 'th':
                e = ThreadEvent(name='thread event')
                bus.publish(e)

            if cmd == 'thpool':
                bus.publish(ThreadPoolEvent(name='thpool event'))

            if cmd == 'coro':
                bus.publish(CoroutineEvent(name='coro event'))

            if cmd == 'tlen':
                print('active threads', bus.active_threads_count)

    except KeyboardInterrupt:
        bus.stop()


if __name__ == '__main__':
    main()


from collections import namedtuple, deque
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


Amplifier = namedtuple('Amplifier', ['func', 'phase', 'inputs'])


class Halt(Exception):
    pass


def amplifier(name):
    logger.info(f'Running {amplifier.__name__} for amplifier {name}')
    i = 0

    while True:
        logger.info(f'{name} loop : {i}')
        if i > 5:
            logger.warning(f'{name} halting!')
            raise Halt

        x = yield

        calculation = x*2
        logger.info(f'{name} yielding {calculation}')

        yield calculation
        i += 1


feedback_loop_config = deque([
    Amplifier(amplifier('A'), 9, deque([1])),
    Amplifier(amplifier('B'), 8, deque([])),
    Amplifier(amplifier('C'), 7, deque([])),
    Amplifier(amplifier('D'), 6, deque([])),
    Amplifier(amplifier('E'), 5, deque([]))
])


if __name__ == '__main__':

    while True:
        amp = feedback_loop_config.popleft()

        while amp.inputs:
            if amp.phase is not None:
                next(amp.func)
                amp.func.send(amp.phase)
                amp = Amplifier(amp.func, None, amp.inputs)

            else:
                next(amp.func)
                feedback_loop_config[0].inputs.appendleft(amp.func.send(amp.inputs.popleft()))

        feedback_loop_config.append(amp)


















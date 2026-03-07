
import pytest
import inspect

def test_dispatcher_has_no_io_or_sleep():
    try:
        from core.outbox import dispatcher
    except ModuleNotFoundError:
        pytest.skip('outbox.dispatcher not implemented.')
    src = inspect.getsource(dispatcher)
    forbidden = [
        'time.sleep', 'asyncio.sleep', 'threading.', 'multiprocessing.',
        'open(', 'requests.', 'httpx.', 'socket.', 'subprocess.', 'os.system('
    ]
    assert not any(tok in src for tok in forbidden), 'Dispatcher must be pure state machine'

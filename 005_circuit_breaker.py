"""
Circuit Breaker Pattern -- a mini system design project.

The idea: when you call something unreliable (an external API, a flaky
database, a slow AI service), you don't want ONE broken dependency to
take down your whole app. A circuit breaker "trips" after too many
failures and starts failing fast instead of hanging or crashing --
then automatically tries again after a cooldown.

Three states:
    CLOSED     -> everything's fine, calls go through normally.
    OPEN       -> too many failures happened, calls are rejected
                  immediately without even trying (fail fast).
    HALF_OPEN  -> cooldown period is over, we cautiously let ONE
                  call through to test if the dependency recovered.

This is the same instinct behind "a bad PDF shouldn't crash the
server" -- just generalized into a reusable pattern instead of a
one-off fix.
"""

import time
from enum import Enum


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitOpenError(Exception):
    """Raised when the circuit is open and a call is rejected immediately."""
    pass


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 5.0):
        """
        failure_threshold: how many consecutive failures before the
                            circuit trips open.
        recovery_timeout:  how many seconds to wait before allowing
                            a test call through (half-open).
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.opened_at = None

    def call(self, func, *args, **kwargs):
        """Run func(*args, **kwargs) through the circuit breaker."""

        if self.state == CircuitState.OPEN:
            if self._cooldown_elapsed():
                # Cooldown is over -- allow one test call through.
                self.state = CircuitState.HALF_OPEN
            else:
                # Still cooling down. Fail fast, don't even try.
                raise CircuitOpenError(
                    "Circuit is open -- rejecting call without attempting it."
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            self._record_failure()
            raise
        else:
            self._record_success()
            return result

    def _record_failure(self):
        self.failure_count += 1
        if self.state == CircuitState.HALF_OPEN:
            # The test call failed -- go straight back to OPEN.
            self._trip()
        elif self.failure_count >= self.failure_threshold:
            self._trip()

    def _record_success(self):
        # Any success resets things -- we're healthy again.
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.opened_at = None

    def _trip(self):
        self.state = CircuitState.OPEN
        self.opened_at = time.monotonic()

    def _cooldown_elapsed(self) -> bool:
        return (time.monotonic() - self.opened_at) >= self.recovery_timeout


# ---------------------------------------------------------------------------
# Demo: simulating a flaky external call (e.g. a slow/unstable AI API)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    call_count = {"n": 0}

    def flaky_external_call():
        """Fails on calls 1-3, then recovers permanently from call 4 onward."""
        call_count["n"] += 1
        if call_count["n"] <= 3:
            raise ConnectionError(f"Simulated failure #{call_count['n']}")
        return "success"

    breaker = CircuitBreaker(failure_threshold=2, recovery_timeout=1.5)

    for attempt in range(1, 7):
        try:
            result = breaker.call(flaky_external_call)
            print(f"Attempt {attempt}: SUCCESS -> {result} (state={breaker.state.value})")
        except CircuitOpenError:
            print(f"Attempt {attempt}: REJECTED FAST -- circuit is open (state={breaker.state.value})")
        except ConnectionError as e:
            print(f"Attempt {attempt}: FAILED -> {e} (state={breaker.state.value})")

        # Whenever the circuit is open, wait out the cooldown so the next
        # attempt gets a real half-open test instead of another fast reject.
        if breaker.state == CircuitState.OPEN:
            print("--- circuit open: waiting out the cooldown ---")
            time.sleep(breaker.recovery_timeout + 0.1)

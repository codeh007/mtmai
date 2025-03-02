from typing import Callable

from autogen_core import CancellationToken


class MtCancelToken(CancellationToken):
    def __init__(
        self, lambda_cancel: Callable[[], None], is_cancelled: Callable[[], bool]
    ):
        # self.is_cancelled = False
        self.lambda_cancel: Callable[[], None] = lambda_cancel
        self.is_cancelled: Callable[[], bool] = is_cancelled
        super().__init__()

    def cancel(self):
        if self.lambda_cancel:
            return self.lambda_cancel()

    def is_cancelled(self):
        if self.is_cancelled:
            return self.is_cancelled()

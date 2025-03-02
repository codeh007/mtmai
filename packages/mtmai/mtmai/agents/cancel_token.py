from autogen_core import CancellationToken

from mtmai.context.ctx import get_step_canceled_ctx, set_step_canceled_ctx


class MtCancelToken(CancellationToken):
    def cancel(self):
        set_step_canceled_ctx(True)

    def is_cancelled(self):
        return get_step_canceled_ctx()

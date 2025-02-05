from ..agents.ctx import AgentContext


class ApiService:
    def __init__(self, ctx: AgentContext):
        self.ctx = ctx

    # def get_hatchet(self):
    #     return self.ctx.hatchet
    def getDefaultModel(self):
        return self.ctx.hatchet.getDefaultModel()

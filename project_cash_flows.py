class ProjectCashFlows:
    project_name = ""
    project_cash_flows = []
    project_period = 0
    project_invest = 0
    project_npv = 0

    def __init__(self, project_name, project_cach_flows):
        self.project_name = project_name
        self.project_cash_flows = project_cach_flows
        self.project_period = len(project_cach_flows)
        for cash in project_cach_flows:
            if cash < 0:
                self.project_invest += cash
            else:
                break
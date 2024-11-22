class ProjectAnalysis:
    project_name = ""
    project_cash_flows = []
    project_period = 0
    project_invest = 0
    project_npv = 0
    project_fixed_cost = 0
    project_total_cost = 0
    project_production_capacticy = 0
    project_selling_price = 0

    def __init__(self, project_name, project_cach_flows,project_fixed_cost,project_total_cost,project_production_capacticy,project_selling_price):
        self.project_name = project_name
        self.project_cash_flows = project_cach_flows
        self.project_period = len(project_cach_flows)
        for cash in project_cach_flows:
            if cash < 0:
                self.project_invest += cash
            else:
                break
        self.project_fixed_cost = project_fixed_cost
        self.project_total_cost = project_total_cost
        self.project_production_capacticy = project_production_capacticy
        self.project_selling_price = project_selling_price


from typing import List


class ProjectAnalysis:
    project_name = ""
    project_cash_flows = []
    project_period = 0
    project_invest = 0
    project_npv = 0
    project_irr = 0
    project_fixed_cost = 0
    project_total_cost = 0
    project_production_capacticy = 0
    project_selling_price = 0
    project_cash_flows_in = []
    project_cash_flows_out = []
    project_dynamic_cycle = 0
    project_static_cycle = 0
    project_opposites = []
    distance = 100
    variable_cost = 0

    def __init__(self, project_name:str, project_cash_flows_in:List,project_cash_flows_out:List
                 ,project_fixed_cost:float,project_total_cost:float,project_production_capacticy:int,project_selling_price:float,discount_rate:float,project_opposites:List[str]):
        self.project_name = project_name
        self.project_cash_flows_in = project_cash_flows_in
        self.project_cash_flows_out = project_cash_flows_out
        self.project_invest = project_cash_flows_out[0]
        project_cash_flows,project_period,distance = combined_cash_flows(project_cash_flows_in,project_cash_flows_out,self.distance)
        self.project_cash_flows = project_cash_flows
        self.project_period = project_period
        self.project_npv = npv(self.project_cash_flows,discount_rate)
        self.project_fixed_cost = project_fixed_cost * 10000
        self.project_total_cost = project_total_cost * 10000
        self.project_production_capacticy = project_production_capacticy * 10000
        self.project_selling_price = project_selling_price
        self.project_opposites = project_opposites
        self.distance = distance * 0.9



# 计算净现值
def npv(cash_flows, discount_rate):
    n = len(cash_flows)
    return sum(round(cash_flows[i] / (1 + discount_rate)**i,2) for i in range(n))


# 合并现金流
def combined_cash_flows(project_cash_flows_in,project_cash_flows_out,distance):
    project_cash_flows = []
    project_period = len(project_cash_flows_in)
    for i in range(len(project_cash_flows_in)):
        project_cash_flows.append(round(project_cash_flows_in[i] - project_cash_flows_out[i],2))
        if 0 < project_cash_flows_in[i] < distance:
            distance = project_cash_flows_in[i]
        if 0 < project_cash_flows_out[i] < distance:
            distance = project_cash_flows_out[i]
    return project_cash_flows,project_period,distance

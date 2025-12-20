class Employee:
    def __init__(self, employee_id, name, department, working=True):
        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.working = working

class EmployeeStatus:
    def terminate(self, employee):
        employee.working = False

    def is_working(self, employee):
        return employee.working

class EmployeeRepository:
    def save_to_database(self, employee):
        pass

class EmployeeReportXML:
    def print(self, employee):
        pass

class EmployeeReportCSV:
    def print(self, employee):
        pass

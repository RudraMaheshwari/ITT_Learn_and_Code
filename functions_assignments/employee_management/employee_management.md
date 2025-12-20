Class Employee
{
int id;
string name;
string department;
bool working;

public:
saveEmployeeTODatabase()
printEmployeeDetailReportXML()
printEmployeeDetailReportCSV()
terminateEmployee()
bool isWorking()
};

## Here the SRP is violated as the class is handling too many responsibilities.

- Save employee to database
- Print employee detail report in XML
- Print employee detail report in CSV
- Terminate employee
- Check if employee is working

## so its now divided into multiple classes which is available in the folder employee_management

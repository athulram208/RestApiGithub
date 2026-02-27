from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

employees_bp = Blueprint("employees", __name__)

# In-memory list of employees
employees = []
current_id = 1


# Create an employee
@employees_bp.route("", methods=["POST"])
@jwt_required()
def create_employee():
    global current_id

    data = request.get_json() or {}

    employee = {
        "EmployeeID": current_id,
        "FirstName": data.get("FirstName", ""),
        "LastName": data.get("LastName", ""),
        "Gender": data.get("Gender", ""),
        "DateOfBirth": data.get("DateOfBirth", ""),
        "DepartmentID": data.get("DepartmentID", "")
    }

    employees.append(employee)
    current_id += 1

    return jsonify(employee), 201


# Get all employees
@employees_bp.route("", methods=["GET"])
@jwt_required()
def list_employees():
    return jsonify({
        "count": len(employees),
        "data": employees
    }), 200


# Get single employee by ID
@employees_bp.route("/<int:employee_id>", methods=["GET"])
@jwt_required()
def get_employee(employee_id):
    employee = next(
        (emp for emp in employees if emp["EmployeeID"] == employee_id),
        None
    )

    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    return jsonify(employee), 200


# Update employee by ID
@employees_bp.route("/<int:employee_id>", methods=["PUT"])
@jwt_required()
def update_employee(employee_id):
    data = request.get_json() or {}

    employee = next(
        (emp for emp in employees if emp["EmployeeID"] == employee_id),
        None
    )

    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    employee["FirstName"] = data.get("FirstName", employee["FirstName"])
    employee["LastName"] = data.get("LastName", employee["LastName"])
    employee["Gender"] = data.get("Gender", employee["Gender"])
    employee["DateOfBirth"] = data.get("DateOfBirth", employee["DateOfBirth"])
    employee["DepartmentID"] = data.get("DepartmentID", employee["DepartmentID"])

    return jsonify(employee), 200


# Delete employee by ID
@employees_bp.route("/<int:employee_id>", methods=["DELETE"])
@jwt_required()
def delete_employee(employee_id):
    global employees

    employee = next(
        (emp for emp in employees if emp["EmployeeID"] == employee_id),
        None
    )

    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    employees = [emp for emp in employees if emp["EmployeeID"] != employee_id]

    return jsonify({"message": "Employee deleted"}), 200
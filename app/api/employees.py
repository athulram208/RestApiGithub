# app/api/employees.py
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

    return jsonify({"employee": employee}), 201

# Get all employees
@employees_bp.route("", methods=["GET"])
@jwt_required()
def list_employees():
    return jsonify({
        "count": len(employees),
        "employees": employees
    }), 200

# Get single employee by ID
@employees_bp.route("/<int:employee_id>", methods=["GET"])
@jwt_required()
def get_employee(employee_id):
    for emp in employees:
        if emp["EmployeeID"] == employee_id:
            return jsonify(emp), 200

    return jsonify({"message": "Employee not found"}), 404

# Update employee by ID
@employees_bp.route("/<int:employee_id>", methods=["PUT"])
@jwt_required()
def update_employee(employee_id):
    data = request.get_json() or {}

    for emp in employees:
        if emp["EmployeeID"] == employee_id:
            emp["FirstName"] = data.get("FirstName", emp["FirstName"])
            emp["LastName"] = data.get("LastName", emp["LastName"])
            emp["Gender"] = data.get("Gender", emp["Gender"])
            emp["DateOfBirth"] = data.get("DateOfBirth", emp["DateOfBirth"])
            emp["DepartmentID"] = data.get("DepartmentID", emp["DepartmentID"])
            return jsonify({"employee": emp}), 200

    return jsonify({"message": "Employee not found"}), 404

# Delete employee by ID
@employees_bp.route("/<int:employee_id>", methods=["DELETE"])
@jwt_required()
def delete_employee(employee_id):
    global employees
    for emp in employees:
        if emp["EmployeeID"] == employee_id:
            employees = [e for e in employees if e["EmployeeID"] != employee_id]
            return jsonify({"message": "Employee deleted"}), 200

    return jsonify({"message": "Employee not found"}), 404
import React, { useState, useEffect } from 'react';
import { employeeAPI } from '../services/api';
import EmployeeModal from '../components/EmployeeModal';

const Employees = () => {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetchEmployees();
  }, []);

  const fetchEmployees = async () => {
    try {
      setLoading(true);
      const response = await employeeAPI.getAll();
      setEmployees(response.data.data);
    } catch (err) {
      setError('Failed to load employees');
      console.error('Fetch employees error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddEmployee = async (employeeData) => {
    try {
      await employeeAPI.create(employeeData);
      setSuccess('Employee added successfully');
      setShowModal(false);
      fetchEmployees();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Failed to add employee';
      setError(errorMessage);
      setTimeout(() => setError(''), 3000);
    }
  };

  const handleDeleteEmployee = async (id) => {
    if (window.confirm('Are you sure you want to delete this employee?')) {
      try {
        await employeeAPI.delete(id);
        setSuccess('Employee deleted successfully');
        fetchEmployees();
        setTimeout(() => setSuccess(''), 3000);
      } catch (err) {
        setError('Failed to delete employee');
        setTimeout(() => setError(''), 3000);
      }
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <h3>Loading employees...</h3>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Employees</h1>
        <p className="page-subtitle">Manage your employee records</p>
      </div>

      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}

      {success && (
        <div className="alert alert-success">
          {success}
        </div>
      )}

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Employee List</h2>
          <button 
            className="btn btn-primary"
            onClick={() => setShowModal(true)}
          >
            Add Employee
          </button>
        </div>

        {employees.length === 0 ? (
          <div className="empty-state">
            <h3>No employees found</h3>
            <p>Start by adding your first employee</p>
            <button 
              className="btn btn-primary"
              onClick={() => setShowModal(true)}
            >
              Add Employee
            </button>
          </div>
        ) : (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Employee ID</th>
                  <th>Full Name</th>
                  <th>Email</th>
                  <th>Department</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {employees.map((employee) => (
                  <tr key={employee.id}>
                    <td>{employee.employee_id}</td>
                    <td>{employee.full_name}</td>
                    <td>{employee.email}</td>
                    <td>{employee.department}</td>
                    <td>
                      <button
                        className="btn btn-danger"
                        onClick={() => handleDeleteEmployee(employee.id)}
                        style={{ fontSize: '12px', padding: '6px 12px' }}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {showModal && (
        <EmployeeModal
          onClose={() => setShowModal(false)}
          onSubmit={handleAddEmployee}
        />
      )}
    </div>
  );
};

export default Employees;
import React, { useState, useEffect } from 'react';
import { employeeAPI, attendanceAPI } from '../services/api';
import AttendanceModal from '../components/AttendanceModal';

const Attendance = () => {
  const [attendanceRecords, setAttendanceRecords] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [filters, setFilters] = useState({
    employee_id: '',
    date: ''
  });

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    fetchAttendanceRecords();
  }, [filters]); // eslint-disable-line react-hooks/exhaustive-deps

  const fetchData = async () => {
    try {
      setLoading(true);
      const [employeesRes, attendanceRes] = await Promise.all([
        employeeAPI.getAll(),
        attendanceAPI.getAll()
      ]);
      
      setEmployees(employeesRes.data.data);
      setAttendanceRecords(attendanceRes.data.data);
    } catch (err) {
      setError('Failed to load data');
      console.error('Fetch data error:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchAttendanceRecords = async () => {
    try {
      const params = {};
      if (filters.employee_id) params.employee_id = filters.employee_id;
      if (filters.date) params.date = filters.date;
      
      const response = await attendanceAPI.getAll(params);
      setAttendanceRecords(response.data.data);
    } catch (err) {
      console.error('Fetch attendance error:', err);
    }
  };

  const handleMarkAttendance = async (attendanceData) => {
    try {
      await attendanceAPI.create(attendanceData);
      setSuccess('Attendance marked successfully');
      setShowModal(false);
      fetchAttendanceRecords();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Failed to mark attendance';
      setError(errorMessage);
      setTimeout(() => setError(''), 3000);
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const clearFilters = () => {
    setFilters({
      employee_id: '',
      date: ''
    });
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="loading">
        <h3>Loading attendance data...</h3>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Attendance</h1>
        <p className="page-subtitle">Track and manage employee attendance</p>
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

      {/* Filters */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Filters</h2>
        </div>
        <div style={{ display: 'flex', gap: '15px', alignItems: 'end', flexWrap: 'wrap' }}>
          <div className="form-group" style={{ minWidth: '200px', marginBottom: 0 }}>
            <label className="form-label">Employee</label>
            <select
              name="employee_id"
              value={filters.employee_id}
              onChange={handleFilterChange}
              className="form-select"
            >
              <option value="">All Employees</option>
              {employees.map(employee => (
                <option key={employee.employee_id} value={employee.employee_id}>
                  {employee.employee_id} - {employee.full_name}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group" style={{ minWidth: '150px', marginBottom: 0 }}>
            <label className="form-label">Date</label>
            <input
              type="date"
              name="date"
              value={filters.date}
              onChange={handleFilterChange}
              className="form-input"
            />
          </div>
          <button
            className="btn btn-secondary"
            onClick={clearFilters}
            style={{ height: 'fit-content' }}
          >
            Clear Filters
          </button>
        </div>
      </div>

      {/* Attendance Records */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Attendance Records</h2>
          <button 
            className="btn btn-primary"
            onClick={() => setShowModal(true)}
          >
            Mark Attendance
          </button>
        </div>

        {attendanceRecords.length === 0 ? (
          <div className="empty-state">
            <h3>No attendance records found</h3>
            <p>Start by marking attendance for employees</p>
            <button 
              className="btn btn-primary"
              onClick={() => setShowModal(true)}
            >
              Mark Attendance
            </button>
          </div>
        ) : (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Employee ID</th>
                  <th>Employee Name</th>
                  <th>Department</th>
                  <th>Date</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {attendanceRecords.map((record) => (
                  <tr key={record.id}>
                    <td>{record.employee_details.employee_id}</td>
                    <td>{record.employee_details.full_name}</td>
                    <td>{record.employee_details.department}</td>
                    <td>{formatDate(record.date)}</td>
                    <td>
                      <span 
                        style={{
                          padding: '4px 8px',
                          borderRadius: '4px',
                          fontSize: '12px',
                          fontWeight: '500',
                          backgroundColor: record.status === 'Present' ? '#d4edda' : '#f8d7da',
                          color: record.status === 'Present' ? '#155724' : '#721c24'
                        }}
                      >
                        {record.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {showModal && (
        <AttendanceModal
          employees={employees}
          onClose={() => setShowModal(false)}
          onSubmit={handleMarkAttendance}
        />
      )}
    </div>
  );
};

export default Attendance;
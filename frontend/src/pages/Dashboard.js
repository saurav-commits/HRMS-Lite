import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { employeeAPI, attendanceAPI } from '../services/api';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalEmployees: 0,
    totalAttendanceRecords: 0,
    presentToday: 0,
    absentToday: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const today = new Date().toISOString().split('T')[0];
      
      const [employeesRes, attendanceRes, todayAttendanceRes] = await Promise.all([
        employeeAPI.getAll(),
        attendanceAPI.getAll(),
        attendanceAPI.getAll({ date: today })
      ]);

      const todayRecords = todayAttendanceRes.data.data;
      const presentToday = todayRecords.filter(record => record.status === 'Present').length;
      const absentToday = todayRecords.filter(record => record.status === 'Absent').length;

      setStats({
        totalEmployees: employeesRes.data.count,
        totalAttendanceRecords: attendanceRes.data.count,
        presentToday,
        absentToday
      });
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <h3>Loading dashboard...</h3>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-error">
        {error}
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Dashboard</h1>
        <p className="page-subtitle">Overview of your HRMS system</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-number">{stats.totalEmployees}</div>
          <div className="stat-label">Total Employees</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{stats.totalAttendanceRecords}</div>
          <div className="stat-label">Total Attendance Records</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{stats.presentToday}</div>
          <div className="stat-label">Present Today</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{stats.absentToday}</div>
          <div className="stat-label">Absent Today</div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Quick Actions</h2>
        </div>
        <div style={{ display: 'flex', gap: '15px', flexWrap: 'wrap' }}>
          <Link to="/employees" className="btn btn-primary">
            Manage Employees
          </Link>
          <Link to="/attendance" className="btn btn-success">
            Mark Attendance
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

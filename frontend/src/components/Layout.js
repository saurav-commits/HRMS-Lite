import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Layout = ({ children }) => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <div className="layout">
      <div className="sidebar">
        <div className="sidebar-header">
          <h1>HRMS Lite</h1>
        </div>
        <nav>
          <ul className="sidebar-nav">
            <li>
              <Link to="/dashboard" className={isActive('/dashboard')}>
                📊 Dashboard
              </Link>
            </li>
            <li>
              <Link to="/employees" className={isActive('/employees')}>
                👥 Employees
              </Link>
            </li>
            <li>
              <Link to="/attendance" className={isActive('/attendance')}>
                📅 Attendance
              </Link>
            </li>
          </ul>
        </nav>
      </div>
      <div className="main-content">
        {children}
      </div>
    </div>
  );
};

export default Layout;
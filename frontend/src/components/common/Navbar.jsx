import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link } from "react-router-dom";

import { setActivePage } from "../../redux/features/activePageSlice.js";

const Navbar = () => {
  const disptach = useDispatch();

  const { activePage } = useSelector((state) => state.activePage);

  return (
    <header id="navbar">
      <ul>
        <li
          onClick={() => disptach(setActivePage(0))}
          className={activePage === 0 ? "active" : null}
        >
          <Link to="/">Home</Link>
        </li>
        <li
          onClick={() => disptach(setActivePage(1))}
          className={activePage === 1 ? "active" : null}
        >
          <Link to="/analytics">Analytics Dashboard</Link>
        </li>
        <li
          onClick={() => disptach(setActivePage(2))}
          className={activePage === 2 ? "active" : null}
        >
          <Link to="/complaints">Complaint History</Link>
        </li>
        <li
          onClick={() => disptach(setActivePage(3))}
          className={activePage === 3 ? "active" : null}
        >
          <Link to="/file-complaint">File Complaint</Link>
        </li>
      </ul>
    </header>
  );
};

export default Navbar;

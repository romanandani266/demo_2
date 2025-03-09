import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Inventory from "./components/Inventory";
import Alerts from "./components/Alerts";
import SalesTrends from "./components/SalesTrends";
import Login from "./components/Login";

const App = () => {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<h1>Welcome to Retail Inventory Management</h1>} />
        <Route path="/inventory" element={<Inventory />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/sales-trends" element={<SalesTrends />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </div>
  );
};

export default App;

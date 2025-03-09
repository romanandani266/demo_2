import React, { useState } from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./components/Login";
import Inventory from "./components/Inventory";
import Alerts from "./components/Alerts";
import SalesTrends from "./components/SalesTrends";

const App = () => {
  const [token, setToken] = useState(null);

  if (!token) {
    return <Login setToken={setToken} />;
  }

  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<h1>Welcome to Retail Inventory Management</h1>} />
        <Route path="/inventory" element={<Inventory token={token} />} />
        <Route path="/alerts" element={<Alerts token={token} />} />
        <Route path="/sales-trends" element={<SalesTrends token={token} />} />
      </Routes>
    </>
  );
};

export default App;

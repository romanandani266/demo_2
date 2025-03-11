import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import { AppBar, Toolbar, Button, Typography } from "@mui/material";
import Inventory from "./components/Inventory";
import Alerts from "./components/Alerts";
import SalesTrends from "./components/SalesTrends";
import Products from "./components/Products";
import Locations from "./components/Locations";
import Login from "./components/Login";

const App = () => {
  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" style={{ flexGrow: 1 }}>
            Retail Inventory Management
          </Typography>
          <Button color="inherit" component={Link} to="/inventory">
            Inventory
          </Button>
          <Button color="inherit" component={Link} to="/alerts">
            Alerts
          </Button>
          <Button color="inherit" component={Link} to="/sales-trends">
            Sales Trends
          </Button>
          <Button color="inherit" component={Link} to="/products">
            Products
          </Button>
          <Button color="inherit" component={Link} to="/locations">
            Locations
          </Button>
          <Button color="inherit" component={Link} to="/login">
            Login
          </Button>
        </Toolbar>
      </AppBar>

      <Routes>
        <Route path="/inventory" element={<Inventory />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/sales-trends" element={<SalesTrends />} />
        <Route path="/products" element={<Products />} />
        <Route path="/locations" element={<Locations />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </div>
  );
};

export default App;
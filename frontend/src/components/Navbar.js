import React from "react";
import { AppBar, Toolbar, Button } from "@mui/material";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Button color="inherit" component={Link} to="/">
          Home
        </Button>
        <Button color="inherit" component={Link} to="/inventory">
          Inventory
        </Button>
        <Button color="inherit" component={Link} to="/alerts">
          Alerts
        </Button>
        <Button color="inherit" component={Link} to="/sales-trends">
          Sales Trends
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;

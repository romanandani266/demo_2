import React, { useEffect, useState } from "react";
import { getInventory } from "../services/api";
import { Typography, CircularProgress, Table, TableBody, TableCell, TableHead, TableRow } from "@mui/material";

const Inventory = () => {
  const [inventory, setInventory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getInventory()
      .then((response) => {
        setInventory(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching inventory:", error);
        setLoading(false);
      });
  }, []);

  if (loading) return <CircularProgress />;

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Inventory
      </Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Product ID</TableCell>
            <TableCell>Location ID</TableCell>
            <TableCell>Stock Level</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {inventory.map((item, index) => (
            <TableRow key={index}>
              <TableCell>{item.product_id}</TableCell>
              <TableCell>{item.location_id}</TableCell>
              <TableCell>{item.stock_level}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default Inventory;
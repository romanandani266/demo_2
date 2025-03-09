import React, { useEffect, useState } from "react";
import { getInventory, updateInventory } from "../api";
import { Table, TableBody, TableCell, TableHead, TableRow, Button, TextField } from "@mui/material";

const Inventory = () => {
  const [inventory, setInventory] = useState([]);

  useEffect(() => {
    const fetchInventory = async () => {
      const data = await getInventory();
      setInventory(data);
    };
    fetchInventory();
  }, []);

  const handleUpdate = async (productId, locationId, stockLevel) => {
    await updateInventory({ product_id: productId, location_id: locationId, stock_level: stockLevel });
    const updatedInventory = await getInventory();
    setInventory(updatedInventory);
  };

  return (
    <div>
      <h2>Inventory</h2>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Product ID</TableCell>
            <TableCell>Location ID</TableCell>
            <TableCell>Stock Level</TableCell>
            <TableCell>Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {inventory.map((item) => (
            <TableRow key={`${item.product_id}-${item.location_id}`}>
              <TableCell>{item.product_id}</TableCell>
              <TableCell>{item.location_id}</TableCell>
              <TableCell>
                <TextField
                  type="number"
                  defaultValue={item.stock_level}
                  onBlur={(e) => handleUpdate(item.product_id, item.location_id, parseInt(e.target.value))}
                />
              </TableCell>
              <TableCell>
                <Button onClick={() => handleUpdate(item.product_id, item.location_id, item.stock_level)}>
                  Update
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default Inventory;

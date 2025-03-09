import React, { useEffect, useState } from "react";
import { getInventory } from "../api";
import { Container, Typography, List, ListItem } from "@mui/material";

const Inventory = ({ token }) => {
  const [inventory, setInventory] = useState([]);

  useEffect(() => {
    const fetchInventory = async () => {
      try {
        const data = await getInventory(token);
        setInventory(data);
      } catch (error) {
        alert(error.detail || "Failed to fetch inventory");
      }
    };
    fetchInventory();
  }, [token]);

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Inventory
      </Typography>
      <List>
        {inventory.map((item) => (
          <ListItem key={item.product_id}>
            Product ID: {item.product_id}, Location ID: {item.location_id}, Stock Level: {item.stock_level}
          </ListItem>
        ))}
      </List>
    </Container>
  );
};

export default Inventory;

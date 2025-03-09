import React, { useEffect, useState } from "react";
import { getSalesTrends } from "../api";

const SalesTrends = () => {
  const [salesTrends, setSalesTrends] = useState([]);

  useEffect(() => {
    const fetchSalesTrends = async () => {
      const data = await getSalesTrends();
      setSalesTrends(data);
    };
    fetchSalesTrends();
  }, []);

  return (
    <div>
      <h2>Sales Trends</h2>
      <ul>
        {salesTrends.map((trend, index) => (
          <li key={index}>
            Product {trend.product_id} at Location {trend.location_id}: {trend.sales_data.join(", ")}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SalesTrends;

import React, { useEffect, useState } from "react";
import { getRestockingAlerts } from "../api";

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const fetchAlerts = async () => {
      const data = await getRestockingAlerts();
      setAlerts(data);
    };
    fetchAlerts();
  }, []);

  return (
    <div>
      <h2>Restocking Alerts</h2>
      <ul>
        {alerts.map((alert, index) => (
          <li key={index}>{alert.alert_message}</li>
        ))}
      </ul>
    </div>
  );
};

export default Alerts;

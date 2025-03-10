import React, { useEffect, useState } from "react";
import { getAllBlogs } from "../api";
import BlogList from "../components/BlogList";

const Home = () => {
  const [blogs, setBlogs] = useState([]);

  useEffect(() => {
    const fetchBlogs = async () => {
      try {
        const data = await getAllBlogs();
        setBlogs(data);
      } catch (error) {
        console.error("Error fetching blogs:", error);
      }
    };

    fetchBlogs();
  }, []);

  return <BlogList blogs={blogs} />;
};

export default Home;

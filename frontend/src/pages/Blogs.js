import React, { useEffect, useState } from "react";
import { fetchBlogs } from "../api";
import BlogList from "../components/BlogList";

const Blogs = () => {
  const [blogs, setBlogs] = useState([]);

  useEffect(() => {
    const loadBlogs = async () => {
      try {
        const data = await fetchBlogs();
        setBlogs(data);
      } catch (error) {
        console.error("Error loading blogs:", error);
      }
    };
    loadBlogs();
  }, []);

  return <BlogList blogs={blogs} />;
};

export default Blogs;

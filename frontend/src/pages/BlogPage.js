import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getBlogById } from "../api";
import { Typography } from "@mui/material";

const BlogPage = () => {
  const { id } = useParams();
  const [blog, setBlog] = useState(null);

  useEffect(() => {
    const fetchBlog = async () => {
      try {
        const data = await getBlogById(id);
        setBlog(data);
      } catch (error) {
        console.error("Error fetching blog:", error);
      }
    };
    fetchBlog();
  }, [id]);

  if (!blog) return <div>Loading...</div>;

  return (
    <div>
      <Typography variant="h3">{blog.title}</Typography>
      <img src={blog.image_url} alt={blog.title} style={{ width: "100%", marginBottom: "16px" }} />
      <Typography variant="body1">{blog.content}</Typography>
    </div>
  );
};

export default BlogPage;

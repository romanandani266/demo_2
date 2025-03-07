import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchBlogById } from "../api";
import { Typography, Box } from "@mui/material";

function BlogPage() {
  const { id } = useParams();
  const [blog, setBlog] = useState(null);

  useEffect(() => {
    const loadBlog = async () => {
      try {
        const data = await fetchBlogById(id);
        setBlog(data);
      } catch (error) {
        console.error("Failed to load blog:", error);
      }
    };
    loadBlog();
  }, [id]);

  if (!blog) return <Typography>Loading...</Typography>;

  return (
    <Box>
      <Typography variant="h3">{blog.title}</Typography>
      <Typography variant="body1">{blog.content}</Typography>
      {blog.image_url && <img src={blog.image_url} alt={blog.title} style={{ width: "100%" }} />}
    </Box>
  );
}

export default BlogPage;

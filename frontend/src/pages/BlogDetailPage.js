import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Container, Typography, CircularProgress } from "@mui/material";
import { getBlogById } from "../api";

const BlogDetailPage = () => {
  const { id } = useParams();
  const [blog, setBlog] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBlog = async () => {
      try {
        const data = await getBlogById(id);
        setBlog(data);
      } catch (error) {
        console.error("Error fetching blog:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchBlog();
  }, [id]);

  if (loading) {
    return <CircularProgress />;
  }

  if (!blog) {
    return <Typography variant="h6">Blog not found</Typography>;
  }

  return (
    <Container>
      <Typography variant="h3" gutterBottom>
        {blog.title}
      </Typography>
      <img src={blog.image_url} alt={blog.title} style={{ width: "100%", marginBottom: "20px" }} />
      <Typography variant="body1">{blog.content}</Typography>
      <Typography variant="caption" display="block" gutterBottom>
        Created at: {new Date(blog.created_at).toLocaleString()}
      </Typography>
    </Container>
  );
};

export default BlogDetailPage;

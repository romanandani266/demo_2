import React, { useEffect, useState } from "react";
import { getBlogs } from "../api";
import { Link } from "react-router-dom";
import { Card, CardContent, Typography, Grid } from "@mui/material";

const BlogList = () => {
  const [blogs, setBlogs] = useState([]);

  useEffect(() => {
    const fetchBlogs = async () => {
      try {
        const data = await getBlogs();
        setBlogs(data);
      } catch (error) {
        console.error("Error fetching blogs:", error);
      }
    };
    fetchBlogs();
  }, []);

  return (
    <Grid container spacing={2}>
      {blogs.map((blog) => (
        <Grid item xs={12} key={blog.id}>
          <Card>
            <CardContent>
              <Typography variant="h5">{blog.title}</Typography>
              <Typography variant="body2">{blog.content.slice(0, 100)}...</Typography>
              <Link to={`/blogs/${blog.id}`}>Read More</Link>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};

export default BlogList;

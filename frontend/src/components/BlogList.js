import React, { useEffect, useState } from "react";
import { fetchBlogs } from "../api";
import { Card, CardContent, Typography, Button } from "@mui/material";
import { Link } from "react-router-dom";

const BlogList = () => {
  const [blogs, setBlogs] = useState([]);

  useEffect(() => {
    fetchBlogs()
      .then((response) => setBlogs(response.data))
      .catch((error) => console.error("Error fetching blogs:", error));
  }, []);

  return (
    <div>
      {blogs.map((blog) => (
        <Card key={blog.id} sx={{ marginBottom: 2 }}>
          <CardContent>
            <Typography variant="h5">{blog.title}</Typography>
            <Typography variant="body2">{blog.content.slice(0, 100)}...</Typography>
            <Button component={Link} to={`/blogs/${blog.id}`}>
              Read More
            </Button>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default BlogList;

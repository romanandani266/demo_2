import React from "react";
import { Link } from "react-router-dom";
import { Card, CardContent, Typography, Button } from "@mui/material";

const BlogList = ({ blogs }) => {
  return (
    <div>
      {blogs.map((blog) => (
        <Card key={blog.id} style={{ marginBottom: "1rem" }}>
          <CardContent>
            <Typography variant="h5">{blog.title}</Typography>
            <Typography variant="body2">{blog.content}</Typography>
            <Button component={Link} to={`/blogs/${blog.id}`} color="primary">
              View Details
            </Button>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default BlogList;

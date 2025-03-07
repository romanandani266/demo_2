import React from "react";
import { Link } from "react-router-dom";
import { Card, CardContent, Typography } from "@mui/material";

const BlogList = ({ blogs }) => {
  return (
    <div>
      {blogs.map((blog) => (
        <Card key={blog.id} style={{ marginBottom: "16px" }}>
          <CardContent>
            <Typography variant="h5">{blog.title}</Typography>
            <Typography variant="body2">{blog.content.substring(0, 100)}...</Typography>
            <Link to={`/blogs/${blog.id}`}>Read More</Link>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default BlogList;

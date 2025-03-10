import React from "react";
import { Link } from "react-router-dom";
import { Card, CardContent, Typography } from "@mui/material";

const BlogList = ({ blogs }) => {
  return (
    <div>
      {blogs.map((blog) => (
        <Card key={blog.id} sx={{ marginBottom: 2 }}>
          <CardContent>
            <Typography variant="h5" component={Link} to={`/blogs/${blog.id}`}>
              {blog.title}
            </Typography>
            <Typography variant="body2">{blog.content.substring(0, 100)}...</Typography>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default BlogList;

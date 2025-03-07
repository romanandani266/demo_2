import React from "react";
import { Link } from "react-router-dom";
import { Card, CardContent, Typography, CardMedia } from "@mui/material";

const BlogList = ({ blogs }) => {
  return (
    <div>
      {blogs.map((blog) => (
        <Card key={blog.id} sx={{ marginBottom: 2 }}>
          {blog.image_url && (
            <CardMedia
              component="img"
              height="140"
              image={blog.image_url}
              alt={blog.title}
            />
          )}
          <CardContent>
            <Typography variant="h5">{blog.title}</Typography>
            <Typography variant="body2">{blog.content_snippet}</Typography>
            <Link to={`/blogs/${blog.id}`}>Read More</Link>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default BlogList;

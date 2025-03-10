import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getBlogById } from '../api';
import { Container, Typography } from '@mui/material';

const BlogDetailPage = () => {
  const { id } = useParams();
  const [blog, setBlog] = useState(null);

  useEffect(() => {
    const fetchBlog = async () => {
      try {
        const data = await getBlogById(id);
        setBlog(data);
      } catch (error) {
        console.error('Error fetching blog:', error);
      }
    };
    fetchBlog();
  }, [id]);

  if (!blog) return <Typography>Loading...</Typography>;

  return (
    <Container>
      <Typography variant="h3" style={{ color: 'blue', textShadow: '1px 1px 2px gray' }}>
        {blog.title}
      </Typography>
      <Typography variant="body1" style={{ margin: '20px 0' }}>
        {blog.content}
      </Typography>
      <img src={blog.image_url} alt={blog.title} style={{ width: '100%' }} />
      <Typography variant="caption">Created at: {new Date(blog.created_at).toLocaleString()}</Typography>
    </Container>
  );
};

export default BlogDetailPage;

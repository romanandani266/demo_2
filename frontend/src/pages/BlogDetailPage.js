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

  if (!blog) return <div>Loading...</div>;

  return (
    <Container>
      <Typography variant="h3" gutterBottom>
        {blog.title}
      </Typography>
      <img src={blog.image_url} alt={blog.title} style={{ width: '100%' }} />
      <Typography variant="body1" style={{ marginTop: '20px' }}>
        {blog.content}
      </Typography>
      <Typography variant="caption" display="block" style={{ marginTop: '10px' }}>
        Created at: {new Date(blog.created_at).toLocaleString()}
      </Typography>
    </Container>
  );
};

export default BlogDetailPage;
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { createBlog, updateBlog, getBlogById } from '../api';
import { TextField, Button, Container } from '@mui/material';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';

const CreateEditPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [imageUrl, setImageUrl] = useState('');

  useEffect(() => {
    if (id) {
      const fetchBlog = async () => {
        try {
          const blog = await getBlogById(id);
          setTitle(blog.title);
          setContent(blog.content);
          setImageUrl(blog.image_url);
        } catch (error) {
          console.error('Error fetching blog:', error);
        }
      };
      fetchBlog();
    }
  }, [id]);

  const handleSubmit = async () => {
    try {
      const blog = { title, content, image_url: imageUrl };
      if (id) {
        await updateBlog(id, blog);
      } else {
        await createBlog(blog);
      }
      navigate('/');
    } catch (error) {
      console.error('Error saving blog:', error);
    }
  };

  return (
    <Container>
      <TextField
        label="Title"
        fullWidth
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        margin="normal"
      />
      <ReactQuill value={content} onChange={setContent} />
      <TextField
        label="Image URL"
        fullWidth
        value={imageUrl}
        onChange={(e) => setImageUrl(e.target.value)}
        margin="normal"
      />
      <Button variant="contained" color="primary" onClick={handleSubmit}>
        Save
      </Button>
    </Container>
  );
};

export default CreateEditPage;
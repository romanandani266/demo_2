import React, { useState } from "react";
import { createBlog, uploadImage } from "../api";
import { TextField, Button } from "@mui/material";

const CreateBlog = () => {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [image, setImage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      let imageUrl = null;
      if (image) {
        const response = await uploadImage(image);
        imageUrl = response.data.image_url;
      }
      await createBlog({ title, content, image_url: imageUrl });
      alert("Blog created successfully!");
    } catch (error) {
      console.error("Error creating blog:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <TextField
        label="Title"
        fullWidth
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />
      <TextField
        label="Content"
        fullWidth
        multiline
        rows={4}
        value={content}
        onChange={(e) => setContent(e.target.value)}
        required
      />
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setImage(e.target.files[0])}
      />
      <Button type="submit" variant="contained" color="primary">
        Create Blog
      </Button>
    </form>
  );
};

export default CreateBlog;

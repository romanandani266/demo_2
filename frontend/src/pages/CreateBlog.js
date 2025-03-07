import React, { useState } from "react";
import { createBlog } from "../api";
import BlogForm from "../components/BlogForm";

const CreateBlog = () => {
  const [error, setError] = useState(null);

  const handleSubmit = async (blogData) => {
    try {
      await createBlog(blogData);
      alert("Blog created successfully!");
    } catch (err) {
      setError("Error creating blog");
    }
  };

  return (
    <div>
      <h1>Create Blog</h1>
      {error && <p>{error}</p>}
      <BlogForm onSubmit={handleSubmit} />
    </div>
  );
};

export default CreateBlog;

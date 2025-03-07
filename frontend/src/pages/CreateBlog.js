import React, { useState } from "react";
import { createBlog } from "../api";
import BlogForm from "../components/BlogForm";

const CreateBlog = () => {
  const [error, setError] = useState(null);

  const handleSubmit = async (blog) => {
    try {
      await createBlog(blog);
      alert("Blog created successfully!");
    } catch (err) {
      setError("Error creating blog");
    }
  };

  return (
    <div>
      <h2>Create Blog</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <BlogForm onSubmit={handleSubmit} />
    </div>
  );
};

export default CreateBlog;

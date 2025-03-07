import React from "react";
import BlogForm from "../components/BlogForm";
import { createBlog } from "../api";

function CreateBlogPage() {
  const handleSubmit = async (formData) => {
    try {
      await createBlog(formData);
      alert("Blog created successfully!");
    } catch (error) {
      console.error("Failed to create blog:", error);
    }
  };

  return <BlogForm onSubmit={handleSubmit} />;
}

export default CreateBlogPage;

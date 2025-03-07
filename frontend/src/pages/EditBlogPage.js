import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import BlogForm from "../components/BlogForm";
import { fetchBlogById, updateBlog } from "../api";

function EditBlogPage() {
  const { id } = useParams();
  const [blog, setBlog] = useState(null);

  useEffect(() => {
    const loadBlog = async () => {
      try {
        const data = await fetchBlogById(id);
        setBlog(data);
      } catch (error) {
        console.error("Failed to load blog:", error);
      }
    };
    loadBlog();
  }, [id]);

  const handleSubmit = async (formData) => {
    try {
      await updateBlog(id, formData);
      alert("Blog updated successfully!");
    } catch (error) {
      console.error("Failed to update blog:", error);
    }
  };

  if (!blog) return <div>Loading...</div>;

  return <BlogForm initialData={blog} onSubmit={handleSubmit} />;
}

export default EditBlogPage;

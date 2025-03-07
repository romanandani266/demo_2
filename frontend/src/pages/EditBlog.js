import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchBlogById, updateBlog } from "../api";
import BlogForm from "../components/BlogForm";

const EditBlog = () => {
  const { id } = useParams();
  const [blog, setBlog] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadBlog = async () => {
      try {
        const data = await fetchBlogById(id);
        setBlog(data);
      } catch (err) {
        setError("Error loading blog");
      }
    };
    loadBlog();
  }, [id]);

  const handleSubmit = async (blogData) => {
    try {
      await updateBlog(id, blogData);
      alert("Blog updated successfully!");
    } catch (err) {
      setError("Error updating blog");
    }
  };

  if (!blog) return <div>Loading...</div>;

  return (
    <div>
      <h1>Edit Blog</h1>
      {error && <p>{error}</p>}
      <BlogForm onSubmit={handleSubmit} initialData={blog} />
    </div>
  );
};

export default EditBlog;

import axios from "axios";

const API_BASE_URL = "http://localhost:8080";

export const api = axios.create({
  baseURL: API_BASE_URL,
});

export const fetchBlogs = (page = 1, limit = 10) =>
  api.get(`/blogs?page=${page}&limit=${limit}`);

export const fetchBlogById = (id) => api.get(`/blogs/${id}`);

export const createBlog = (data) => api.post("/blogs", data);

export const updateBlog = (id, data) => api.put(`/blogs/${id}`, data);

export const deleteBlog = (id) => api.delete(`/blogs/${id}`);

export const uploadImage = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/blogs/upload-image", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

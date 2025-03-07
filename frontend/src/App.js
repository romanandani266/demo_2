import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import BlogList from "./components/BlogList";
import BlogDetail from "./components/BlogDetail";
import BlogForm from "./components/BlogForm";

const App = () => {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<BlogList />} />
        <Route path="/blogs/:id" element={<BlogDetail />} />
        <Route path="/create" element={<BlogForm />} />
      </Routes>
    </>
  );
};

export default App;

import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import CreateEditBlog from './pages/CreateEditBlog';
import BlogDetailPage from './pages/BlogDetailPage';
import Navbar from './components/Navbar';
import { ThemeProvider } from '@mui/material/styles';
import theme from './theme';

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/create" element={<CreateEditBlog />} />
        <Route path="/edit/:id" element={<CreateEditBlog />} />
        <Route path="/blogs/:id" element={<BlogDetailPage />} />
      </Routes>
    </ThemeProvider>
  );
};

export default App;
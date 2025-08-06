import  { useState, useEffect } from "react";
import axios from "axios";

const API_BASE = "http://localhost:8000"; // Adjust according to your backend URL

export default function App() {
  const [users, setUsers] = useState([]);
  const [blogs, setBlogs] = useState([]);
  const [newUser, setNewUser] = useState({ username: "", email: "", password: "" });
  const [newBlog, setNewBlog] = useState({ title: "", content: "", author: "", published: true, tags: "" });

  // Fetch users
  useEffect(() => {
    axios.get(`${API_BASE}/users`).then((res) => setUsers(res.data.data));
   
  }, []);

  // Fetch blogs
  useEffect(() => {
    axios.get(`${API_BASE}/blogs`).then((res) => setBlogs(res.data.data));
  }, []);
  

  const handleUserCreate = async () => {
    await axios.post(`${API_BASE}/users`, newUser);
    const res = await axios.get(`${API_BASE}/users`);
    setUsers(res.data.data);
    setNewUser({ username: "", email: "", password: "" });
  };

  const handleBlogCreate = async () => {
    const blogPayload = {
      ...newBlog,
      tags: newBlog.tags.split(",").map((tag) => tag.trim()),
    };
    await axios.post(`${API_BASE}/blogs`, blogPayload);
    const res = await axios.get(`${API_BASE}/blogs`);
    setBlogs(res.data.data);
    setNewBlog({ title: "", content: "", author: "", published: true, tags: "" });
  };

  return (
    <div className="p-6 font-sans">
      <h1 className="text-2xl font-bold mb-4">Users</h1>

      <input
        className="border p-2 mr-2"
        placeholder="Username"
        value={newUser.username}
        onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
      />
      <input
        className="border p-2 mr-2"
        placeholder="Email"
        value={newUser.email}
        onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
      />
      <input
        className="border p-2 mr-2"
        placeholder="Password"
        type="password"
        value={newUser.password}
        onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
      />
      <button onClick={handleUserCreate} className="bg-blue-500 text-white px-4 py-2 rounded">Create User</button>

      <ul className="mt-4">
        {users.map((u) => (
          <li key={u.id} className="border p-2 mb-2 rounded">
            <strong>{u.username}</strong> - {u.email}
          </li>
        ))}
      </ul>

      <h1 className="text-2xl font-bold mt-8 mb-4">Blogs</h1>

      <input
        className="border p-2 mr-2"
        placeholder="Title"
        value={newBlog.title}
        onChange={(e) => setNewBlog({ ...newBlog, title: e.target.value })}
      />
      <input
        className="border p-2 mr-2"
        placeholder="Content"
        value={newBlog.content}
        onChange={(e) => setNewBlog({ ...newBlog, content: e.target.value })}
      />
      <input
        className="border p-2 mr-2"
        placeholder="Author"
        value={newBlog.author}
        onChange={(e) => setNewBlog({ ...newBlog, author: e.target.value })}
      />
      <input
        className="border p-2 mr-2"
        placeholder="Tags (comma-separated)"
        value={newBlog.tags}
        onChange={(e) => setNewBlog({ ...newBlog, tags: e.target.value })}
      />
      <button onClick={handleBlogCreate} className="bg-green-500 text-white px-4 py-2 rounded">Create Blog</button>

      <ul className="mt-4">
        {blogs.map((b) => (
          <li key={b.id} className="border p-2 mb-2 rounded">
            <strong>{b.title}</strong> by {b.author} ({b.published ? "Published" : "Unpublished"})<br />
            {b.content}<br />
            Tags: {b.tags?.join(", ")}
          </li>
        ))}
      </ul>
    </div>
  );
}

const API_URL = "http://127.0.0.1:5000"; // Backend API URL

// Login User
async function loginUser(userId, password) {
  try {
    const response = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: userId, password }),
    });

    if (response.ok) {
      alert("Login successful!");
      localStorage.setItem("userId", userId);
      localStorage.setItem("password", password);
      fetchTasks(userId, password); // Load tasks
    } else {
      alert("Invalid credentials. Try again.");
    }
  } catch (error) {
    console.error("Error logging in:", error);
  }
}

// Fetch Tasks
async function fetchTasks(userId, password) {
  try {
    const response = await fetch(`${API_URL}/tasks`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Basic ${btoa(`${userId}:${password}`)}`, // Use Basic Auth
      },
    });

    if (response.ok) {
      const tasks = await response.json();
      displayTasks(tasks);
    } else {
      alert("Failed to load tasks.");
    }
  } catch (error) {
    console.error("Error fetching tasks:", error);
  }
}

// Add Task
document.getElementById("taskForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = document.getElementById("title").value;
  const description = document.getElementById("description").value;
  const dueDate = document.getElementById("dueDate").value;
  const priority = document.getElementById("priority").value;

  const userId = localStorage.getItem("userId");
  const password = localStorage.getItem("password");

  if (!userId || !password) {
    alert("Please log in first.");
    return;
  }

  try {
    const response = await fetch(`${API_URL}/tasks`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Basic ${btoa(`${userId}:${password}`)}`,
      },
      body: JSON.stringify({ title, description, due_date: dueDate, priority }),
    });

    if (response.ok) {
      fetchTasks(userId, password); // Reload tasks
      document.getElementById("taskForm").reset();
      alert("Task added successfully!");
    } else {
      alert("Failed to add task.");
    }
  } catch (error) {
    console.error("Error adding task:", error);
  }
});

// Delete Task
async function deleteTask(taskId) {
  const userId = localStorage.getItem("userId");
  const password = localStorage.getItem("password");

  if (!userId || !password) {
    alert("Please log in first.");
    return;
  }

  try {
    const response = await fetch(`${API_URL}/tasks/${taskId}`, {
      method: "DELETE",
      headers: {
        Authorization: `Basic ${btoa(`${userId}:${password}`)}`,
      },
    });

    if (response.ok) {
      fetchTasks(userId, password); // Reload tasks
      alert("Task deleted successfully!");
    } else {
      alert("Failed to delete task.");
    }
  } catch (error) {
    console.error("Error deleting task:", error);
  }
}

// Display Tasks
function displayTasks(tasks) {
  const taskList = document.getElementById("taskList");
  taskList.innerHTML = "";

  tasks.forEach((task) => {
    const li = document.createElement("li");
    li.textContent = `${task.title} (${task.priority}) - Due: ${task.due_date}`;

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";
    deleteBtn.onclick = () => deleteTask(task.id);

    li.appendChild(deleteBtn);
    taskList.appendChild(li);
  });
}

// Login Form Handler
document.getElementById("loginForm").addEventListener("submit", (e) => {
  e.preventDefault();
  const userId = document.getElementById("userId").value;
  const password = document.getElementById("password").value;
  loginUser(userId, password);
});

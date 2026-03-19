import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTrash } from '@fortawesome/free-solid-svg-icons';

// Use runtime API origin from window object; default to same-origin behind the ingress.
const API_URL = window.VITE_API_URL || '';

function App() {
  const [count, setCount] = useState(0)
  const [tasks, setTasks] = useState([]);
  const [taskInput, setTaskInput] = useState('');

  const fetchAPI = async () => {
    const response = await axios.get(`${API_URL}/api/tasks`);
    console.log(response.data);
    setTasks(response.data);
  };

  const handleTaskChange = (e) => {
  setTaskInput(e.target.value);
  e.target.style.height = 'auto';
  e.target.style.height = e.target.scrollHeight + 'px';
  };

  const handleAddTask = async () => {
    if (taskInput.trim() === '') return;
    
    try {
      await axios.post(`${API_URL}/api/tasks`, 
        { task: taskInput },
        { headers: { 'Content-Type': 'application/json' } }
      );
      setTaskInput(''); // Clear input
      fetchAPI(); // Refresh tasks list
    } catch (error) {
      console.error('Error adding task:', error);
    }
};

  useEffect(() => {
    fetchAPI();
  }, []);

  return (
    <>
      <section id="center">
        <div className="hero">
          <img src={heroImg} className="base" width="170" height="179" alt="" />
          <img src={reactLogo} className="framework" alt="React logo" />
          <img src={viteLogo} className="vite" alt="Vite logo" />
        </div>
        <div>
          <h1>My tasks</h1>
        </div>
        <label for="task">New Task:</label>
        <textarea 
          id="task" 
          name="task"
          value={taskInput}
          onChange={(e) => setTaskInput(e.target.value)}
          style={{ resize: 'none', overflow: 'hidden', minHeight: '80px' }}> </textarea>
        <button
          className="counter"
          onClick={handleAddTask}
        >
          Add new task
        </button>
        <p>
            {tasks.map((task) => (
              <>
                <div key={task.id}>
                  <span>{task.task}</span>
                  <button 
                    onClick={() => {
                      axios.delete(`${API_URL}/api/tasks/${task.id}`)
                        .then(() => fetchAPI())
                        .catch((error) => console.error('Error deleting task:', error));
                    }}
                    style={{ backgroundColor: '#ff4444', color: 'white', border: 'none', cursor: 'pointer', padding: '8px 12px', borderRadius: '4px', fontSize: '16px', marginLeft: '16px' }}
                  ><FontAwesomeIcon icon={faTrash} /></button>
                  <br>
                  </br>
                </div>
              </>
            ))
            }
        </p>
      </section>

      <div className="ticks"></div>

      <div className="ticks"></div>
      <section id="spacer"></section>
    </>
  )
}

export default App

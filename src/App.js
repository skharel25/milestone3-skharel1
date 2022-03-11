import './App.css';
import { useState } from 'react'

function App() {
  const [fact, setFact] = useState("");
  function handleClick() {
    fetch('/returncomments', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    }).then((response) => response.json())
      .then((data) => {
        setFact(data.comment);
      });
  }
  return (
    <div className="App">
      <button onClick={handleClick}>Delete</button>
      <button onClick={handleClick}>Save Changes</button>
      <br></br>
      {fact}
    </div>
  );
}

export default App;

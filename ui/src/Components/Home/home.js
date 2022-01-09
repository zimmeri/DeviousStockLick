import React from 'react';

const Home = () => {

  const generatePost = () => {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'n': 2})
    };
    fetch('/api/generate', requestOptions)
      .then(response => response.json())
      .then(data => {
        console.log(data)
        fetch('/api/generate')
            .then(response => response.json())
            .then(data => console.log(data));
      });
  }

  const generateScore = () => {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'n': 10})
    };
    fetch('/api/score', requestOptions)
      .then(response => response.json())
      .then(data => {console.log(data)})
  }

  return(
    <div>
      <button type="button" onClick={() => generatePost()}>Generate Post</button>
      <button type="button" onClick={() => generateScore()}>Generate Score</button>
    </div>
  )
}

export default Home;

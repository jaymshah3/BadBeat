import React, { Component } from 'react';
import './App.css';
import { Button, TextField } from '@material-ui/core';
import io from 'socket.io-client';

class App extends Component {
  constructor() {
    super();
    this.state = {
      socket: null,
      endpoint: 'http://localhost:5000',
      username: '',
      isInGame: false,
      joinRequests: [{name:"aditya", bank: 5000}]
    };
  }

  componentDidMount() {
    const { endpoint } = this.state;
    console.log(endpoint);
    const socket = io(endpoint);
    this.setState({socket: socket})
  }

  render() {
    const { username, isInGame, joinRequests } = this.state;
    const isDisabled = username == "" || username == undefined;

    const outOfGame = (
      <form onSubmit={() => this.joinGame()}>
        <TextField value={this.state.username} onChange={this.handleUsernameChange} id="outlined-basic" label="Username" variant="outlined" />
        <Button variant="contained" type="submit" disabled={isDisabled}>Join Game</Button>
      </form>
    );

    const inGame = (
      <ul>
          {
            joinRequests.map((element) => {
              return <li key={element.name}>
                <div>
                  <p>{element['name']}</p>
                  <p>{element['bank']}</p>
                  <Button variant="contained" color="primary" onClick={() => {this.handleRequest(element, true)}}>Approve</Button>
                  <Button variant="contained" color="secondary" onClick={() => this.handleRequest(element, false)}>Reject</Button>
                </div>
              </li>
            })
          }
        </ul>
    );

    const show = isInGame ? inGame : outOfGame;

    return (
      <div className="App">
        {show}
      </div>
    );
  }

  handleUsernameChange = (e) => {
    this.setState({
      username: e.target.value
    });
  }

  handleRequest = (element, decision) => {
    const { socket } = this.state;

    if (decision) {
      console.log("approve");
    } else {
      console.log("reject");
    }
  }

  joinGame() {
    const { socket } = this.state;

    this.setState({isInGame: true});
    socket.emit('request to join', {
      username: 'jawn',
      room: 1,
    })
    socket.on('join request', (data) => {
      this.setState((state) => {
        const joinRequests = state.joinRequests.concat(data)
        return {
          joinRequests
        }
      })
    })
  }
}

export default App;

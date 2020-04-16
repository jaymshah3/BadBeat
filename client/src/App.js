import React, { Component } from 'react';
import './App.css';
import { Button, TextField } from '@material-ui/core';
import io from 'socket.io-client';
import PreGameDashboard from './PreGameDashboard.js';

class App extends Component {
  constructor() {
    super();
    this.state = {
      socket: null,
      endpoint: 'http://localhost:5000',
      username: '',
      isInPreGame: false,
      requested: false,
      owner: false
    };
  }

  componentDidMount() {
    const { endpoint } = this.state;
    const socket = io(endpoint);
    console.log(socket);
    this.setState({socket: socket})

    this.defineHandlers(socket);
  }

  defineHandlers(socket) {
    socket.on('reject request', () => {
      this.setState({requested: false});
    });

    socket.on('approve request', () => {
      this.setState({requested: false, isInPreGame: true});
    });

    socket.on('owner', () => {
      console.log('got owner')
      this.setState({requested: false, isInPreGame: true, owner: true});
    });
  }

  render() {
    const { username, isInPreGame, socket, owner } = this.state;
    const isDisabled = username == "" || username == undefined;
    console.log('isInPreGame is ' + isInPreGame)

    const outOfGame = (
      <div>
        <TextField value={this.state.username} onChange={this.handleUsernameChange} id="outlined-basic" label="Username" variant="outlined" />
        <Button variant="contained" type="submit" disabled={isDisabled} onClick={() => this.joinGame()}>Join Game</Button>
      </div>
    );

    const inPreGame = <PreGameDashboard socket={socket} owner={owner}/>;

    const show = isInPreGame ? inPreGame : outOfGame;

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

  joinGame() {
    const { socket, username } = this.state;

    this.setState({requested: true});
    socket.emit('request to join', {
      username: username,
      room: 1,
      bank: 1000
    })
  }
}

export default App;

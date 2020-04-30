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
      bank: '',
      isInPreGame: false,
      requested: false,
      isOwner: false,
      room: 0,
      inputRoom: '',
      usernameError: false
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
    socket.on('request response', (data) => {
      if (data['approve']) {
        this.setState({requested: false, isInPreGame: true, usernameError: false, room: data['room']});
      } else {
        this.setState({requested: false});
      }
    });

    socket.on('owner', (data) => {
      console.log('got owner')
      this.setState({requested: false, isInPreGame: true, isOwner: true, usernameError: false, room: data['room']});
    });

    socket.on('duplicate username', () => {
      this.setState({requested: false, usernameError: true})
    });
  }

  render() {
    const { 
      username, 
      usernameError, 
      isInPreGame, 
      socket, 
      isOwner, 
      room, 
      requested,
      bank,
      inputRoom
    } = this.state;

    const isDisabled = username == "" || username == undefined;

    const outOfGame = (
      <div>
        <TextField 
          value={this.state.username} 
          onChange={this.handleUsernameChange} 
          id="outlined-basic" 
          label="Username" 
          variant="outlined" 
          error={usernameError}
          helperText={usernameError ? "Username already exists." : ""}
        />
        <TextField 
          value={bank} 
          onChange={this.handleBankChange} 
          id="outlined-basic" 
          label="Bank" 
          variant="outlined" 
          // error={}
          // helperText={usernameError ? "Username already exists." : ""}
        />
        <TextField 
          value={inputRoom} 
          onChange={this.handleInputRoomChange} 
          id="outlined-basic" 
          label="Room" 
          variant="outlined" 
          // error={}
          // helperText={usernameError ? "Username already exists." : ""}
        />
        <Button variant="contained" type="submit" disabled={isDisabled || this.isInvalidNum(bank)} onClick={() => this.createGame()}>Create Game</Button>
        <Button variant="contained" type="submit" disabled={isDisabled || this.isInvalidNum(bank) || this.isInvalidNum(inputRoom)} onClick={() => this.joinGame()}>Join Game</Button>
      </div>
    );

    const requestedView = <h1>Requested...</h1>

    const inPreGame = <PreGameDashboard 
                        socket={socket} 
                        isOwner={isOwner} 
                        room={room} 
                        username={username}
                        bank={parseInt(bank)}
                      />;

    let show;
    if (requested) {
      show = requestedView;
    } else if (isInPreGame) {
      show = inPreGame;
    } else {
      show = outOfGame;
    }

    return (
      <div className="App">
        {show}
      </div>
    );
  }

  isInvalidNum(data) {
    return isNaN(data) || data == '';
  }

  handleUsernameChange = (e) => {
    this.setState({
      username: e.target.value
    });
  }

  handleBankChange = (e) => {
    this.setState({
      bank: e.target.value
    });
  }

  handleInputRoomChange = (e) => {
    this.setState({
      inputRoom: e.target.value
    });
  }

  createGame() {
    const { socket, username, bank } = this.state;

    this.setState({requested: true});
    socket.emit('create room', {
      username: username,
      bank: parseInt(bank),
      small_blind: 5,
      big_blind: 10
    });
  }

  joinGame() {
    const { socket, username, bank, inputRoom } = this.state;

    this.setState({requested: true});
    socket.emit('request to join', {
      username: username,
      room: inputRoom,
      bank: parseInt(bank)
    });
  }
}

export default App;

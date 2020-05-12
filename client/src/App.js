import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from 'react-router-dom';
import { connect } from 'react-redux';
import './App.css';
import Home from './Home';
import PreGameDashboard from './PreGameDashboard';
import { Button, TextField } from '@material-ui/core';
import io from 'socket.io-client';
import { setSocket } from './js/actions/index';
import { setOwner } from './js/actions/home';
import {
  addJoinRequest,
  addJoinedPlayer, 
  setJoinedPlayers, 
  setGameStart,
  removeJoinRequest,
  requestResponse 
} from './js/actions/pregame';
import { ENDPOINT } from './js/constants/socket-info';

function mapDispatchToProps(dispatch) {
  return {
    setSocket: socket => dispatch(setSocket(socket)),
    setOwner: owner => dispatch(setOwner(owner)),
    addJoinedPlayer: player => dispatch(addJoinedPlayer(player)),
    addJoinRequest: request => dispatch(addJoinRequest(request)),
    setJoinedPlayers: players => dispatch(setJoinedPlayers(players)),
    setGameStart: start => dispatch(setGameStart(start)),
    removeJoinRequest: request => dispatch(removeJoinRequest(request))
  };
}

class ConnectedApp extends Component {
  constructor(props) {
    super(props);
    this.state = {
      socket: null
    }

    console.log(JSON.stringify(props));
  }

  componentDidMount() {
    const socket = io(ENDPOINT);
    this.props.setSocket(socket);
    this.setState({
      socket: socket
    })
    this.defineHandlers(socket);
  }

  defineHandlers(socket) {
    socket.on('owner',(data) => {
      this.props.setOwner(data.room)
    });
    socket.on('join request', (data) => {
			this.props.addJoinRequest(data);
		});
		socket.on('user joined', (data) => {
      this.props.addJoinedPlayer(data);
      this.props.removeJoinRequest(data);
		});
		socket.on('user list', (data) => {
			this.props.setJoinedPlayers(data);
		});
		socket.on('game start', () => {
			this.props.setGameStart(true)
		});
  }

  render() {
    const { socket } = this.state;

    if (!socket) {
      return <h3>Connecting...</h3>
    }

    return (
      <Router>
        <Switch>
          <Route 
            path="/:id" 
            render={(props) => <PreGameDashboard {...props} />}>
          </Route>
          <Route path="/">
            <Home />
          </Route>
        </Switch>
      </Router>
    )
  }
}

const App = connect(null, mapDispatchToProps)(ConnectedApp);

export default App;

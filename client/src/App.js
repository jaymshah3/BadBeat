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
import io from 'socket.io-client';
import { setSocket } from './js/actions/index';

function mapDispatchToProps(dispatch) {
  return {
    setSocket: socket => dispatch(setSocket(socket))
  };
}

class ConnectedApp extends Component {
  constructor(props) {
    super(props);
    this.state = {
      socket: null
    }
  }

  componentDidMount() {
    const socket = io({transports: ['websocket']});
    this.props.setSocket(socket);
    this.setState({
      socket: socket
    })
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

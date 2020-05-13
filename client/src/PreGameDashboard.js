import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Button, List, ListItem, ListItemText, Divider } from '@material-ui/core';
import JoinDialog from './JoinDialog';
import InGameDashboard from './InGameDashboard';

const mapStateToProps = state => {
    return {
        socket: state.socket,
    };
}

class ConnectedPreGameDashboard extends Component {
    constructor(props) {
        super(props);

		let isOwner = false;
		let isJoined = false;
		let username = "";
		let bank = 0;

        if (this.props.location && this.props.location.state && this.props.location.state.isOwner) {
			isOwner = true;
			isJoined = true;
			username = this.props.location.state.username;
			bank = this.props.location.state.bank;
        }

        this.state = {
			isOwner: isOwner,
			isJoined: isJoined,
			isRequested: false,
			showJoinDialog: false,
			initialLoad: false,
			joinedPlayers: [],
			joinRequests: [],
			startGame: false,
			username: username,
			bank: bank
		};
	}

	componentDidMount() {
		this.defineHandlers()
		this.loadUsers();
	}

	defineHandlers() {
		const { socket } = this.props;
		socket.on('join request', (data) => {
			this.setState((state) => {
				const joinRequests = state.joinRequests.concat(data)
				return {
					joinRequests
				}
			});
		});
		socket.on('user joined', (data) => {
			this.setState((state) => {
				const joinedPlayers = state.joinedPlayers.concat(data);
				const joinRequests = state.joinRequests.filter(x => x['username'] != data['username'])
				return {
					joinedPlayers,
					joinRequests
				}
			});
		});
		socket.on('user list', (data) => {
			this.setState({joinedPlayers: data["players"]});
		});
		socket.on('game start', () => {
			this.setState({startGame: true});
		});
	}
	
	loadUsers() {
		const { socket } = this.props;
		const { id } = this.props.match.params;

		socket.emit('list users', {room: id});
	}

    showStartButton() {
        const { isOwner, joinedPlayers } = this.state;

		if (isOwner && joinedPlayers.length >= 2) {
			return <Button variant="contained" onClick={() => this.startGame()}>Start Game</Button>;
		} else {
			return null;
		}
	}

	showJoinedPlayers() {
		const { joinedPlayers } = this.state;

		return <List>
			{
				joinedPlayers.map((element) => {
					return <ListItem key={element['username']}>
						<div>
							<ListItemText>{element['username']}</ListItemText>
							<ListItemText>{element['bank']}</ListItemText>
						</div>
					</ListItem>
				})
			}
		</List>
	}

	showRequests() {
        const { isOwner, joinRequests } = this.state;


		if (isOwner) {
			return <List>
				{
					joinRequests.map((element) => {
						return <ListItem key={element['username']}>
							<div>
								<ListItemText>{element['username']}</ListItemText>
								<ListItemText>{element['bank']}</ListItemText>
								<Button variant="contained" color="primary" onClick={() => {this.handleRequest(element, true)}}>Approve</Button>
								<Button variant="contained" color="secondary" onClick={() =>{this.handleRequest(element, false)}}>Reject</Button>
							</div>
						</ListItem>
					})
				}
     		</List>
		} else {
			return null;
		}
	}

	handleRequest = (element, decision) => {
		const { socket } = this.props;
		const { id } = this.props.match.params;
		const data = {
			username: element['username'],
			bank: element['bank'],
			request_sid: element['request_sid'],
			approve: decision,
			room: id
		}
		socket.emit('handle join request', data);
	}

	showJoinButton() {
		const { isJoined, isRequested } = this.state;

		if (!isJoined && !isRequested) {
			return <Button variant="contained" onClick={() => this.joinGame()}>Join Game</Button>;
		} else if (!isJoined && isRequested) {
			return <Button variant="contained" onClick={() => this.joinGame()} disabled={true}>Requested...</Button>;
		}
		return null;
	}

	joinGame() {
		this.setState({showJoinDialog: true})
	}

	handleClose = (value, newUsername, newBank) => {
		let update = {
			showJoinDialog: false, 
			isJoined: value
		}
		if (value) {
			update['username'] = newUsername
			update['bank'] = newBank
		}
		console.log(this.state)
		console.log(update)
        this.setState(update);
    }

	startGame() {
		const { socket } = this.props;
		const { id } = this.props.match.params;

		socket.emit('start', {room: id});
	}

	render() {
		const { 
			showJoinDialog, 
			startGame, 
			joinedPlayers,
			username,
			bank 
		} = this.state;
		const { socket } = this.props;
		const { id } = this.props.match.params;
        const connectingView = <h3>Connecting...</h3>
        if (socket == null) {
            return connectingView;
        }
        const preGame = (
			<div>
				{this.showStartButton()}
				{this.showJoinButton()}
				{this.showRequests()}
				<Divider />
				{this.showJoinedPlayers()}
				<JoinDialog 
					open={showJoinDialog}
					room={id}
					onClose={this.handleClose}
				/>
			</div>
		)
		const inGame = <InGameDashboard 
							socket={socket} 
							room={id} 
							players={joinedPlayers}
							username={username}
							bank={bank}
        				/>

		const show = startGame ? inGame : preGame;

		return <div>{show}</div>
	}
}

const PreGameDashboard = connect(mapStateToProps)(ConnectedPreGameDashboard);

export default PreGameDashboard;
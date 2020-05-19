import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Button, List, ListItem, ListItemText, Divider } from '@material-ui/core';
import JoinDialog from './JoinDialog';
import InGameDashboard from './InGameDashboard';
import mapStateToProps from './js/utils/mapStateToProps';
import ChatComponent from './ChatComponent';

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
			bank: bank,
			usernameError: false,
			currState: null,
			pendingStandUp: false,
			pendingSitDown: false,
			isStoodUp: false
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
				return {
					joinedPlayers,
				}
			});
		});
		socket.on('game info', (data) => {
			let currState = null;
			if (data['started']) {
				currState = {
					communityCards: data['community_cards'],
					pot: data['pot'],
					highestCurrentContribution: data['highest_current_contribution']
				}
			}
			this.setState({
				joinedPlayers: data['players'],
				startGame: data['started'],
				currState: currState
			});
		});
		socket.on('game start', () => {
			this.setState({startGame: true});
		});
		socket.on('duplicate username', () => {
			this.setState({isRequested: false, usernameError: true})
		});
		socket.on('request response', (data) => {
			if (data['approve']) {
                this.setState({
					isRequested: false, 
					usernameError: false, 
					isJoined: true,
					username: data['username'],
					bank: data['bank']
				});
			} else {
                this.setState({isRequested: false});
			}
		});
	}
	
	loadUsers() {
		const { socket } = this.props;
		const { id } = this.props.match.params;

		socket.emit('game info', {room: id});
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
		this.setState(state => {
			const joinRequests = state.joinRequests.filter(x => x['username'] != data['username']);
			return {
				joinRequests
			}
		})
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

	handleClose = (value) => {
		this.setState({
			showJoinDialog: false, 
			isRequested: value
		});
		// if (value) {
		// 	update['username'] = newUsername
		// 	update['bank'] = newBank
		// } else if (newUsername) {
		// 	this.setState({
		// 		isRequested: true
		// 	})
		// }
		// console.log(this.state)
		// console.log(update)
        // this.setState(update);
    }

	startGame() {
		const { socket } = this.props;
		const { id } = this.props.match.params;

		socket.emit('start', {room: id});
	}

	showChatRoom() {
		const { isJoined, username } = this.state;
		const { id } = this.props.match.params;

		if (isJoined) {
			return <ChatComponent username={username} room={id} />
		}
	}

	showStandUpToggleButton() {
		const { startGame, pendingStandUp, isStoodUp } = this.state;
		if (startGame && (pendingStandUp || isStoodUp)) {
			return <Button 
			variant="contained" 
			type="submit" 
			onClick={() => this.toggleStandUp()}>Sit Down</Button>
		} else if (startGame) {
			return <Button 
				variant="contained" 
				type="submit" 
				onClick={() => this.toggleStandUp()}>Stand Up</Button>
		}
	}

	standUp() {

	}

	render() {
		const { 
			showJoinDialog, 
			startGame, 
			joinedPlayers,
			username,
			bank,
			currState 
		} = this.state;
		const { socket } = this.props;
		const { id } = this.props.match.params;
        const connectingView = <h3>Connecting...</h3>
        if (socket == null) {
            return connectingView;
        }
        const preGame = (
			<div>
				{this.showStandUpToggleButton()}
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
							currState={currState}
							room={id} 
							players={joinedPlayers}
							username={username}
							bank={bank}
        				/>

		const show = startGame ? inGame : preGame;

		return <div>
			{this.showChatRoom()}
			{show}
		</div>
	}
}

const PreGameDashboard = connect(mapStateToProps)(ConnectedPreGameDashboard);

export default PreGameDashboard;
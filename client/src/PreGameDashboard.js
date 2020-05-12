import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Button, List, ListItem, ListItemText, Divider } from '@material-ui/core';
import JoinDialog from './JoinDialog';

const mapStateToProps = state => {
    return {
        socket: state.socket,
        room: state.owner,
        joinedPlayers: state.joinedPlayers,
        joinRequests: state.joinRequests,
        startGame: state.startGame
    };
  }

class ConnectedPreGameDashboard extends Component {
    constructor(props) {
        super(props);

		let isOwner = false;
		let isJoined = false;
        if (this.props.location && this.props.location.state && this.props.location.state.isOwner) {
			isOwner = true;
			isJoined = true;
        }

        this.state = {
			isOwner: isOwner,
			isJoined: isJoined,
			isRequested: false,
			showJoinDialog: false,
			initialLoad: false
		};
	}

	componentDidMount() {
		this.checkSocketAndLoadUsers()
	}

	componentDidUpdate() {
		this.checkSocketAndLoadUsers()
		
	}
	
	checkSocketAndLoadUsers() {
		const { socket } = this.props;
		const { id } = this.props.match.params;
		const { initialLoad } = this.state;

		if (!socket || initialLoad) {
			return;
		}

		this.setState({initialLoad: true})
		socket.emit('list users', {room: id});
		

	}

    showStartButton() {
        const { isOwner } = this.state;
        const { joinedPlayers } = this.props;

		if (isOwner && joinedPlayers.length >= 2) {
			return <Button variant="contained" onClick={() => this.startGame()}>Start Game</Button>;
		} else {
			return null;
		}
	}

	showJoinedPlayers() {
		const { joinedPlayers } = this.props;

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
        const { isOwner } = this.state;
        const { joinRequests } = this.props;


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

	handleClose(value) {
        this.setState({showJoinDialog: false});
        if (value) {
            this.setState({isRequested: true});
        }
    }

	startGame() {
		const { socket, room } = this.props;
		socket.emit('start', {room: room});
	}

	render() {
		const { showJoinDialog } = this.state;
		const { socket, startGame } = this.props;
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
					onClose={(val) => this.handleClose(val)}
				/>
			</div>
		)
		// const inGame = <InGameDashboard 
		// 					socket={socket} 
		// 					room={room} 
		// 					players={joinedPlayers}
		// 					username={username}
		// 					bank={bank}
        // 				/>
        const inGame = <h3>in game</h3>

		const show = startGame ? inGame : preGame;

		return <div>{show}</div>
	}
}

const PreGameDashboard = connect(mapStateToProps)(ConnectedPreGameDashboard);

export default PreGameDashboard;
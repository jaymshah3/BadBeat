import React, { Component } from 'react';
import { any, bool, number } from 'prop-types';
import { Button, List, ListItem, Divider } from '@material-ui/core';

class PreGameDashboard extends Component {
  constructor(props) {
		super(props);
		this.state = {
			joinRequests: [],
			joinedPlayers: []
		};
	}

	componentDidMount() {
		this.defineHandlers();
		this.loadPlayers();
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
			console.log('user joined');
			console.log(data);
			this.setState((state) => {
				const joinedPlayers = state.joinedPlayers.concat(data);
				return {
					joinedPlayers
				}
			});
		});
		socket.on('user list', (data) => {
			this.setState({joinedPlayers: data["players"]});
		});
	}

	loadPlayers() {
		const { socket } = this.props;
		socket.emit('list users', {room: 1});
	}

	handleRequest = (element, decision) => {
		const { socket, room } = this.props;
		const data = {
			username: element['username'],
			bank: element['bank'],
			approve: decision,
			room: room
		}
		this.setState(state => {
			const joinRequests = state.joinRequests.filter(x => x['username'] != element['username']);
			return {
				joinRequests
			}
		});
		socket.emit('handle join request', data);
	}

	showStartButton() {
		const { isOwner } = this.props;
		const { joinedPlayers } = this.state;

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
							<p>{element['username']}</p>
							<p>{element['bank']}</p>
						</div>
					</ListItem>
				})
			}
		</List>
	}

	showRequests() {
		const { isOwner } = this.props;
		const { joinRequests } = this.state;

		if (isOwner) {
			return <List>
				{
					joinRequests.map((element) => {
						return <ListItem key={element['username']}>
							<div>
								<p>{element['username']}</p>
								<p>{element['bank']}</p>
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

	render() {
		return (
			<div>
				{this.showStartButton()}
				{this.showRequests()}
				<Divider />
				{this.showJoinedPlayers()}
			</div>
		)
	}
}

PreGameDashboard.propTypes = {
	socket: any,
	isOwner: bool,
	room: number
}

export default PreGameDashboard;
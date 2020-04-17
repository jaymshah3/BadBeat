import React, { Component } from 'react';
import { any, string, number } from 'prop-types';
import { Button } from '@material-ui/core';

class JoinRequest extends Component {
	constructor(props) {
		super(props);
	}

	handleRequest = (decision) => {
		const { socket, username, bank, room } = this.props;
		element = {
			username: username,
			bank: bank,
			approve: decision,
			room: room
		}
		socket.emit('handle join request', element);
	}

	render() {
		const { username, bank } = this.props;

		return (
			<li key={username}>
				<div>
					<p>{username}</p>
					<p>{bank}</p>
					<Button variant="contained" color="primary" onClick={() => {this.handleRequest(true)}}>Approve</Button>
					<Button variant="contained" color="secondary" onClick={() =>{this.handleRequest(false)}}>Reject</Button>
				</div>
			</li>
		)
	}
}

JoinRequest.propTypes = {
	socket: any,
	username: string,
	bank: number,
	room: number
}

export default JoinRequest;
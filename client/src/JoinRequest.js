import React, { Component } from 'react';
import { any, string, number } from 'prop-types';
import { Button } from '@material-ui/core';

class JoinRequest extends Component {
	constructor(props) {
		super(props);
	}

	handleRequest = (element, decision) => {
		const { socket } = this.props;
		element['approve'] = decision;
		socket.emit('handle join request', element);
	}

	render() {
		const { username, bank } = this.props;

		return (
			<li key={username}>
				<div>
					<p>{username}</p>
					<p>{bank}</p>
					<Button variant="contained" color="primary" onClick={() => {this.handleRequest(username, true)}}>Approve</Button>
					<Button variant="contained" color="secondary" onClick={() => this.handleRequest(username, false)}>Reject</Button>
				</div>
			</li>
		)
	}
}

JoinRequest.propTypes = {
	socket: any,
	username: string,
	bank: number
}

export default JoinRequest;
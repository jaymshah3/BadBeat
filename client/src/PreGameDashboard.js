import React, { Component } from 'react';
import { any, bool } from 'prop-types';
import JoinRequest from './JoinRequest.js';
import { Button, List, ListItem } from '@material-ui/core';

class PreGameDashboard extends Component {
  constructor(props) {
		super(props);
		this.state = {
			joinRequests: [{username: 'jay', bank: 1000}],
			joinedPlayers: [{username: 'sri', bank: 2000}]
		};
	}

	componentDidMount() {
		this.defineHandlers();
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
		socket.on('user has joined', (data) => {
			this.setState((state) => {
				const joinedPlayers = state.joinedPlayers.concat(data)
				return {
				joinedPlayers
				}
			});
		})
	}

	showStartButton() {
		const { owner } = this.props;
		const { joinedPlayers } = this.state;
		console.log(owner);

		if (owner && joinedPlayers.length >= 2) {
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
		const { socket, owner } = this.props;
		const { joinRequests } = this.state;

		if (owner) {
			return <List>
					{
						joinRequests.map((element) => {
							return <ListItem key={element['username']}>
								<JoinRequest socket={socket} username={element['username']} bank={element['bank']} />
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
				{this.showJoinedPlayers()}
			</div>
		)
	}
}

PreGameDashboard.propTypes = {
	socket: any,
	owner: bool
}

export default PreGameDashboard;
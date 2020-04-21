import React, { Component } from 'react';
import { List, ListItem, Button, Divider, ListItemText } from '@material-ui/core';
import { any, number, string } from 'prop-types';
import RaiseDialog from './RaiseDialog.js';

class InGameDashboard extends Component {
    constructor(props) {
        super(props);

        const players = props['players'];
        const newList = players.map(x => {
            return {
                username: x['username'], 
                bank: x['bank'], 
                latestAction: 'check',
            }
        });
        this.state = {
            starting: true,
            personalCards: [],
            communityCards: [],
            options: [],
            highestCurrentContribution: 0,
            currentPlayers: newList,
            pot: 0,
            bank: props['bank'],
            showRaiseDialog: false
        }
    }

    componentDidMount() {
        const { currentPlayers } = this.state;
        this.defineHandlers();
    }

    defineHandlers() {
        const { socket } = this.props;

        socket.on('dealt cards', (data) => {
            this.setState({personalCards: data['cards']})
        });

        socket.on('options for player', (data) => {
            this.setState({
                options: data['options'], 
                highestCurrentContribution: data['highest_contribution']
            });
        });

        socket.on('highest contribution', (data) => {
            this.setState({
                highestCurrentContribution: data['highest_contribution']
            });
        });

        socket.on('player action', (data) => {
            this.setState(state => {
                const newList = []
                const currentPlayers = state['currentPlayers'];
                for (let i = 0; i < currentPlayers.length; i++) {
                    if (currentPlayers[i]['username'] == data['username']) {
                        currentPlayers[i]['latestAction'] = data['action'];
                        currentPlayers[i]['currentContribution'] = data['currentContribution'];
                        if (data['action'] != 'fold') {
                            currentPlayers[i]['bank'] -= data['amount'];
                        }
                    }
                    newList.push(currentPlayers[i]);
                }
                return {
                    currentPlayers: newList
                }
            });
        });

        socket.on('pot update', (data) => {
            this.setState({pot: data['pot']});
        });

        socket.on('community cards', (data) => {
            this.setState({communityCards: data['community_cards']});
        });
    }

    getMyCurrentContribution() {
        const { currentPlayers } = this.state;
        const { username } = this.props;
        console.log(currentPlayers)
        console.log(username)

        for (let i = 0; i < currentPlayers.length; i++) {
            if (currentPlayers[i]['username'] == username) {
                return currentPlayers[i]['currentContribution'];
            }
        }
    }

    showButtonForAction(action) {
        const { highestCurrentContribution, currentContribution } = this.state;

        if (action == 'fold') {
            return <Button onClick={() => this.doAction('fold')}>Fold</Button>
        } else if (action == 'raise') {
            return <Button onClick={() => this.doAction('raise')}>Raise</Button>
        } else if (action == 'call') {
            return <Button onClick={() => this.doAction('call')}>Call for {highestCurrentContribution - this.getMyCurrentContribution()}</Button>
        } else {
            return <Button onClick={() => this.doAction('check')}>Check</Button>
        }
    }

    doAction(action) {
        if (action == 'fold') {
            this.fold();
        } else if (action == 'call' || action == 'check') {
            this.call();
        } else {
            this.setState({showRaiseDialog: true})
        }
    }

    handleClose(value) {
        this.setState({showRaiseDialog: false});
        if (value) {
            this.setState({options: []});
        }
    }

    fold() {
        const { socket, username } = this.props;

        socket.emit('fold', {username: username});
        this.setState({options: []});
    }

    call() {
        const { socket, username } = this.props;
        const { highestCurrentContribution } = this.state;
        const currentContribution = highestCurrentContribution - this.getMyCurrentContribution()

        socket.emit('call', {username: username, amount: highestCurrentContribution-currentContribution});
        this.setState({options: []});
    }

    render() {
        const { 
            currentPlayers, 
            options, 
            highestCurrentContribution,
            bank, 
            showRaiseDialog,
            personalCards,
            communityCards,
            pot 
        } = this.state;
        const { username, socket } = this.props;

        return <div>
            <List>
                {
                    currentPlayers.map((element) => {
                        return <ListItem key={element['username']}>
                            <div>
                                <ListItemText>{element['username']}</ListItemText>
                                <ListItemText>{element['bank']}</ListItemText>
                            </div>
                        </ListItem>
                    })
                }
            </List>
            <Divider />
            <h3>Your cards</h3>
            <List>
                {
                    personalCards.map((element) => {
                        return <ListItem key={element['value'] + element['suit']}>
                            <ListItemText>{element['value']} of {element['suit']}</ListItemText>
                        </ListItem>
                    })
                }
            </List>
            <Divider />
            <h3>Community cards</h3>
            <List>
                {
                    communityCards.map((element) => {
                        return <ListItem key={element['value'] + element['suit']}>
                            <ListItemText>{element['value']} of {element['suit']}</ListItemText>
                        </ListItem>
                    })
                }
            </List>
            <Divider />
            <List>
                {
                    options.map((element) => {
                        return <ListItem key={element}>
                            {this.showButtonForAction(element)}
                        </ListItem>
                    })
                }
            </List>
            <Divider />
            <RaiseDialog 
                username={username}
                bank={bank}
                socket={socket}
                open={showRaiseDialog}
                onClose={(value) => this.handleClose(value)}
            />
            <h3>Pot: {pot}</h3>
            <h3>Your Current Contribution: {this.getMyCurrentContribution()}</h3>
            <h3>Highest Contribution: {highestCurrentContribution}</h3>
        </div>
    }
}

InGameDashboard.propTypes = {
	socket: any,
    room: number,
    players: any,
    username: string
}

export default InGameDashboard;
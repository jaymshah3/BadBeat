import React, { Component } from 'react';
import { List, ListItem, Button, Divider, ListItemText } from '@material-ui/core';
import { any, number, string } from 'prop-types';
import { connect } from 'react-redux';
import RaiseDialog from './RaiseDialog.js';
import mapStateToProps from './js/utils/mapStateToProps';

class ConnectedInGameDashboard extends Component {
    constructor(props) {
        super(props);

        const players = props['players'];
        const newList = players.map(x => {
            return {
                username: x['username'], 
                bank: x['bank'], 
                latestAction: '',
                currentContribution: 0
            }
        });
        let communityCards = [];
        let pot = 0;
        let highestCurrentContribution = 0;
        if (props['currState']) {
            communityCards = props['currState']['communityCards'];
            pot = props['currState']['pot'];
            highestCurrentContribution = props['currState']['highestCurrentContribution'];
        }
        console.log("beginning: " + JSON.stringify(newList))
        this.state = {
            personalCards: [],
            communityCards: communityCards,
            options: [],
            highestCurrentContribution: highestCurrentContribution,
            currentPlayers: newList,
            pot: pot,
            showRaiseDialog: false,
            winnings: 0,
            winners: [],
            maxBet: 0,
            minBet: 0
        }
    }

    componentDidMount() {
        this.defineHandlers();
    }

    resetState() {
        const { currentPlayers } = this.state;

        this.setState({
            personalCards: [],
            communityCards: [],
            options: [],
            highestCurrentContribution: 0,
            currentPlayers: currentPlayers,
            pot: 0,
            showRaiseDialog: false,
            winnings: 0,
            winners: [] 
        })
    }

    defineHandlers() {
        const { socket, username } = this.props;

        socket.on('dealt cards', (data) => {
            this.setState({
                personalCards: data['cards'],
                result: '',
                winnings: 0
            });
        });

        socket.on('options for player', (data) => {
            this.setState({
                options: data['options'], 
                highestCurrentContribution: data['highest_contribution'],
                maxBet: data['max_bet'],
                minBet: data['min_bet']
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
                    let newObj = {};
                    if (currentPlayers[i]['username'] == data['username']) {
                        newObj['username'] = currentPlayers[i]['username'];
                        newObj['latestAction'] = data['action'];
                        newObj['currentContribution'] = data['currentContribution'];
                        newObj['bank'] = currentPlayers[i]['bank']
                    } else {
                        newObj = currentPlayers[i];
                    }
                    newList.push(newObj);
                }
                return {
                    currentPlayers: newList
                }
            });
        });

        socket.on('withdraw', (data) => {
            this.setState(state => {
                const newList = []
                const currentPlayers = state['currentPlayers'];
                for (let i = 0; i < currentPlayers.length; i++) {
                    let newObj = {};
                    if (currentPlayers[i]['username'] == data['username']) {
                        newObj['username'] = currentPlayers[i]['username'];
                        newObj['latestAction'] = currentPlayers[i]['action'];
                        newObj['currentContribution'] = currentPlayers[i]['currentContribution'];
                        newObj['bank'] = currentPlayers[i]['bank'] - data['amount']
                    } else {
                        newObj = currentPlayers[i];
                    }
                    newList.push(newObj);
                }
                console.log(newList)
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

        socket.on('reset current contribution', (data) => {
            this.setState(state => {
                const newList = []
                const currentPlayers = state['currentPlayers'];
                for (let i = 0; i < currentPlayers.length; i++) {
                    let newObj = {};
                    newObj['username'] = currentPlayers[i]['username'];
                    newObj['latestAction'] = '';
                    newObj['currentContribution'] = 0;
                    newObj['bank'] = currentPlayers[i]['bank']
                    
                    newList.push(newObj);
                }
                return {
                    currentPlayers: newList,
                }
            });
        });

        socket.on('current hand', (data) => {
            this.setState({currentHand: data});
        });

        socket.on('best hand', (data) => {
            this.setState({currentHand: data});
        });

        socket.on('result', (data) => {
            this.setState(state => {
                const newList = []
                let winners = []
                let winnings = 0;
                const currentPlayers = state['currentPlayers'];
                for (let i = 0; i < currentPlayers.length; i++) {
                    let newObj = {};
                    const resultObj = data[currentPlayers[i]['username']]
                    console.log("resultObj")
                    console.log(resultObj)
                    newObj['username'] = currentPlayers[i]['username'];
                    newObj['latestAction'] = currentPlayers[i]['action'];
                    newObj['currentContribution'] = currentPlayers[i]['currentContribution'];
                    newObj['bank'] = resultObj['final_bank']
                    if (username == currentPlayers[i]['username']) {
                        winnings = resultObj['winnings']
                    }
                    if (resultObj['winnings'] > 0) {
                        winners.push(resultObj);
                    }
                    console.log("newObj")
                    console.log(newObj)
                    newList.push(newObj);
                }
                console.log("newList")
                console.log(newList)
                return {
                    currentPlayers: newList,
                    personalCards: [],
                    communityCards: [],
                    options: [],
                    highestCurrentContribution: 0,
                    pot: 0,
                    showRaiseDialog: false,
                    currentHand: null
                }
            }, () => {console.log(this.state)});
        });

        // socket.on('new game', () => {
        //     this.resetState();
        // });
    }

    getMyCurrentContribution() {
        const { currentPlayers } = this.state;
        const { username } = this.props;

        for (let i = 0; i < currentPlayers.length; i++) {
            if (currentPlayers[i]['username'] == username) {
                return currentPlayers[i]['currentContribution'];
            }
        }
    }

    getMyCurrentBank() {
        const { currentPlayers } = this.state;
        const { username } = this.props;

        for (let i = 0; i < currentPlayers.length; i++) {
            if (currentPlayers[i]['username'] == username) {
                return currentPlayers[i]['bank'];
            }
        }
    }

    showWinOrLoss() {
        const { winners } = this.state;
        if (winners.length == 0) {
            return null;
        } else {
            return <List>
                        {winners.map(x => <ListItem key={x['username']}>
                            <p>{x['username'] + ' ' + x['winnings'] + ' ' + x['hand'][0]['value'] + " of " + x['hand'][0]['suit'] + ', ' + x['hand'][1]['value'] + " of " + x['hand'][1]['suit']}</p>
                        </ListItem>)}
                    </List>
                    
        }
    }

    showCurrentHand() {
        const { currentHand } = this.state;
        if (currentHand == null) {
            return null;
        } else {
            let cardsString = '';
            for (let i = 0; i < currentHand['cards'].length; i++) {
                cardsString += currentHand['cards'][i]['value'] + " of " + currentHand['cards'][i]['suit']
                cardsString += ", "
            }
            return <h3>Your best hand is {currentHand['major_group']} with cards {cardsString}</h3>
        }
    }

    showButtonForAction(action) {
        const { highestCurrentContribution } = this.state;

        if (action == 'fold') {
            return <Button onClick={() => this.doAction('fold')}>Fold</Button>
        } else if (action == 'raise') {
            return <Button onClick={() => this.doAction('raise')}>Raise</Button>
        } else if (action == 'call') {
            return <Button onClick={() => this.doAction('call')}>Call for {highestCurrentContribution - this.getMyCurrentContribution()}</Button>
        } else if (action =='check') {
            return <Button onClick={() => this.doAction('check')}>Check</Button>
        } else if (action == 'bet') {
            return <Button onClick={() => this.doAction('raise')}>Bet</Button>
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
        const { socket, username, room } = this.props;

        socket.emit('fold', {username: username, room: room});
        this.setState({options: []});
    }

    call() {
        const { socket, username, room } = this.props;
        const { highestCurrentContribution } = this.state;
        const currentContribution = this.getMyCurrentContribution()

        console.log(username);

        socket.emit('call', {
            username: username, 
            amount: highestCurrentContribution-currentContribution,
            room: room
        });
        this.setState({options: []});
    }

    render() {
        const { 
            currentPlayers, 
            options, 
            highestCurrentContribution,
            showRaiseDialog,
            personalCards,
            communityCards,
            pot,
            minBet,
            maxBet 
        } = this.state;
        const { username, socket, room } = this.props;
        const bank = this.getMyCurrentBank()
        const currentContribution = this.getMyCurrentContribution();

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
            {this.showWinOrLoss()}
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
                room={room}
                socket={socket}
                open={showRaiseDialog}
                onClose={(value) => this.handleClose(value)}
                currentContribution={currentContribution}
                minBet={minBet}
                maxBet={maxBet}
            />
            {this.showCurrentHand()}
            <h3>Pot: {pot}</h3>
            <h3>Your Current Contribution: {currentContribution}</h3>
            <h3>Highest Contribution: {highestCurrentContribution}</h3>
        </div>
    }
}


const InGameDashboard = connect(mapStateToProps)(ConnectedInGameDashboard);

export default InGameDashboard;
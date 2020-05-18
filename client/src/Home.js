import React, { Component } from 'react';
import { connect } from 'react-redux';
import { TextField, Button } from '@material-ui/core';
import { Redirect } from 'react-router-dom';
import { isUnsanitized, isInvalidNum } from './js/utils/input-validators';
import mapStateToProps from './js/utils/mapStateToProps';


class ConnectedHome extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            bank: '',
            smallBlind: '',
            bigBlind: '',
            usernameError: true,
            bankError: true,
            smallBlindError: true,
            bigBlindError: true,
            owner: null
        }
    }

    componentDidMount() {
        const { socket } = this.props;

        socket.on('owner',(data) => {
            this.setState({
                owner: data.room            
            });
        });
    }

    handleUsernameChange = (e) => {
        this.setState({
            username: e.target.value,
            usernameError: isUnsanitized(e.target.value)
        });
    }

    handleBankChange = (e) => {
        this.setState({
            bank: e.target.value,
            bankError: isInvalidNum(e.target.value)
        });
    }

    handleSmallBlindChange = (e) => {
        this.setState({
            smallBlind: e.target.value,
            smallBlindError: isInvalidNum(e.target.value)
        });
    }

    handleBigBlindChange = (e) => {
        this.setState({
            bigBlind: e.target.value,
            bigBlindError: isInvalidNum(e.target.value)
        });
    }

    isError() {
        const { usernameError, bankError, smallBlindError, bigBlindError } = this.state;

        return (usernameError || bankError || smallBlindError || bigBlindError);
    }

    render() {
        const { username, bank, smallBlind, bigBlind, owner } = this.state;

        if (owner) {
            return <Redirect 
                to={{
                    pathname: "/"+owner,
                    state: { 
                        isOwner: true,
                        username: username,
                        bank: bank 
                    }
                }}
            />
        }

        const createGameView = (
            <div>
                <TextField 
                    value={username} 
                    onChange={this.handleUsernameChange} 
                    id="outlined-basic" 
                    label="Username" 
                    variant="outlined" 
                />
                <TextField 
                    value={bank} 
                    onChange={this.handleBankChange} 
                    id="outlined-basic" 
                    label="Bank" 
                    variant="outlined" 
                />
                <TextField 
                    value={smallBlind} 
                    onChange={this.handleSmallBlindChange} 
                    id="outlined-basic" 
                    label="Small Blind" 
                    variant="outlined" 
                />
                <TextField 
                    value={bigBlind} 
                    onChange={this.handleBigBlindChange} 
                    id="outlined-basic" 
                    label="Big Blind" 
                    variant="outlined" 
                />
                <Button 
                    variant="contained" 
                    type="submit" 
                    disabled={this.isError()} 
                    onClick={() => this.createGame()}
                >Create Game</Button>

            </div>
        )
                
        return createGameView;
    }

    createGame() {
        const { username, bank, smallBlind, bigBlind } = this.state;
        const { socket } = this.props;
        socket.emit('create room', {
            username: username,
            bank: parseInt(bank),
            small_blind: parseInt(smallBlind),
            big_blind: parseInt(bigBlind)
        });
    }
}

const Home = connect(mapStateToProps)(ConnectedHome);

export default Home;
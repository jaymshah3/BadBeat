import React, { Component } from 'react';
import { TextField, Dialog, DialogTitle, Button } from '@material-ui/core';
import { connect } from 'react-redux';
import { isInvalidNum, isUnsanitized } from './js/utils/input-validators';
import mapStateToProps from './js/utils/mapStateToProps';


class ConnectedJoinDialog extends Component {
    constructor(props) {
        super(props);

        this.state = {
            username: '',
            bank: '',
        }
    }

    handleUsernameChange(e) {
        this.setState({
            username: e.target.value
        });
    }

    handleBankChange(e) {
        this.setState({
            bank: e.target.value
        })
    }

    handleClose() {
        const { onClose } = this.props;

        onClose(false);
    }

    join() {
        const { socket, room, onClose } = this.props;

        const { bank, username } = this.state;
        socket.emit('request to join', {
            username: username,
            room: room,
            bank: parseInt(bank)
        });
        onClose(true, username, bank);
    }

    isDisabled() {
        const { bank, username } = this.state;
        return (isInvalidNum(bank) || isUnsanitized(username));
    }

    render() {
        const { username, bank, usernameError } = this.state;
        const { open } = this.props

        return <Dialog onClose={() => this.handleClose()} open={open}>
        <DialogTitle>Join Game</DialogTitle>
        <TextField 
            label="Username" 
            value={username} 
            onChange={(e) => this.handleUsernameChange(e)}
            helperText={usernameError ? "Username already exists. " : ""}
            error={usernameError}
        />
        <TextField 
            label="Bank" 
            value={bank} 
            onChange={(e) => this.handleBankChange(e)}
        />
        <Button onClick={() => this.join()} disabled={this.isDisabled()}>Join</Button>
    </Dialog>
    }
}

const JoinDialog = connect(mapStateToProps)(ConnectedJoinDialog);

export default JoinDialog;
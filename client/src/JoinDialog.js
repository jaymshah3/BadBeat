import React, { Component } from 'react';
import { TextField, Dialog, DialogTitle, Button } from '@material-ui/core';
import { connect } from 'react-redux';
import { isInvalidNum, isUnsanitized } from './js/utils/input-validators';

const mapStateToProps = state => {
    return {
        socket: state.socket
    };
  }

class ConnectedJoinDialog extends Component {
    constructor(props) {
        super(props);

        this.state = {
            username: '',
            bank: ''
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
        onClose(true)
        
    }

    isDisabled() {
        const { bank, username } = this.state;
        console.log(bank)
        console.log(username)
        return (isInvalidNum(bank) || isUnsanitized(username));
    }

    render() {
        const { username, bank } = this.state;
        const { open } = this.props;

        return <Dialog onClose={() => this.handleClose()} open={open}>
        <DialogTitle>Join Game</DialogTitle>
        <TextField label="Username" value={username} onChange={(e) => this.handleUsernameChange(e)}/>
        <TextField label="Bank" value={bank} onChange={(e) => this.handleBankChange(e)}/>
        <Button onClick={() => this.join()} disabled={this.isDisabled()}>Done</Button>
    </Dialog>
    }
}

const JoinDialog = connect(mapStateToProps)(ConnectedJoinDialog);

export default JoinDialog;
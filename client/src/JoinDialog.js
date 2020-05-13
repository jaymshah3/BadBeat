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
            bank: '',
            isRequested: false,
            usernameError: false,
        }
    }

    componentDidMount() {
        const { socket, onClose } = this.props;

        socket.on('request response', (data) => {
			if (data['approve']) {
                this.setState({isRequested: false, usernameError: false});
                console.log(data)
                onClose(true, data['username'], data['bank']);
			} else {
                this.setState({isRequested: false});
			}
		});

		socket.on('duplicate username', () => {
			this.setState({isRequested: false, usernameError: true})
		});
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
        const { socket, room } = this.props;

        const { bank, username } = this.state;
        socket.emit('request to join', {
            username: username,
            room: room,
            bank: parseInt(bank)
        });
        this.setState({
            isRequested: true
        })
    }

    isDisabled() {
        const { bank, username } = this.state;
        return (isInvalidNum(bank) || isUnsanitized(username));
    }

    render() {
        const { username, bank, usernameError, isRequested } = this.state;
        const { open } = this.props;

        const button = <Button onClick={() => this.join()} disabled={this.isDisabled()}>Join</Button>;
        const requested = <p>Requested...</p>

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
        {isRequested ? requested : button}
    </Dialog>
    }
}

const JoinDialog = connect(mapStateToProps)(ConnectedJoinDialog);

export default JoinDialog;
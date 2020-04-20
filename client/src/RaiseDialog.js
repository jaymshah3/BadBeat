import React, { Component } from 'react';
import { TextField, Dialog, DialogTitle, Button } from '@material-ui/core';
import { bool, number, string, func, any } from 'prop-types';

class RaiseDialog extends Component {
    constructor(props) {
        super(props);
        this.state = {
            amount: 0
        }
    }

    handleAmountChange(e) {
        this.setState({
            amount: parseInt(e.target.value)
        });
    }

    raise() {
        const { socket, onClose, username } = this.props;
        const { amount } = this.state;

        socket.emit('raise', {
            username: username,
            amount: amount
        });
        onClose(true);
    }

    handleClose() {
        const { onClose } = this.props;
        onClose(false);
    }


    render() {  
        const { bank, open } = this.props;
        const { amount } = this.state;

        return <Dialog onClose={() => this.handleClose()} open={open}>
            <DialogTitle>How much do you want to add?</DialogTitle>
            <p>Your bank is {bank}.</p>
            <TextField value={amount} onChange={this.handleAmountChange}/>
            <Button onClick={() => this.raise()}>Done</Button>
        </Dialog>
    }
}

RaiseDialog.propTypes = {
    bank: number,
    open: bool,
    username: string,
    onClose: func,
    socket: any
}

export default RaiseDialog;
import React, { Component } from 'react';
import { TextField, Dialog, DialogTitle, Button } from '@material-ui/core';
import { bool, number, string, func, any } from 'prop-types';
import { connect } from 'react-redux';

const mapStateToProps = state => {
    return {
        socket: state.socket,
    };
}

class ConnectedRaiseDialog extends Component {
    constructor(props) {
        super(props);
        this.state = {
            amount: ''
        }
    }

    handleAmountChange(e) {
        this.setState({
            amount: e.target.value
        });
    }

    raise() {
        const { socket, onClose, username, room } = this.props;
        const { amount } = this.state;

        socket.emit('raise', {
            username: username,
            amount: parseInt(amount),
            room: room
        });
        onClose(true);
    }

    handleClose() {
        const { onClose } = this.props;
        onClose(false);
    }


    render() {  
        const { bank, open, currentContribution } = this.props;
        const { amount } = this.state;

        return <Dialog onClose={() => this.handleClose()} open={open}>
            <DialogTitle>How much do you want to raise to?</DialogTitle>
            <p>Your bank is {bank}. You've already contributed {currentContribution}. </p>
            <TextField value={amount} onChange={(e) => this.handleAmountChange(e)}/>
            <Button onClick={() => this.raise()} disabled={isNaN(amount) || amount == ''}>Done</Button>
        </Dialog>
    }
}

// RaiseDialog.propTypes = {
//     bank: number,
//     open: bool,
//     username: string,
//     onClose: func,
//     socket: any,
//     currentContribution: number,
//     room: string
// }

const RaiseDialog = connect(mapStateToProps)(ConnectedRaiseDialog);

export default RaiseDialog;
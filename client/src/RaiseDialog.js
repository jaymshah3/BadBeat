import React, { Component } from 'react';
import { Dialog, DialogTitle, Button, Slider } from '@material-ui/core';
import { bool, number, string, func, any } from 'prop-types';
import { connect } from 'react-redux';
import mapStateToProps from './js/utils/mapStateToProps';

class ConnectedRaiseDialog extends Component {
    constructor(props) {
        super(props);
        console.log(props);
        this.state = {
            amount: props.minBet
        }
    }

    componentDidUpdate(prevProps) {
        if (prevProps.minBet == this.props.minBet) {
            return;
        }

        this.setState({
            amount: this.props.minBet
        });
    }

    handleAmountChange(_, value) {
        this.setState({
            amount: value
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
        const { bank, open, currentContribution, minBet, maxBet } = this.props;
        const { amount } = this.state;

        return <Dialog onClose={() => this.handleClose()} open={open}>
            <DialogTitle>How much do you want to raise to?</DialogTitle>
            <p>Your bank is {bank}. You've already contributed {currentContribution}. </p>
            <Slider
                defaultValue={minBet}
                max={Math.min(maxBet, bank)}
                min={minBet}
                onChange={(e, v) => this.handleAmountChange(e, v)}
                step={1}
            />
            <p>{amount}</p>
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
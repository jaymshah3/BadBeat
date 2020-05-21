import React, { Component } from 'react';
import { connect } from 'react-redux';
import mapStateToProps from './js/utils/mapStateToProps';
import { List, ListItem, Input } from '@material-ui/core';

class ConnectedChatComponent extends Component {
    
    MAX_MESSAGES = 500;

    constructor(props) {
        super(props);
        
        this.state = {
            messages: [],
            message: ''
        }
    }

    componentDidMount() {
        this.defineHandlers();
    }

    defineHandlers() {
        const { socket } = this.props;
        socket.on('chat message', (data) => {
            this.setState(state => {
                let messages = state.messages.concat(data);
                if (messages.length > this.MAX_MESSAGES) {
                    messages = messages.slice(messages.length() - this.MAX_MESSAGES)
                }
                return {
                    messages
                }
            });
        });
    }

    renderMessage(element) {
        return <li><p><b>{element.username + ": "}</b>{element.message}</p></li>
    }

    handleMessageChange(e) {
        this.setState({
            message: e.target.value
        })
    }

    onFormSubmit(e) {
        e.preventDefault()
        const { message } = this.state;
        const { socket, username, room } = this.props;

        if (message != "") {
            socket.emit('chat message', {
                room: room,
                message: message,
                username: username
            });
            this.setState({
                message: ''
            })
        }
    }

    render() {
        const { messages, message } = this.state;

        return <div>
            <ul>
                {
                    messages.map((x, i) => this.renderMessage(x, i))
                }
            </ul>
            
            <form onSubmit={(e) => this.onFormSubmit(e)}>
                <Input 
                    label="Chat"
                    value={message}
                    onChange={(v) => this.handleMessageChange(v)}
                />
            </form>

        </div>
    }

}

const ChatComponent = connect(mapStateToProps)(ConnectedChatComponent);

export default ChatComponent;
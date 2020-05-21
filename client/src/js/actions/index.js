import { SET_SOCKET } from '../constants/action-types';

export function setSocket(payload) {
    return {
        type: SET_SOCKET, 
        payload
    }
};
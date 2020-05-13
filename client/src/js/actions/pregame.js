import { 
    ADD_JOIN_REQUEST, 
    ADD_JOINED_PLAYER, 
    SET_JOINED_PLAYERS,
    SET_GAME_START,
    REMOVE_JOIN_REQUEST
} from '../constants/action-types';

export function addJoinRequest(payload) {
    return {
        type: ADD_JOIN_REQUEST, 
        payload
    }
};

export function addJoinedPlayer(payload) {
    return {
        type: ADD_JOINED_PLAYER, 
        payload
    }
};

export function setJoinedPlayers(payload) {
    return {
        type: SET_JOINED_PLAYERS,
        payload
    }
}

export function setGameStart(payload) {
    return {
        type: SET_GAME_START,
        payload
    }
}

export function removeJoinRequest(payload) {
    return {
        type: REMOVE_JOIN_REQUEST,
        payload
    }
}
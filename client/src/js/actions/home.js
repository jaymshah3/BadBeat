import { SET_OWNER } from '../constants/action-types';

export function setOwner(payload) {
    return {
        type: SET_OWNER, 
        payload
    }
};
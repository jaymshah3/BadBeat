import { 
  SET_SOCKET, 
  SET_OWNER, 
  ADD_JOIN_REQUEST, 
  ADD_JOINED_PLAYER,
  SET_JOINED_PLAYERS,
  SET_GAME_START,
  REMOVE_JOIN_REQUEST
} from "../constants/action-types";

const initialState = {
    socket: undefined,
    // owner: undefined,
    // joinRequests: [],
    // joinedPlayers: [],
    // startGame: false
  };
  
  function rootReducer(state = initialState, action) {
    if (action.type == SET_SOCKET) {
      return Object.assign({}, state, {
        socket: action.payload
      });
    // } else if (action.type == SET_OWNER) {
    //   return Object.assign({}, state, {
    //     owner: action.payload
    //   });
    // } else if (action.type == ADD_JOINED_PLAYER) {
    //   return Object.assign({}, state, {
    //     joinedPlayers: state.joinedPlayers.concat(action.payload)
    //   });
    // } else if (action.type == ADD_JOIN_REQUEST) {
    //   return Object.assign({}, state, {
    //     joinRequests: state.joinRequests.concat(action.payload)
    //   });
    // } else if (action.type == SET_JOINED_PLAYERS) {
    //   return Object.assign({}, state, {
    //     joinedPlayers: action.payload['players']
    //   })
    // } else if (action.type == SET_GAME_START) {
    //   return Object.assign({}, state, {
    //     startGame: action.payload
    //   });
    // } else if (action.type == REMOVE_JOIN_REQUEST) {
    //   return Object.assign({}, state, {
    //     joinRequests: state.joinRequests.filter(x => x['username'] != action.payload['username'])
    //   });
    }
    return state;
  };
  
  export default rootReducer;
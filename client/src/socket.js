import { reactive } from "vue";
import { io } from "socket.io-client";
export const socket = io()

export var state = reactive({
    connected: false,
    myResponses: []
});

//state.connected=true;
//state.connected=true;
socket.on("connected", () => {
  console.log("connected");
  state.connected = true;
});

//socket.on("disconnect", () => {
 // state.connected = false;
//});


socket.on("my_response", (response) => {
  state.myResponses.push(response);
});


export function sendMyEvent(message) {
  socket.emit("my_event", { data: message });
}

export function sendMyBroadcastEvent(message) {
  socket.emit("my_broadcast_event", { data: message });
}

export function joinRoom(room) {
  socket.emit("join", { room });
}

export function leaveRoom(room) {
  socket.emit("leave", { room });
}

export function closeRoom(room) {
  socket.emit("close_room", { room });
}

export function sendToRoom(room, message) {
  socket.emit("my_room_event", { data: message, room });
}

export function requestDisconnect() {
  socket.emit("disconnect_request");
}

export default { state, socket };


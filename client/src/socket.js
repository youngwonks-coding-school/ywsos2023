import { reactive } from "vue";
import { io } from "socket.io-client";
// export const socket = io("ws://127.0.0.1:5000")

// export var state = reactive({
//   connected: false,
//   myResponses: []
// });



//whenever something is emitted on back end, use socketio.on("what was emitted", () => {code needed}); for a response



// socket.on('connect', () => {
//   console.log("I am connected")
//   state.connected = true;
//   socket.emit("my_event",{data:"connected"})
// });



// socket.on("disconnect", () => {
//   state.connected = false;
//   console.log("I am disconnected")
// });





export default { state, socket };

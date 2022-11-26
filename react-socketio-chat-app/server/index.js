const express = require("express");
const app = express();
const http = require("http");
const cors = require("cors");
const { Server } = require("socket.io");
const _ = require("lodash");
const axios = require("axios");
app.use(cors());

const server = http.createServer(app);

const io = new Server(server, {
  cors: {
    origin: "http://localhost:3000",
    methods: ["GET", "POST"],
  },
});

const modelServerUrl =
  "https://xewbi-01gjsajz6vwfast8kk9t49qzds.litng-ai-03.litng.ai/api/predict/"; // put your API URL here

io.on("connection", (socket) => {
  console.log(`User Connected: ${socket.id}`);

  socket.on("join_room", (data) => {
    socket.join(data);
    console.log(`User with ID: ${socket.id} joined room: ${data}`);
  });

  socket.on("send_message", async (data) => {

    if (_.get(data, 'img', null) === null) {
      socket.to(data.room).emit("receive_message", data);
    } else {
      try {
        const modelResponse = await axios.post(
          modelServerUrl,
          { encoded_image_str: data.img }
        );

        if (_.get(modelResponse.data, "lewd_image_flag", false)) {
          socket
            .to(data.room)
            .emit("receive_message", {
              room: data.room,
              author: "SERVER",
              message:
                "SERVER: The user tried to send an NSFW image which is blocked as per out content policy",
              time: data.time,
            });
        } else {
          socket.to(data.room).emit("receive_message", data);
        }
      } catch {
        socket.to(data.room).emit("receive_message", data);
      }
    }
  });

  socket.on("disconnect", () => {
    console.log("User Disconnected", socket.id);
  });
});

server.listen(3001, () => {
  console.log("SERVER RUNNING");
});

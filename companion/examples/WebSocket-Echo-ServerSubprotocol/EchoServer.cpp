#include "EchoServer.h"

#include <log/Logger.h>

EchoServer::EchoServer(web::websocket::SubProtocolContext* context, const std::string& name)
    : web::websocket::server::SubProtocol(context, name, 90, 3) {
}

void EchoServer::onConnected() {
    VLOG(1) << "WebSocket echo server connected";
}

void EchoServer::onMessageStart(int) {
    currentMessage.clear();
}

void EchoServer::onMessageData(const char* chunk, std::size_t chunkLen) {
    currentMessage.append(chunk, chunkLen);
}

void EchoServer::onMessageEnd() {
    VLOG(1) << "WebSocket echo server received: " << currentMessage;
    sendMessage(currentMessage);
    currentMessage.clear();
}

void EchoServer::onMessageError(uint16_t errnum) {
    LOG(WARNING) << "WebSocket echo server message error: " << errnum;
    currentMessage.clear();
}

void EchoServer::onDisconnected() {
    VLOG(1) << "WebSocket echo server disconnected";
    currentMessage.clear();
}

bool EchoServer::onSignal(int) {
    sendClose();
    return false;
}

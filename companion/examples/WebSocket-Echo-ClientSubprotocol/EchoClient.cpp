#include "EchoClient.h"

#include <log/Logger.h>

EchoClient::EchoClient(web::websocket::SubProtocolContext* context, const std::string& name)
    : web::websocket::client::SubProtocol(context, name, 90, 3) {
}

void EchoClient::onConnected() {
    VLOG(1) << "WebSocket echo client connected";
    sendMessage("hello");
}

void EchoClient::onMessageStart(int) {
    currentMessage.clear();
}

void EchoClient::onMessageData(const char* chunk, std::size_t chunkLen) {
    currentMessage.append(chunk, chunkLen);
}

void EchoClient::onMessageEnd() {
    VLOG(1) << "WebSocket echo client received: " << currentMessage;
    currentMessage.clear();
    sendClose();
}

void EchoClient::onMessageError(uint16_t errnum) {
    LOG(WARNING) << "WebSocket echo client message error: " << errnum;
    currentMessage.clear();
}

void EchoClient::onDisconnected() {
    VLOG(1) << "WebSocket echo client disconnected";
    currentMessage.clear();
}

bool EchoClient::onSignal(int) {
    sendClose();
    return false;
}

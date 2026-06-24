#include "EchoClient.h"

EchoClient::EchoClient(web::websocket::SubProtocolContext* context, const std::string& name)
    : web::websocket::client::SubProtocol(context, name, 90, 3) {
}

void EchoClient::onConnected() {
    sendMessage("hello");
}

void EchoClient::onMessageStart(int) {
    currentMessage.clear();
}

void EchoClient::onMessageData(const char* chunk, std::size_t chunkLen) {
    currentMessage.append(chunk, chunkLen);
}

void EchoClient::onMessageEnd() {
    sendMessage(currentMessage);
    currentMessage.clear();
}

void EchoClient::onMessageError(uint16_t) {
    currentMessage.clear();
}

void EchoClient::onDisconnected() {
    currentMessage.clear();
}

bool EchoClient::onSignal(int) {
    sendClose();
    return false;
}

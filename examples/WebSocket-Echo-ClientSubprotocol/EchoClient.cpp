#include "EchoClient.h"

EchoClient::EchoClient(web::websocket::SubProtocolContext* context, const std::string& name)
    : web::websocket::client::SubProtocol(context, name, 90, 3) {
}

void EchoClient::onConnected() {
    sendMessage("hello");
}

void EchoClient::onMessageStart([[maybe_unused]] int opCode) {
    currentMessage.clear();
}

void EchoClient::onMessageData(const char* chunk, std::size_t chunkLen) {
    currentMessage.append(chunk, chunkLen);
}

void EchoClient::onMessageEnd() {
    sendMessage(currentMessage);
    currentMessage.clear();
}

void EchoClient::onMessageError([[maybe_unused]] uint16_t errnum) {
    currentMessage.clear();
}

void EchoClient::onDisconnected() {
    currentMessage.clear();
}

bool EchoClient::onSignal([[maybe_unused]] int sig) {
    sendClose();
    return false;
}

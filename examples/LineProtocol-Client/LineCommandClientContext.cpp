#include "LineCommandClientContext.h"

#include <core/socket/SocketAddress.h>
#include <core/socket/stream/SocketConnection.h>
#include <log/Logger.h>

#include <array>
#include <string>
#include <string_view>

namespace {

    constexpr std::array<std::string_view, 4> commandSequence{
        "PING\n",
        "STATUS\n",
        "UNKNOWN\n",
        "QUIT\n",
    };

    std::string printableCommand(std::string_view command) {
        if (!command.empty() && command.back() == '\n') {
            command.remove_suffix(1);
        }
        if (!command.empty() && command.back() == '\r') {
            command.remove_suffix(1);
        }

        return std::string(command);
    }

} // namespace

LineCommandClientContext::LineCommandClientContext(core::socket::stream::SocketConnection* socketConnection)
    : core::socket::stream::SocketContext(socketConnection) {
}

void LineCommandClientContext::onConnected() {
    VLOG(1) << "Line command client connected to " << getSocketConnection()->getRemoteAddress().toString();
}

void LineCommandClientContext::onDisconnected() {
    VLOG(1) << "Line command client disconnected from " << getSocketConnection()->getRemoteAddress().toString();
    receiveBuffer.clear();
}

bool LineCommandClientContext::onSignal(int signum) {
    VLOG(1) << "Line command client closing due to signal " << signum;
    close();

    return true;
}

std::size_t LineCommandClientContext::onReceivedFromPeer() {
    char chunk[1024];
    const std::size_t chunkLen = readFromPeer(chunk, sizeof(chunk));

    if (chunkLen == 0) {
        return 0;
    }

    receiveBuffer.append(chunk, chunkLen);

    std::size_t lineEnd = receiveBuffer.find('\n');
    while (lineEnd != std::string::npos) {
        std::string line = receiveBuffer.substr(0, lineEnd);
        if (!line.empty() && line.back() == '\r') {
            line.pop_back();
        }

        processLine(line);
        receiveBuffer.erase(0, lineEnd + 1);
        lineEnd = receiveBuffer.find('\n');
    }

    return chunkLen;
}

void LineCommandClientContext::processLine(const std::string& line) {
    VLOG(1) << "Line command client received '" << line << "'";

    if (line == "READY") {
        if (readyReceived) {
            LOG(WARNING) << "Line command client received duplicate READY greeting";
            close();
            return;
        }

        readyReceived = true;
        sendNextCommand();
        return;
    }

    if (!readyReceived) {
        LOG(WARNING) << "Line command client received protocol data before READY";
        close();
        return;
    }

    if (line == "PONG" || line == "OK" || line == "ERR unknown command") {
        sendNextCommand();
        return;
    }

    LOG(WARNING) << "Line command client received unexpected response '" << line << "'";
    close();
}

void LineCommandClientContext::sendNextCommand() {
    if (nextCommandIndex >= commandSequence.size()) {
        return;
    }

    const std::string_view command = commandSequence[nextCommandIndex++];
    VLOG(1) << "Line command client sending '" << printableCommand(command) << "'";
    sendToPeer(command.data(), command.length());

    if (command == "QUIT\n") {
        VLOG(1) << "Line command client waiting for server-side close";
    }
}

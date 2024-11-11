#include "exception.h"

Exception::Exception(int code, const std::string& message)
    : error_code_(code), error_message_(message) {}

int Exception::code() const noexcept {
    return error_code_;
}

const std::string& Exception::message() const noexcept {
    return error_message_;
}

const char* Exception::what() const noexcept {
    what_buffer_ = "Error " + std::to_string(error_code_) + ": " + error_message_;
    return what_buffer_.c_str();
}

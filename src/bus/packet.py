from base64 import b64decode, b64encode
from json import dumps, loads


class Packet:
    def __init__(self, body, *, code="OK", data_type="JSON", request_type="Update", **headers):
        assert type(data_type) == str, "Data-Type must be string"
        assert data_type in ("JSON", "Binary", "Plain"), "Invalid Data-Type"
        assert request_type in ["Update", "Handshake",
                                "Retrieve"], "Invalid Request-Type"

        assert type(code) == str, "code must be string"

        for k, v in headers.items():
            assert type(k) == str, "Key of header must be string"
            assert type(v) == str, "Value of header must be string"

        self.headers = {
            "Code": code,
            "Data-Type": data_type
        }

        self.headers.update(headers)
        self.body = body

    def encode(self):
        # Encodes headers with updated k, v pairs
        encoded_headers = b"\n".join(f"{k}: {v}".encode("utf-8") for k, v in
                                     self.headers.items()) + b"\n\n"

        encoded_body = bytes()
        if self.data_type == "JSON":
            dump = None

            try:
                dump = dumps(self.body)

            except ValueError:
                raise ValueError("Invalid dictionary for body")

            except TypeError:
                raise TypeError("Type of body must be dictionary")

            encoded_body = b64encode(dump)

        elif self.data_type in ["Binary", "Plain"]:
            encoded_body = b64encode(self.body)

        encoded_message = encoded_headers + encoded_body
        return encoded_message

    @staticmethod
    def decode(encoded_packet):
        pass  # TODO: This

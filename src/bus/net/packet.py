from base64 import b64decode, b64encode, encode
from json import dumps, loads


class Packet:
    def __init__(self, body, *, code="OK", data_type="JSON", request_type="Update", **headers):
        assert type(data_type) == str, "Data-Type must be string"
        assert data_type.upper() in ("JSON", "BINARY", "PLAIN"), "Invalid Data-Type"
        assert type(request_type) == str, "Request-Type must be of type string"

        assert type(code) == str, "code must be string"

        for k, v in headers.items():
            assert type(k) == str, "Key of header must be string"
            assert type(v) == str, "Value of header must be string"

        self.headers = {
            "Code": code,
            "Data-Type": data_type,
            "Request-Type": request_type
        }

        self.headers.update(headers)
        self.body = body

    def encode(self):
        # Encodes headers with updated k, v pairs
        encoded_headers = b"\n".join("{}: {}".format(k, v).encode("utf-8") for k, v in
                                     self.headers.items()) + b"\n\n"

        encoded_body = bytes()
        if self.headers["Data-Type"] == "JSON":
            dump = None

            try:
                dump = dumps(self.body)

            except ValueError:
                raise ValueError("Invalid dictionary for body")

            except TypeError:
                raise TypeError("Type of body must be dictionary")

            encoded_body = b64encode(dump.encode("utf-8"))

        elif self.headers["Data-Type"] in ["Binary", "Plain"]:
            encoded_body = str(b64encode(self.body)).encode("utf-8")

        encoded_message = encoded_headers + encoded_body
        return encoded_message

    @staticmethod
    def decode(encoded_packet):
        headers, encoded_body = encoded_packet.decode("utf-8").split("\n\n")

        body = b64decode(encoded_body)
        body_data = None

        header_dict = {}
        for ln in headers.split("\n"):
            k, v = ln.split(": ")

            header_dict[k] = v

        data_type = header_dict.get("Data-Type", "Null").upper()
        code = header_dict.get("Code", "Null").upper()
        request_type = header_dict.get("Request-Type", "Null")

        if data_type == "JSON":
            body_data = loads(body.decode("utf-8"))

        elif data_type in ["BINARY", "PLAIN"]:
            body_data = body

        custom_headers = {header: value for header, value in header_dict.items() if header.upper(
        ) not in ["DATA-TYPE", "REQUEST-TYPE", "CODE"]}

        return Packet(body_data, code=code, data_type=data_type, request_type=request_type, **custom_headers)

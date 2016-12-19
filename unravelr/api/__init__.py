from .disassembler import Disassembler


def init_api(api_extension):
    api_extension.add_resource(Disassembler, "/api/disassembler")

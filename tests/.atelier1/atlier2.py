import mcp3008

with mcp3008.MCP3008() as adc:
    print(adc.read([mcp3008.CH0])) # prints raw data [CH0]
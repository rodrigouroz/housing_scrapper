import os

def run_debugger():
  import debugpy
  # 5678 is the default attach port in the VS Code debug configurations. Unless a host and port are specified, host defaults to 127.0.0.1
  debugpy.listen(5678)
  print("Waiting for debugger attach")
  debugpy.wait_for_client()
  debugpy.breakpoint()
  print('break on this line')

if (os.environ.get('ENABLE_DEBUGGER')):
  run_debugger()

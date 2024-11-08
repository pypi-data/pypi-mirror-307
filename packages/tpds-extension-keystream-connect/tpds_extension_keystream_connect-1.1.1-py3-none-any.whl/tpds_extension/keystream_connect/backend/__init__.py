import os
from tpds.devices import TpdsBoards, TpdsDevices


# Add the Board information
TpdsBoards().add_board_info(os.path.join(os.path.dirname(__file__), 'boards'))

# Add the Part information
TpdsDevices().add_device_info(os.path.join(os.path.dirname(__file__), 'parts'))

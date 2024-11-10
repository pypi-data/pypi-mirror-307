# Copyright 2024 CrackNuts. All rights reserved.

import pathlib
from typing import Any

from cracknuts_panel.acquisition_panel import AcquisitionPanelWidget
from cracknuts_panel.cracker_panel import CrackerPanelWidget
from cracknuts_panel.panel import MsgHandlerPanelWidget
from cracknuts_panel.trace_panel import TraceMonitorPanelWidget


class CracknutsPanelWidget(CrackerPanelWidget, AcquisitionPanelWidget, TraceMonitorPanelWidget, MsgHandlerPanelWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "CrackNutsPanelWidget.js"
    _css = ""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if "acquisition" not in kwargs:
            raise ValueError("acquisition must be provided")
        kwargs["cracker"] = kwargs["acquisition"].cracker
        super().__init__(*args, **kwargs)

    def sync_config(self) -> None:
        CrackerPanelWidget.sync_config(self)
        AcquisitionPanelWidget.sync_config(self)

    def bind(self) -> None:
        CrackerPanelWidget.bind(self)
        AcquisitionPanelWidget.bind(self)

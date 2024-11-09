from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import wx

from .glyphMetricPanelUI import GlyphMetricPanelUI

if TYPE_CHECKING:
    from wbDefcon import Glyph

    from .editPanel import GlyphEditPanel


class GlyphMetricPanel(GlyphMetricPanelUI):
    refreshNotifications = (
        "Glyph.WidthChanged",
        "Glyph.LeftMarginDidChange",
        "Glyph.RightMarginDidChange",
        "Glyph.ContoursChanged",
        "Glyph.ComponentsChanged",
        "Glyph.ComponentBaseGlyphDataChanged",
    )

    def __init__(
        self,
        parent: GlyphEditPanel,
        id: int = wx.ID_ANY,
        pos: wx.Position = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.BORDER_NONE | wx.TAB_TRAVERSAL,
        name: str = "GlyphMetricPanel",
    ):
        self._glyph: Optional[Glyph] = None
        super().__init__(parent, id=id, pos=pos, size=size, style=style, name=name)

    @property
    def glyph(self) -> Optional[Glyph]:
        return self._glyph

    @glyph.setter
    def glyph(self, value: Glyph):
        if self._glyph == value:
            return
        del self.glyph
        self._glyph = value
        for layer in self._glyph.layerSet:
            for notificationName in self.refreshNotifications:
                if self._glyph.name in layer and not layer[
                    self._glyph.name
                ].hasObserver(self, notificationName):
                    layer[self._glyph.name].addObserver(
                        self, "handleNotification", notificationName
                    )
        self._setControlValues()
        self.Refresh()

    @glyph.deleter
    def glyph(self):
        if self._glyph is None:
            return
        for layer in self._glyph.layerSet:
            for notificationName in self.refreshNotifications:
                if self._glyph.name in layer and layer[self._glyph.name].hasObserver(
                    self, notificationName
                ):
                    layer[self._glyph.name].removeObserver(self, notificationName)
        self._glyph = None
        self.Refresh()

    def _setControlValues(self):
        if self._glyph is None:
            return
        try:
            if self._glyph.leftMargin is not None:
                self.spinCtrlDouble_LSB.Value = self._glyph.leftMargin
            self.spinCtrlDouble_width.Value = self._glyph.width
            if self._glyph.rightMargin is not None:
                self.spinCtrlDouble_RSB.Value = self._glyph.rightMargin
        except RuntimeError:
            pass

    def handleNotification(self, notification):
        self._setControlValues()

    # event handlers

    def on_spinCtrlDouble_LSB(self, event: wx.SpinDoubleEvent):
        glyph = self._glyph
        dx = event.Value - glyph.leftMargin
        if not dx:
            return
        glyph.moveBy((dx, 0))
        font = glyph.font
        for glyphName in font.componentReferences.get(glyph.name, ()):
            if glyphName in font:
                compositeGlyph = glyph.font[glyphName]
                for component in compositeGlyph.components:
                    if component.baseGlyph == glyph.name:
                        component.moveBy((-dx, 0))

    def onUpdate_spinCtrlDouble_LSB(self, event: wx.UpdateUIEvent):
        if self._glyph is None or self._glyph.leftMargin is None:
            self.spinCtrlDouble_LSB.Value = 0
            event.Enable(False)
            return
        event.Enable(True)

    def on_spinCtrlDouble_width(self, event: wx.SpinDoubleEvent):
        self._glyph.width = event.Value

    def onUpdate_spinCtrlDouble_width(self, event: wx.UpdateUIEvent):
        if self.glyph is None:
            self.spinCtrlDouble_width.Value = 0
            event.Enable(False)
            return
        event.Enable(True)

    def on_spinCtrlDouble_RSB(self, event: wx.SpinDoubleEvent):
        self._glyph.rightMargin = event.Value

    def onUpdate_spinCtrlDouble_RSB(self, event: wx.UpdateUIEvent):
        if self._glyph is None or self._glyph.rightMargin is None:
            self.spinCtrlDouble_RSB.Value = 0
            event.Enable(False)
            return
        event.Enable(True)

    def Destroy(self):
        del self.glyph
        return super().Destroy()

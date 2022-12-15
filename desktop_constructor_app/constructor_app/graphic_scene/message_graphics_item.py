import typing

import PySide6
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QPointF, QRectF, Signal, QResource, QObject
from PySide6.QtGui import QBrush, QColor, QPen, QLinearGradient
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QGraphicsItem, QGraphicsObject

from b_logic.data_objects import BotMessage, BotVariant


class MessageGraphicsSignalSender(QObject):
    # в списке передаются варианты сообщения
    add_variant_request = Signal(BotMessage, list)

    # пользователь запросил изменение сообщения
    # (в списке передаются варианты сообщения BotVariant)
    request_change_message = Signal(BotMessage, list)

    request_change_variant = Signal(BotVariant)


class MessageGraphicsItem(QGraphicsItem):
    """
    Объект графической сцены Блок.
    Состоит из сообщений и принадлежащих ему Вариантов
    """

    _MSG_WIDTH = 150
    _MSG_HEIGHT = 100

    _VARIANT_WIDTH = 150
    _VARIANT_HEIGHT = 50

    _MESSAGE_COLOR = 0xceffff
    _TEXT_COLOR = 0x154545
    _PEN_COLOR = 0x137b7b

    _BORDER_THICKNESS_NORMAL = 2
    _BORDER_THICKNESS_SELECTED = 3

    _ROUND_RADIUS = 30
    _VARIANT_BACKGROUND = 0x9edee6
    _SELECTED_VARIANT_BACKGROUND = 0x84d2dc
    _BLOCK_RECT_EXTEND_SPACE = 25
    _MESSAGE_TEXT_BORDER = 25
    _VARIANT_TEXT_BORDER = 5
    _BOUNDING_RECT_SPARE_PAINTING_DISTANCE = 2
    _VARIANT_DISTANCE = 25
    _VARIANT_ICON_RECT_BORDER = 10

    def __init__(self, message: BotMessage, variants: typing.List[BotVariant]):
        super().__init__()
        assert isinstance(message, BotMessage)
        assert all(isinstance(variant, BotVariant) for variant in variants)

        self.signal_sender: MessageGraphicsSignalSender = MessageGraphicsSignalSender()

        self._brush = QBrush(QColor(self._MESSAGE_COLOR))

        self._normal_pen = QPen(
            QColor(self._PEN_COLOR),
            self._BORDER_THICKNESS_NORMAL,
            QtCore.Qt.PenStyle.SolidLine)

        self._selected_pen = QPen(
            QColor(self._PEN_COLOR),
            self._BORDER_THICKNESS_SELECTED,
            QtCore.Qt.PenStyle.SolidLine)

        for pen in (self._selected_pen, self._normal_pen):
            pen.setJoinStyle(QtCore.Qt.PenJoinStyle.RoundJoin)

        self._message: BotMessage = message

        self._variants = variants

        self._current_variant_index: typing.Optional[int] = None

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)

        self.setPos(QPointF(self._message.x, self._message.y))

    def get_message(self) -> BotMessage:
        return self._message

    def boundingRect(self) -> QRectF:
        rect = self._block_rect()
        x = rect.x() - self._BOUNDING_RECT_SPARE_PAINTING_DISTANCE
        y = rect.y() - self._BOUNDING_RECT_SPARE_PAINTING_DISTANCE
        width = rect.width() + self._BOUNDING_RECT_SPARE_PAINTING_DISTANCE * 2
        height = rect.height() + self._BOUNDING_RECT_SPARE_PAINTING_DISTANCE * 2
        return QRectF(x, y, width, height)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: typing.Any) -> typing.Any:
        result = super().itemChange(change, value)
        # синхронизируем позицию графического элемента и координаты сообщения
        if change == QGraphicsItem.ItemPositionChange:
            assert isinstance(value, QPointF)
            new_position = value
            self._message.x = int(new_position.x())
            self._message.y = int(new_position.y())

        return result

    def paint(
            self,
            painter: QtGui.QPainter,
            option: QtWidgets.QStyleOptionGraphicsItem,
            widget: typing.Optional[QtWidgets.QWidget]):
        assert isinstance(painter, QtGui.QPainter)
        assert isinstance(option, QtWidgets.QStyleOptionGraphicsItem)
        assert isinstance(widget, QtWidgets.QWidget) or widget is None

        print('we paint')

        self._draw_block(painter)

        self._draw_message(painter)

        for variant_index, variant in enumerate(self._variants):
            self._draw_variant(painter, variant, variant_index)

        illusory_variant_index = len(self._variants)

        self._draw_variant(painter, None, illusory_variant_index)

    def mousePressEvent(self, event: PySide6.QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            click_position: QPointF = event.pos()
            variant_on_position = self._variant_by_position(click_position)
            if variant_on_position is not None:
                self._current_variant_index = self._variants.index(variant_on_position)
            else:
                self._current_variant_index = None
            self._update_image()

        print(f'current variant index {self._current_variant_index}')
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        illusory_variant_index = len(self._variants)
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            click_position: QPointF = event.pos()

            add_variant_rect = self._variant_rect(illusory_variant_index)
            message_rect = self._message_rect()

            variant_on_position = self._variant_by_position(click_position)

            if add_variant_rect.contains(click_position):
                self.signal_sender.add_variant_request.emit(self._message, self._variants)
            elif message_rect.contains(click_position):
                self.signal_sender.request_change_message.emit(self._message, self._variants)
            elif variant_on_position is not None:
                self.signal_sender.request_change_variant.emit(variant_on_position)

        super().mouseDoubleClickEvent(event)

    def get_current_variant(self) -> typing.Optional[BotVariant]:
        """
        Получить текущий выбранный вариант.
        Вариант может быть выбран только тогда, когда выбран блок
        Returns:
            Объект выбранного варианта или None, если вариант не выбран
        """
        variant: typing.Optional[BotVariant] = None
        # понятие "текущий вариант" имеет смысл только тогда, когда текущий блок выделен
        if self._current_variant_index is not None and self.isSelected():
            variant = self._variants[self._current_variant_index]
        return variant

    def delete_variant(self, variant_id: int) -> None:
        big_bounding_rect = self.boundingRect()
        big_scene_bounding_rect = self.sceneBoundingRect()
        self.update(big_bounding_rect)
        searched_var = None
        for variant in self._variants:
            if variant.id == variant_id:
                searched_var = variant
                break
        self._variants.remove(searched_var)
        # self._variants = [variant for variant in self._variants if variant.id != variant_id]
        # self._current_variant_index = None
        self.scene().update(big_scene_bounding_rect)
        # print('big bounding rect ', big_bounding_rect)
        print('update after delete')
        self.update(big_bounding_rect)

    def _update_image(self) -> None:
        """
        Перерисовать блок. Нужно вызывать этот метод, когда визуальное отображение блока меняется,
        чтобы избежать артефактов рисования
        """
        self.update(self.boundingRect())

    def _variant_by_position(self, position: QPointF) -> typing.Optional[BotVariant]:
        variant_on_position: typing.Optional[BotVariant] = None
        for variant_index, variant in enumerate(self._variants):
            if self._variant_rect(variant_index).contains(position):
                variant_on_position = variant

        return variant_on_position

    def _draw_block(self, painter: QtGui.QPainter):
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(self._get_block_brush())
        painter.drawRoundedRect(self._block_rect(), 30, 30)

    def _draw_message(self, painter: QtGui.QPainter):
        self._setup_message_colors(painter)

        painter.drawRoundedRect(self._message_rect(), self._ROUND_RADIUS, self._ROUND_RADIUS)

        self._setup_text_color(painter)

        painter.drawText(self._message_text_rect(), self._message.text)

    def _draw_variant(self, painter: QtGui.QPainter, variant: typing.Optional[BotVariant], index: int):
        assert isinstance(painter, QtGui.QPainter)
        assert isinstance(variant, BotVariant) or variant is None
        assert isinstance(index, int)

        illusory_variant = variant is None

        self._setup_variant_colors(painter, index, illusory_variant)

        painter.drawRect(self._variant_rect(index))

        if not illusory_variant:
            painter.setPen(QColor(self._TEXT_COLOR))
            painter.drawText(self._variant_text_rect(index), variant.text)
        else:
            # отображается несуществующий вариант, который позволяет добавлять новые варианты
            add_variant_icon_render = QSvgRenderer(':/icons/images/add_variant.svg')
            add_variant_icon_render.setAspectRatioMode(QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            add_variant_icon_render.render(painter, self._variant_icon_rect(index))

    def _get_plus_variant_rect(self, variant_index: int):
        variant_rect = self._variant_rect(variant_index)
        height = variant_rect.height()
        variant_rect.x() + variant_rect.width() / 2.0 - height

    def _get_block_brush(self) -> QBrush:
        alpha_top_left = 180
        alpha_right_bottom = 50
        if self.isSelected():
            alpha_top_left = 230
            alpha_right_bottom = 230

        gradient = QLinearGradient(0, 0, 100, 100)

        block_brush_color_top_left = QColor(0xb4e6ce)
        block_brush_color_top_left.setAlpha(alpha_top_left)

        block_brush_color_right_bottom = QColor(0xaef7d5)
        block_brush_color_right_bottom.setAlpha(alpha_right_bottom)

        gradient.setColorAt(0.0, block_brush_color_top_left)
        gradient.setColorAt(1.0, block_brush_color_right_bottom)
        block_brush = QBrush(gradient)
        return block_brush

    def _setup_message_colors(self, painter: QtGui.QPainter):
        painter.setBrush(self._brush)
        if self.isSelected():
            painter.setPen(self._selected_pen)
        else:
            painter.setPen(self._normal_pen)

    def _setup_variant_colors(
            self,
            painter: QtGui.QPainter,
            painted_variant_index: typing.Optional[int],
            is_illusory_variant: bool
    ):
        assert isinstance(painter, QtGui.QPainter)
        assert isinstance(painted_variant_index, typing.Optional[int])
        assert isinstance(is_illusory_variant, bool)
        if not is_illusory_variant:
            # понятие "текущий вариант" имеет смысл только тогда, когда текущий блок выделен
            if self.isSelected() and painted_variant_index == self._current_variant_index:
                painter.setBrush(QColor(self._SELECTED_VARIANT_BACKGROUND))
                painter.setPen(self._selected_pen)
            else:
                painter.setBrush(QColor(self._VARIANT_BACKGROUND))
                painter.setPen(self._normal_pen)
        else:
            painter.setBrush(QColor(self._VARIANT_BACKGROUND))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)

    def _setup_text_color(self, painter: QtGui.QPainter):
        painter.setPen(QColor(self._TEXT_COLOR))

    def _variant_rect(self, variant_index: int) -> QRectF:
        dy = self._VARIANT_HEIGHT + self._VARIANT_DISTANCE
        return QRectF(
            0,
            self._MSG_HEIGHT + self._VARIANT_DISTANCE + dy * variant_index,
            self._VARIANT_WIDTH,
            self._VARIANT_HEIGHT)

    def _variant_text_rect(self, variant_index: int) -> QRectF:
        variant_rect = self._variant_rect(variant_index)
        return QRectF(
            variant_rect.x() + self._VARIANT_TEXT_BORDER,
            variant_rect.y() + self._VARIANT_TEXT_BORDER,
            variant_rect.width() - self._VARIANT_TEXT_BORDER * 2,
            variant_rect.height() - self._VARIANT_TEXT_BORDER * 2
        )

    def _variant_icon_rect(self, variant_index: int) -> QRectF:
        variant_rect = self._variant_rect(variant_index)

        return QRectF(
            variant_rect.x() + self._VARIANT_ICON_RECT_BORDER,
            variant_rect.y() + self._VARIANT_ICON_RECT_BORDER,
            variant_rect.width() - self._VARIANT_ICON_RECT_BORDER * 2,
            variant_rect.height() - self._VARIANT_ICON_RECT_BORDER * 2
        )

    def _message_rect(self) -> QRectF:
        return QRectF(0, 0, self._MSG_WIDTH, self._MSG_HEIGHT)

    def _message_text_rect(self) -> QRectF:
        return QRectF(
            self._MESSAGE_TEXT_BORDER,
            self._MESSAGE_TEXT_BORDER,
            self._MSG_WIDTH - self._MESSAGE_TEXT_BORDER * 2,
            self._MSG_HEIGHT - self._MESSAGE_TEXT_BORDER * 2
        )

    def _block_rect(self) -> QRectF:
        rect = self._message_rect()
        # обычные варианты + иллюзорный вариант (через который добавляются новые варианты)
        for variant_index in range(len(self._variants) + 1):
            rect = rect.united(self._variant_rect(variant_index))

        x = rect.x() - self._BLOCK_RECT_EXTEND_SPACE
        y = rect.y() - self._BLOCK_RECT_EXTEND_SPACE
        width = rect.width() + 2 * self._BLOCK_RECT_EXTEND_SPACE
        height = rect.height() + 2 * self._BLOCK_RECT_EXTEND_SPACE
        return QRectF(x, y, width, height)

import typing
from dataclasses import dataclass

import PySide6
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QPointF, QRectF, Signal, QResource, QObject
from PySide6.QtGui import QBrush, QColor, QPen, QLinearGradient
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QGraphicsItem, QGraphicsObject

from b_logic.data_objects import BotMessage, BotVariant


class BlockGraphicsSignalSender(QObject):
    # в списке передаются варианты сообщения
    add_variant_request = Signal(BotMessage, list)

    # пользователь запросил изменение сообщения
    # (в списке передаются варианты сообщения BotVariant)
    request_change_message = Signal(BotMessage, list)

    request_change_variant = Signal(BotVariant)


@dataclass(slots=True, frozen=True)
class BlockColorScheme:
    message_color = 0xceffff
    text_color = 0x154545
    pen_color = 0x137b7b

    variant_background = 0x9edee6
    selected_variant_background = 0x84d2dc


class BlockGraphicsItem(QGraphicsItem):
    """
    Объект графической сцены Блок.
    Состоит из Сообщений и принадлежащих ему Вариантов
    """

    _MSG_WIDTH = 150
    _MSG_HEIGHT = 100

    _VARIANT_WIDTH = 150
    _VARIANT_HEIGHT = 50

    _BORDER_THICKNESS_NORMAL = 2
    _BORDER_THICKNESS_SELECTED = 3

    _ROUND_RADIUS = 30
    _BLOCK_RECT_EXTEND_SPACE = 25
    _MESSAGE_TEXT_BORDER = 25
    _VARIANT_TEXT_BORDER = 5
    _BOUNDING_RECT_SPARE_PAINTING_DISTANCE = 2
    _VARIANT_DISTANCE = 25
    _VARIANT_ICON_RECT_BORDER = 10

    def __init__(self, message: BotMessage, variants: typing.List[BotVariant]):
        """
        Конструктор блока. Блок возьмет свои координаты из координат сообщения
        Args:
            message: сообщение блока
            variants: варианты блока
        """
        super().__init__()
        assert isinstance(message, BotMessage)
        assert all(isinstance(variant, BotVariant) for variant in variants)

        self.signal_sender: BlockGraphicsSignalSender = BlockGraphicsSignalSender()

        self._color_scheme = BlockColorScheme()

        # кисточка (заливка) для рисования сообщений
        self._message_brush = QBrush(QColor(self._color_scheme.message_color))

        # карандаш (контур) для рисования сообщений и вариантов, если они не выделены
        self._normal_pen = QPen(
            QColor(self._color_scheme.pen_color),
            self._BORDER_THICKNESS_NORMAL,
            QtCore.Qt.PenStyle.SolidLine)

        # карандаш (контур) для рисования сообщений и вариантов, если они выделены
        self._selected_pen = QPen(
            QColor(self._color_scheme.pen_color),
            self._BORDER_THICKNESS_SELECTED,
            QtCore.Qt.PenStyle.SolidLine)

        for pen in (self._selected_pen, self._normal_pen):
            pen.setJoinStyle(QtCore.Qt.PenJoinStyle.RoundJoin)

        # сообщение блока
        self._message: BotMessage = message

        # варианты блока
        self._variants: typing.List[BotVariant] = variants

        # индекс выделенного варианта
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

        # нарисовать сам блок
        self._draw_block(painter)

        # нарисовать сообщение
        self._draw_message(painter)

        # нарисовать все обычные варианты
        for variant_index, variant in enumerate(self._variants):
            self._draw_variant(painter, variant, variant_index)

        # нарисовать иллюзорный вариант, через который происходит добавление других вариантов
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
        """
        Удаляет из блока вариант с указанным индексом
        Args:
            variant_id: индекс удаляемого варианта
        """

        big_bounding_rect = self.boundingRect()
        big_scene_bounding_rect = self.sceneBoundingRect()
        self.update(big_bounding_rect)
        self.prepareGeometryChange()

        self._remove_variant_from_list(variant_id)

        # после удаления варианта из списка индекс текущего варианта мог
        # начать указывать на несуществующий вариант
        self._fix_current_variant_index()

        self.scene().update(big_scene_bounding_rect)

        self.update(big_bounding_rect)

    def _remove_variant_from_list(self, variant_id: int) -> None:
        assert isinstance(variant_id, int)
        searched_var: typing.Optional[BotVariant] = None
        for variant in self._variants:
            if variant.id == variant_id:
                searched_var = variant
                break
        if searched_var is not None:
            self._variants.remove(searched_var)
        else:
            print('Try remove not exists variant')

    def _fix_current_variant_index(self) -> None:
        """
        Поправляет текущий вариант, если вдруг индекс текущего варианта перестанет
        существовать (после удаления варианта)
        """
        if self._current_variant_index is not None:
            variants_number = len(self._variants)
            if self._current_variant_index >= variants_number:
                if variants_number > 0:
                    self._current_variant_index = variants_number - 1
                else:
                    self._current_variant_index = None

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
        painter.drawRoundedRect(self._block_rect(), self._ROUND_RADIUS, self._ROUND_RADIUS)

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
            painter.setPen(QColor(self._color_scheme.text_color))
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
        painter.setBrush(self._message_brush)
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
                painter.setBrush(QColor(self._color_scheme.selected_variant_background))
                painter.setPen(self._selected_pen)
            else:
                painter.setBrush(QColor(self._color_scheme.variant_background))
                painter.setPen(self._normal_pen)
        else:
            painter.setBrush(QColor(self._color_scheme.variant_background))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)

    def _setup_text_color(self, painter: QtGui.QPainter):
        painter.setPen(QColor(self._color_scheme.text_color))

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

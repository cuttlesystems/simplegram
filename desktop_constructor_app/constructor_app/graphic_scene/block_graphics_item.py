import typing

import PySide6
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QPointF, QRectF, Signal, QObject
from PySide6.QtGui import QBrush, QColor, QPen, QLinearGradient
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QGraphicsItem

from b_logic.data_objects import BotMessage, BotVariant, BotDescription
from desktop_constructor_app.constructor_app.graphic_scene.colors.block_color_scheme import BlockColorScheme
from utils.cut_string import cut_string


class BlockGraphicsSignalSender(QObject):
    """
    Класс для описания сигналов, которые отправляет
    графический Блок
    """

    # в списке передаются варианты сообщения
    # Параметры: (объект сообщения, список вариантов сообщения)
    add_variant_request = Signal(BotMessage, list)

    # пользователь запросил изменение сообщения
    # Параметры: (объект блока, в списке передаются варианты сообщения BotVariant)
    request_change_message = Signal(object, list)

    # пользователь запросил изменение варианта
    # Параметры: (объект блока, объект варианта)
    request_change_variant = Signal(object, BotVariant)

    # поменялся (мог поменяться) выделенный объект блока
    selected_item_changed = Signal()


class BlockGraphicsItem(QGraphicsItem):
    """
    Объект графической сцены Блок.
    Состоит из Сообщений и принадлежащих ему Вариантов
    """
    _MAX_MESSAGE_CHARS = 25
    _MAX_VARIANT_CHARS = 25

    _MESSAGE_WIDTH = 150
    _MESSAGE_HEIGHT = 100

    _VARIANT_WIDTH = 150
    _VARIANT_HEIGHT = 50

    _START_MESSAGE_TITLE_WIDTH = 150
    _START_MESSAGE_TITLE_HEIGHT = 20

    _BORDER_THICKNESS_NORMAL = 2
    _BORDER_THICKNESS_SELECTED = 3

    _ROUND_RADIUS = 30
    _BLOCK_RECT_EXTEND_SPACE = 25
    _MESSAGE_TEXT_BORDER = 25
    _VARIANT_TEXT_BORDER = 5
    _BOUNDING_RECT_SPARE_PAINTING_DISTANCE = 2
    _VARIANT_DISTANCE = 25
    _VARIANT_ICON_RECT_BORDER = 10
    _START_MESSAGE_TITLE_BORDER_X = 25
    _START_MESSAGE_TITLE_BORDER_Y = -20

    def __init__(self, message: BotMessage, variants: typing.List[BotVariant], start_message_id: int = None):
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

        # кисточка (заливка) для первого сообщения
        self._start_message_brush = QBrush(QColor(self._color_scheme.start_message_color))

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

        # id стартового сообщения
        self._start_message_id = start_message_id

        # варианты блока
        self._variants: typing.List[BotVariant] = variants

        # индекс выделенного варианта
        self._current_variant_index: typing.Optional[int] = None

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)

        # установим положение блока на сцене исходя из положения сообщения
        self.setPos(QPointF(self._message.x, self._message.y))

    def _is_message_started(self) -> bool:
        """
        Определяет, является ли сообщение стартовым.

        Returns:
            Boolean, является ли сообщение стартовым.
        """
        return self._message.id == self._start_message_id

    def set_started_state(self, started: bool):
        pass
        # todo: перерисовка

    def get_message(self) -> BotMessage:
        return self._message

    def boundingRect(self) -> QRectF:
        """
        Внешняя область фигуры. Используется Qt для рисования. Рисовать блок можно только внутри этих координат.
        Если область рисования не соответствует области возвращаемой этой функцией,
        то будут появляться артефакты рисования.
        Returns:
            координаты внешней области фигуры
        """
        rect = self._block_rect()
        x = rect.x() - self._BOUNDING_RECT_SPARE_PAINTING_DISTANCE
        y = rect.y() - self._BOUNDING_RECT_SPARE_PAINTING_DISTANCE
        width = rect.width() + self._BOUNDING_RECT_SPARE_PAINTING_DISTANCE * 2
        height = rect.height() + self._BOUNDING_RECT_SPARE_PAINTING_DISTANCE * 2
        return QRectF(x, y, width, height)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: typing.Any) -> typing.Any:
        """
        Метод, который позволяет встраиваться в процесс изменения графического элемента (данного блока).
        Args:
            change: производимое изменение (перечисление)
            value: значение, которое меняется

        Returns:
            значение, полученное от базового класса
        """
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
            widget: typing.Optional[QtWidgets.QWidget]) -> None:
        """
        Метод рисования. В этом методе мы самостоятельно реализуем рисование блока.
        Args:
            painter: объект с помощью которого производится рисование
            option: не используется в данном случае
            widget: не используется в данном случае
        """
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
        """
        Метод, вызываемый при клике по блоку
        Args:
            event: параметры события
        """
        if event.button() in (QtCore.Qt.MouseButton.LeftButton, QtCore.Qt.MouseButton.RightButton):
            click_position: QPointF = event.pos()
            # определим какому варианту соответствуют координаты клика
            variant_on_position = self._variant_by_position(click_position)
            # установим текущий вариант на тот, на который кликнули (если клик произведен по варианту),
            # либо сбросим текущий вариант, если клик в другом месте
            if variant_on_position is not None:
                self._current_variant_index = self._variants.index(variant_on_position)
            else:
                self._current_variant_index = None
            self._update_image()
            self.signal_sender.selected_item_changed.emit()

        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        """
        Метод, вызываемый при двойном клике по блоку
        Args:
            event: параметры события
        """
        illusory_variant_index = len(self._variants)
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            click_position: QPointF = event.pos()

            add_variant_rect = self._variant_rect(illusory_variant_index)
            message_rect = self._message_rect()

            variant_on_position = self._variant_by_position(click_position)

            # клик по кнопке добавления нового варианта
            if add_variant_rect.contains(click_position):
                self.signal_sender.add_variant_request.emit(self._message, self._variants)
            # клик по сообщению
            elif message_rect.contains(click_position):
                self.signal_sender.request_change_message.emit(self, self._variants)
            # клик по какому-то определенному варианту
            elif variant_on_position is not None:
                self.signal_sender.request_change_variant.emit(self, variant_on_position)

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

    def get_variants(self) -> typing.List[BotVariant]:
        """
        Получить варианты, относящиеся к данному блоку (к сообщению данного блока)
        Returns:
            список объектов вариантов
        """
        return self._variants

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

    def change_message(self, message: BotMessage) -> None:
        """
        Вызывается, если поменялось сообщение, связанное с блоком
        Args:
            message: новое измененное сообщение
        """
        assert isinstance(message, BotMessage)
        self.prepareGeometryChange()
        self._message = message
        self.update(self.boundingRect())

    def add_variant(self, variant: BotVariant) -> None:
        """
        Добавить вариант в данный блок. Происходит визуальное добавление
        нового варианта на графический блок.
        Args:
            variant: объект добавляемого варианта
        """
        assert isinstance(variant, BotVariant)
        self.prepareGeometryChange()
        self._variants.append(variant)
        self._update_image()

    def change_variant(self, variant: BotVariant) -> None:
        """
        Изменить данные заданного варианта. По id сопоставит вариант и заменит его
        Args:
            variant: вариант, который изменился
        """
        assert isinstance(variant, BotVariant)
        internal_variant = self._find_variant_object(variant.id)
        self.prepareGeometryChange()
        if internal_variant is not None:
            # todo: класс для копирования вариантов (или переделать другим способом)
            internal_variant.text = variant.text
            internal_variant.current_message_id = variant.current_message_id
            internal_variant.next_message_id = variant.next_message_id
        else:
            print('Can not find variant')
        self.update(self.boundingRect())

    def _remove_variant_from_list(self, variant_id: int) -> None:
        variant = self._find_variant_object(variant_id)
        if variant is not None:
            self._variants.remove(variant)
        else:
            print('Try remove not exists variant')

    def _find_variant_object(self, variant_id: int) -> typing.Optional[BotVariant]:
        assert isinstance(variant_id, int)
        searched_var: typing.Optional[BotVariant] = None
        for variant in self._variants:
            if variant.id == variant_id:
                searched_var = variant
                break
        return searched_var

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
        чтобы избежать артефактов рисования.
        Еще не вызов этого метода при изменении изображения может в некоторых случаях приводить к
        падению приложения.
        """
        self.update(self.boundingRect())
        self.scene().update(self.sceneBoundingRect())

    def _variant_by_position(self, position: QPointF) -> typing.Optional[BotVariant]:
        variant_on_position: typing.Optional[BotVariant] = None
        for variant_index, variant in enumerate(self._variants):
            if self._variant_rect(variant_index).contains(position):
                variant_on_position = variant

        return variant_on_position

    def _draw_block(self, painter: QtGui.QPainter) -> None:
        """
        Метод для рисования только блока
        Args:
            painter: объект для рисования
        """
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(self._get_block_brush())
        painter.drawRoundedRect(self._block_rect(), self._ROUND_RADIUS, self._ROUND_RADIUS)

    def _draw_message(self, painter: QtGui.QPainter) -> None:
        # настроим цвета кисточки и заливки и нарисуем сообщение
        self._setup_message_colors(painter)
        painter.drawRoundedRect(self._message_rect(), self._ROUND_RADIUS, self._ROUND_RADIUS)

        # настроим цвет текста и напишем текст сообщения
        self._setup_text_color(painter)
        painter.drawText(self._message_text_rect(), cut_string(self._message.text, self._MAX_MESSAGE_CHARS))

        if self._is_message_started():
            painter.drawText(self._start_message_title_block_rect(), 'Start message')

    def _draw_variant(self, painter: QtGui.QPainter, variant: typing.Optional[BotVariant], index: int):
        assert isinstance(painter, QtGui.QPainter)
        assert isinstance(variant, BotVariant) or variant is None
        assert isinstance(index, int)

        is_illusory_variant = variant is None

        self._setup_variant_colors(painter, index, is_illusory_variant)

        painter.drawRect(self._variant_rect(index))

        if not is_illusory_variant:
            painter.setPen(QColor(self._color_scheme.text_color))
            painter.drawText(self._variant_text_rect(index), cut_string(variant.text, self._MAX_VARIANT_CHARS))
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
        if self._is_message_started():
            painter.setBrush(self._start_message_brush)
        else:
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
                # настройки рисования для выделенного элемента
                painter.setBrush(QColor(self._color_scheme.selected_variant_background))
                painter.setPen(self._selected_pen)
            else:
                # настройки рисования
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
            self._MESSAGE_HEIGHT + self._VARIANT_DISTANCE + dy * variant_index,
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
        return QRectF(0, 0, self._MESSAGE_WIDTH, self._MESSAGE_HEIGHT)

    def _message_text_rect(self) -> QRectF:
        return QRectF(
            self._MESSAGE_TEXT_BORDER,
            self._MESSAGE_TEXT_BORDER,
            self._MESSAGE_WIDTH - self._MESSAGE_TEXT_BORDER * 2,
            self._MESSAGE_HEIGHT - self._MESSAGE_TEXT_BORDER * 2
        )

    def _block_rect(self) -> QRectF:
        """
        Область блока
        Returns:
            координаты области блока
        """
        rect = self._message_rect()
        # обычные варианты + иллюзорный вариант (через который добавляются новые варианты)
        for variant_index in range(len(self._variants) + 1):
            rect = rect.united(self._variant_rect(variant_index))

        x = rect.x() - self._BLOCK_RECT_EXTEND_SPACE
        y = rect.y() - self._BLOCK_RECT_EXTEND_SPACE
        width = rect.width() + 2 * self._BLOCK_RECT_EXTEND_SPACE
        height = rect.height() + 2 * self._BLOCK_RECT_EXTEND_SPACE
        return QRectF(x, y, width, height)

    def _start_message_title_block_rect(self) -> QRectF:
        return QRectF(
            self._START_MESSAGE_TITLE_BORDER_X,
            self._START_MESSAGE_TITLE_BORDER_Y,
            self._START_MESSAGE_TITLE_WIDTH,
            self._START_MESSAGE_TITLE_HEIGHT,
        )

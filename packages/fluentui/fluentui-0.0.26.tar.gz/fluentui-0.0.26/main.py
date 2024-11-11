import sys
from math import radians, cos, sin

from PySide6.QtCore import Qt, QSize, QRectF
from PySide6.QtGui import QPixmap, QPainter, QFont, QFontMetrics, QBrush, QPen
from PySide6.QtWidgets import QApplication, QGraphicsPixmapItem, QToolBox, QStyleOptionGraphicsItem, QWidget

from fluentui.gui import Font, Color
from fluentui.widgets import Widget, Row, Column, ImageViewer, WidgetMix, Label, Stretch, ColorDialog, Spacing, Slider, \
    Input, Application, Button, RadioButton, StyleSheet


class WatermarkPixmap(QGraphicsPixmapItem):
    def __init__(self, filename: str, *,
                 text='Watermark',
                 size=24,
                 angle=0,
                 color='#fff',
                 alpha=0.6,
                 spacing=5,
                 ):
        super().__init__(QPixmap(filename))
        self.text = text
        self.font = Font("Arial, Microsoft YaHei UI", point=size, weight=QFont.Weight.Medium)
        self.angle = angle  # 旋转角度
        self.color = Color(color, alpha)
        self.spacing = spacing  # 水印间距百分比

    def set_text(self, text: str) -> None:
        self.text = text
        self.update()

    def set_font_size(self, size: int) -> None:
        self.font.setPointSize(size)
        self.update()

    def set_angle(self, angle: int) -> None:
        self.angle = angle
        self.update()

    def set_color(self, color: str, alpha: int) -> None:
        if color: self.color.setNamedColor(color)
        self.color.setAlphaF(alpha)
        self.update()

    def set_spacing(self, spacing: int) -> None:
        self.spacing = spacing
        self.update()

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget):
        super().paint(painter, option, widget)
        font_metrics = QFontMetrics(self.font)
        text_size = font_metrics.size(Qt.TextFlag.TextSingleLine, self.text)

        # 计算旋转后的文本尺寸
        rad = radians(self.angle)  # 将旋转角度转为弧度
        rotated_width = text_size.width() * cos(rad) + text_size.height() * sin(rad)
        rotated_height = text_size.width() * sin(rad) + text_size.height() * cos(rad)

        # 创建水印图案（包含间距）
        bounding_rect = self.boundingRect()
        radius = min(bounding_rect.width() / 2, bounding_rect.height() / 2)  # 最小半径
        spacing = radius * self.spacing / 100  # 水印间距

        pattern_size = QSize(int(rotated_width + spacing), int(rotated_height + spacing))
        pixmap = QPixmap(pattern_size)
        pixmap.fill(Qt.GlobalColor.transparent)

        watermark = QPainter(pixmap)
        watermark.setFont(self.font)
        watermark.setPen(QPen(self.color, 0))

        # 将原点移到图案中心，但考虑间距
        watermark.translate(pattern_size.width() / 2 - spacing / 2,
                            pattern_size.height() / 2 - spacing / 2)
        watermark.rotate(self.angle)

        # 绘制文本，确保居中
        text_rect = QRectF(-text_size.width() / 2, -text_size.height() / 2,
                           text_size.width(), text_size.height())
        watermark.drawText(text_rect, self.text)
        watermark.end()

        painter.fillRect(bounding_rect, QBrush(pixmap))


class ToolBox(WidgetMix, QToolBox):
    def __init__(self):
        super().__init__(width=200)
        self.alpha = 0.5  # 透明度
        self.angle = 0  # 旋转角度
        self.spacing = 5  # 间距百分比
        self.font_size = 24  # 字体大小

        self.text = Input('水印', placeholder='请输入水印')
        self.color_label = Label(
            appear={'border': '1 solid #d1d1d1'},
            width=32,
            on_clicked=self.on_color_clicked
        )

        self.color_dialog = ColorDialog(color_selected=lambda: self.on_color_clicked(False))
        self.color_dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)

        self.alpha_label = Label(f'透明 {int(self.alpha * 100)}%', width=60)
        self.alpha_slider = Slider(100, value=100 * self.alpha, value_changed=self.on_alpha_changed)

        self.angle_label = Label(f'旋转 {self.angle}°', width=60)
        self.angle_slider = Slider(360, value=self.angle, value_changed=self.on_angle_changed)

        self.spacing_label = Label(f'间距 {self.spacing}%', width=60)
        self.spacing_slider = Slider(100, value=self.angle, value_changed=self.on_spacing_changed)

        self.size_label = Label(f'尺寸 {self.font_size}', width=60)
        self.size_slider = Slider(100, value=self.font_size, value_changed=self.on_size_changed)

        self.addItem(Widget(Column(
            Row(self.text, Spacing(6), self.color_label),
            Row(self.alpha_label, self.alpha_slider, spacing=6),
            Row(self.angle_label, self.angle_slider, spacing=6),
            Row(self.spacing_label, self.spacing_slider, spacing=6),
            Row(self.size_label, self.size_slider, spacing=6),
            Stretch(),
            spacing=6,
            margin='8',
        )), '添加水印')

    def on_color_clicked(self, open=True):
        if open: self.color_dialog.open()
        self.color_label.setStyleSheet(
            f'Label {{\n'
            f'    border: 1 solid #d1d1d1;\n'
            f'    background: {self.color_dialog.currentColor().name()};\n'
            f'}}'
        )

    def on_size_changed(self, value: int):
        self.font_size = value
        self.size_label.setText(f'尺寸 {value}')

    def on_alpha_changed(self, value: int):
        self.alpha = value * 0.01
        self.alpha_label.setText(f'透明 {int(self.alpha * 100)}%')

    def on_angle_changed(self, value: int):
        self.angle = value
        self.angle_label.setText(f'旋转 {value}°')

    def on_spacing_changed(self, value: int):
        self.spacing = value
        self.spacing_label.setText(f'间距 {value}%')


class MainWindow(Widget):
    def __init__(self):
        self.view = ImageViewer()
        self.view.setMinimumSize(700, 420)
        self.right = ToolBox()

        super().__init__(Row(self.view, self.right))

        self.setWindowTitle('Image Viewer')
        self.resize(800, 600)

    def load_image(self, filename: str):
        self.view.load(item := WatermarkPixmap(
            filename,
            text=self.right.text.text(),
            size=self.right.font_size,
            angle=self.right.angle,
            color=self.right.color_dialog.currentColor().name(),
            alpha=self.right.alpha,
            spacing=self.right.spacing
        ))

        self.right.text.textChanged.connect(item.set_text)
        self.right.angle_slider.valueChanged.connect(item.set_angle)
        self.right.color_dialog.colorSelected.connect(
            lambda: item.set_color(self.right.color_dialog.currentColor().name(), self.right.alpha)
        )
        self.right.alpha_slider.valueChanged.connect(lambda: item.set_color('', self.right.alpha))
        self.right.spacing_slider.valueChanged.connect(item.set_spacing)
        self.right.size_slider.valueChanged.connect(item.set_font_size)


if __name__ == '__main__':
    app = Application(
        font=Font(pixel=14),
        color_scheme=Qt.ColorScheme.Light
    )

    win = Widget(size='960 600')

    b1 = Button(
        'Light',
        color_scheme='dark',
        parent=win,
        # clicked=lambda: apply_theme(win, 'light')
    )

    # StyleSheet.apply(b1, 'dark')
    b1.setParent(win)

    # b2 = RadioButton(
    #     'Light',
    #     parent=win,
    #     # clicked=lambda: apply_theme(win, 'dark')
    # )

    b1.move(10, 20)
    # b2.move(10, 60)

    win.show()
    sys.exit(app.exec())

    # viewer = MainWindow()
    # viewer.show()
    # viewer.load_image('input.png')
    #
    # sys.exit(app.exec())

import sys

from PyMyMethod.Method import FileControl
from PySide6.QtWidgets import QApplication

from qfluentwidgets import SettingCardGroup, VBoxLayout, SmoothScrollArea, FluentIcon, setTheme, Theme, InfoBar, \
    InfoBarPosition, Action, TitleLabel, OptionsSettingCard, OptionsConfigItem, qconfig, OptionsValidator, \
    FolderListSettingCard, ConfigItem, FolderValidator, FolderListValidator, ExpandSettingCard, ExpandGroupSettingCard, \
    ToolButton, PrimaryToolButton, TransparentPushButton

from CustomCardWidget import *


class Demo(SmoothScrollArea):
    def __init__(self):
        super().__init__()

        self.initWindow()
        self.initCardGroup()
        self.initLayout()

    def initWindow(self):
        self.scrollWidget = QWidget()
        self.vLayout = VBoxLayout(self.scrollWidget)
        self.vLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.resize(1200, 700)
        desktop = QApplication.primaryScreen().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.cardGroup = SettingCardGroup('标准按钮卡片', self)
        self.cardGroup.setContentsMargins(20, 20, 20, 20)

    def initCardGroup(self):
        pushButtonCard = PushButtonCard(
                FluentIcon.SETTING,
                '标准按钮',
                'PushButton',
                '确定',
                parent=self
            )
        self.cardGroup.addSettingCard(
            pushButtonCard
        )
        pushButtonCard.button.clicked.connect(
            lambda: print('标准按钮卡片')
        )
        # -----------------------------------------
        primaryPushButtonCard = PrimaryPushButtonCard(
                FluentIcon.SEND,
                '主题色按钮',
                'PrimaryPushButton',
                '确定',
                parent=self
            )
        self.cardGroup.addSettingCard(
            primaryPushButtonCard
        )
        primaryPushButtonCard.button.clicked.connect(
            lambda: print('主题色按钮')
        )
        # -----------------------------------------
        switchButtonCard = SwitchButtonCard(
                FluentIcon.WIFI,
                '状态开关按钮',
                'SwitchButton',
                True,
                self
            )
        self.cardGroup.addSettingCard(
            switchButtonCard
        )
        switchButtonCard.button.checkedChanged.connect(
            lambda b: print(b)
        )
        # -----------------------------------------
        self.cardGroup.addSettingCard(
            HyperLinkButtonCard(
                'https://www.baidu.com',
                FluentIcon.GITHUB,
                '超链接按钮',
                'HyperLinkButton',
                buttonText='打开百度',
                buttonIcon=FluentIcon.LINK,
                parent=self
            )
        )
        # -----------------------------------------
        comboBoxCard = ComboxButtonCard(
            FluentIcon.FLAG,
            '下拉框',
            'ComboBox',
            ['1', '2', '3'],
            '确定',
            True,
            '提示信息',
            self
        )
        self.cardGroup.addSettingCard(
            comboBoxCard
        )
        comboBoxCard.combox.currentIndexChanged.connect(
            lambda: print(comboBoxCard.combox.currentText())
        )
        comboBoxCard.button.clicked.connect(
            lambda: print(f'选中的是{comboBoxCard.combox.currentText()}')
        )
        # -----------------------------------------
        editComboBoxCard = EditComboBoxButtonCard(
            FluentIcon.SEND,
            '可编辑下拉框',
            'EditComboBox',
            ['1', '2', '3'],
            '确定',
            True,
            '提示信息',
            parent=self
        )
        self.cardGroup.addSettingCard(
            editComboBoxCard
        )
        editComboBoxCard.combox.currentIndexChanged.connect(
            lambda: print(editComboBoxCard.combox.currentText())
        )
        # -----------------------------------------
        self.twoButtonCard = TwoButtonCard(
            FluentIcon.POWER_BUTTON,
            '双按钮',
            'TwoButton',
            '选择文件路径',
            FluentIcon.FOLDER,
            '确定',
            self,
        )
        self.cardGroup.addSettingCard(
            self.twoButtonCard
        )
        self.twoButtonCard.oneButton.clicked.connect(
            lambda: (
                self.updateFilePath(FileControl().getFilePathQT()),
                InfoBar.info(
                    '',
                    f'选择的目录是{self.filePath}',
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    isClosable=False,
                    parent=self
                ),
                self.twoButtonCard.contentLabel.setText(f'文件路径: {self.filePath}')
            )
        )
        self.twoButtonCard.button.clicked.connect(
            lambda: print('确定')
        )
        # -----------------------------------------
        self.cardGroup.addSettingCard(
            ComboBoxCard(
                FluentIcon.DOWNLOAD,
                '下拉框',
                'ComboBox',
                ['简体中文', '繁体中文', 'English'],
                True,
                '选择语言',
                self
            )
        )
        # -----------------------------------------
        self.cardGroup.addSettingCard(
            EditComboBoxCard(
                FluentIcon.DOWNLOAD,
                '下拉框',
                'ComboBox',
                ['简体中文', '繁体中文', 'English'],
                True,
                '选择语言',
                self
            )
        )
        # -----------------------------------------
        self.cardGroup.addSettingCard(
            OptionsSettingCard(
                # qconfig.themeMode,
                OptionsConfigItem(
                    'theme',
                    'theme',
                    '浅色',
                    OptionsValidator(['浅色', '深色', '跟随系统设置'])
                ),
                FluentIcon.BRUSH,
                '应用主题',
                '调整你的应用外观',
                ['浅色', '深色', '跟随系统设置']
            )
        )
        # -----------------------------------------
        folderCard = FolderListSettingCard(
                ConfigItem(
                    'folder',
                    'folder',
                    [],
                    FolderListValidator()
                ),
                '本地音乐库',
                '',
                parent=self
            )
        self.cardGroup.addSettingCard(
            folderCard
        )
        # -----------------------------------------
        expand = ExpandGroupSettingCard(
                FluentIcon.GITHUB,
                'title',
                'content',
                self
            )
        self.cardGroup.addSettingCard(
            expand
        )
        # -----------------------------------------
        self.expand = ExpandButtonCard(
                FluentIcon.IMAGE_EXPORT,
                '展开卡片',
                'ExpandButton',
                self
            )
        self.cardGroup.addSettingCard(
            self.expand
        )
        items = [
            ['开启省电模式', '确定', PushButton],
            ['开启飞行模式', '确定', PrimaryPushButton],
            ['开启WIFI', '确定', TransparentPushButton],
            ['开启性能模式', '确定', ToolButton],
            ['开启vx', '确定', PrimaryToolButton],
            ['开启5G', '确定', TransparentToolButton],
        ]

        functions = [
            lambda: print('开启省电模式'),
            lambda: print('开启飞行模式'),
            lambda: print('开启WIFI'),
            lambda: print('开启性能模式'),
            lambda: print('开启vx'),
            lambda: print('开启5G'),
        ]

        for item, fc in zip(items, functions):
            self.expand.addButton(
                item[0],
                item[1],
                button=item[2],
            ).clicked.connect(fc)

        combox = self.expand.addComboBox(
            '下拉框',
            ['1', '2', '3', '4', '5'],
        )
        editCombox = self.expand.addComboBox(
            '下拉框',
            ['Hello', 'World', 'Python', 'Qt'],
            comboBox=EditableComboBox
        )
        combox.currentIndexChanged.connect(
            lambda: print(combox.currentText())
        )
        editCombox.currentIndexChanged.connect(
            lambda: print(editCombox.currentText())
        )
        # -----------------------------------------
        self.expand.addSwitchButton(
            '开启WIFI',
            True,
        ).checkedChanged.connect(lambda b: print(b))
        self.expand.addRangeButton(
            '设置音量',
            (0, 100),
            20,
        ).valueChanged.connect(lambda value: print(value))
        # -----------------------------------------

    def initLayout(self):
        self.vLayout.addWidget(self.cardGroup)

    def updateFilePath(self, path):
        self.filePath = path

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    setTheme(Theme.DARK)
    window.show()
    sys.exit(app.exec())
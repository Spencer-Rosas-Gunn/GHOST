from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QFont
from qdarkstyle import load_stylesheet_pyqt5
import http.cookiejar
from http.cookiejar import CookieJar
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEngineSettings


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.cookie_instances = {}
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        monospaced_font = QFont("Courier New", 12)
        monospaced_font.setBold(True)
        self.setFont(monospaced_font)

    def add_tab(self, url):
        browser = QWebEngineView()
        browser.settings().setAttribute(QWebEngineSettings.WebRTCPublicInterfacesOnly, True)
        browser.settings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, False)
        browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, False)
        browser.settings().setAttribute(QWebEngineSettings.WebGLEnabled, False)
        browser.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)

        browser.setUrl(QUrl(url))
        index = self.addTab(browser, "New Tab")
        self.setCurrentIndex(index)
        self.setTabText(index, "Loading...")  # Set initial title as "Loading..."
        browser.titleChanged.connect(lambda title: self.setTabText(index, title))

    def close_tab(self, index):
        current_tab = self.widget(index)
        if current_tab:
            current_tab.page().profile().clearAllVisitedLinks()
        self.removeTab(index)

class MyWebBrowser(QMainWindow):
    def __init__(self):
        self.default_page = "https://www.mojeek.com/?qsba=1&hp=minimal&theme=dark&autocomp=0&qss=Bing,Brave,DuckDuckGo,Ecosia,Google,Lilo,Metager,Qwant,Startpage,Swisscows,Yandex,Yep,You"
        monospaced_font = QFont("Courier New", 12)
        button_font = QFont("Courier New", 24)
        monospaced_font.setBold(True)

        super().__init__()

        self.tabs = TabWidget()
        self.add_tab(self.default_page)

        self.url_bar = QTextEdit()
        self.url_bar.setMaximumHeight(30)
        self.url_bar.setFont(monospaced_font)
        self.url_bar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.url_bar.setWordWrapMode(False)

        self.url_bar.grabShortcut(QKeySequence(Qt.Key_Return))
        self.url_bar.grabShortcut(QKeySequence(Qt.Key_Enter))
        self.url_bar.installEventFilter(self)

        self.go_btn = QPushButton("  ↺  ")
        self.go_btn.setMinimumHeight(30)
        self.go_btn.clicked.connect(self.navigate)
        self.go_btn.setFont(button_font)

        self.back_btn = QPushButton("  ↤  ")
        self.back_btn.setMinimumHeight(30)
        self.back_btn.setFont(button_font)
        self.back_btn.clicked.connect(self.back)

        self.forward_btn = QPushButton("  ↦  ")
        self.forward_btn.setMinimumHeight(30)
        self.forward_btn.setFont(button_font)
        self.forward_btn.clicked.connect(self.forward)

        self.add_tab_btn = QPushButton("  ↻  ")
        self.add_tab_btn.setMinimumHeight(30)
        self.add_tab_btn.clicked.connect(lambda: self.add_tab(self.default_page))
        self.add_tab_btn.setFont(button_font)

        self.instance_display = QPushButton("  0  ")
        self.instance_display.setMinimumHeight(30)
        self.instance_display.setFont(button_font)
        self.instance_display.clicked.connect(self.reset)

        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.url_bar)
        self.horizontal_layout.addWidget(self.go_btn)
        self.horizontal_layout.addWidget(self.back_btn)
        self.horizontal_layout.addWidget(self.forward_btn)
        self.horizontal_layout.addWidget(self.add_tab_btn)
        self.horizontal_layout.addWidget(self.instance_display)

        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addLayout(self.horizontal_layout)
        self.central_layout.addWidget(self.tabs)

        self.cookie_instances = {}

        self.setCentralWidget(self.central_widget)
        self.show()

    def eventFilter(self, obj, event):
        if obj == self.url_bar and event.type() == QEvent.KeyPress:
            if event.key() in [Qt.Key_Return, Qt.Key_Enter]:
                self.navigate()
                return True
        return super().eventFilter(obj, event)

    def add_tab(self, url):
        self.tabs.add_tab(url)
    
    def reset(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            instance_id = "0"
            if not self.goto_instance(instance_id):
                self.clear_instance(instance_id)
                self.instance_display.setText("  0  ")
            else:
                self.clear_instance(instance_id)
    
    def back(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.back()

    def forward(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.forward()

    def navigate(self):
        current_tab = self.tabs.currentWidget()        
        if current_tab:
            url = self.url_bar.toPlainText()
            if url == "~dark":
                self.default_page = "https://www.mojeek.com/?qsba=1&hp=minimal&theme=dark&autocomp=0&qss=Bing,Brave,DuckDuckGo,Ecosia,Google,Lilo,Metager,Qwant,Startpage,Swisscows,Yandex,Yep,You"
                self.url_bar.setText(self.default_page)
                current_tab.setUrl(QUrl(self.default_page))
                app.setStyleSheet(load_stylesheet_pyqt5())
                return
            if url == "~lite":
                self.default_page = "https://www.mojeek.com/?qsba=1&hp=minimal&theme=lite&autocomp=0&qss=Bing,Brave,DuckDuckGo,Ecosia,Google,Lilo,Metager,Qwant,Startpage,Swisscows,Yandex,Yep,You"
                self.url_bar.setText(self.default_page)
                current_tab.setUrl(QUrl(self.default_page))
                app.setStyleSheet("")
                return
            if url.startswith("~inst "):
                instance_id = url[6:]
                instance_num = int(instance_id)  # Initialize instance_num
                if not self.goto_instance(instance_id):
                    self.new_instance(instance_id)
                if instance_num < 10:
                    self.instance_display.setText("  " + str(instance_num) + "  ")
                elif instance_num < 100:
                    self.instance_display.setText(" " + str(instance_num) + "  ")
                else:
                    self.instance_display.setText(" " + str(instance_num) + " ")
                return
            if not url.startswith("https://"):
                if not url.startswith("http://"):
                    url = "https://" + url
            self.url_bar.setText(url)
            current_tab.setUrl(QUrl(url))

    def new_instance(self, instance_id):
        new_cookie_jar = CookieJar()
        self.cookie_instances[instance_id] = {'jar': new_cookie_jar}

    def goto_instance(self, instance_id):
        if instance_id in self.cookie_instances:
            self.cookie_jar = self.cookie_instances[instance_id]['jar']
            return True
        else:
            return False


    def clear_instance(self, instance_id):
        if instance_id in self.cookie_instances:
            self.cookie_instances[instance_id]['jar'].clear()

if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(load_stylesheet_pyqt5())
    window = MyWebBrowser()
    app.exec_()
rkstyle import load_stylesheet_pyqt5
import http.cookiejar
from http.cookiejar import CookieJar
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEngineSettings


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.cookie_instances = {}
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        monospaced_font = QFont("Courier New", 12)
        monospaced_font.setBold(True)
        self.setFont(monospaced_font)

    def add_tab(self, url):
        browser = QWebEngineView()
        browser.settings().setAttribute(QWebEngineSettings.WebRTCPublicInterfacesOnly, True)
        browser.settings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, False)
        browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, False)
        browser.settings().setAttribute(QWebEngineSettings.WebGLEnabled, False)
        browser.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, False)


        browser.setUrl(QUrl(url))
        index = self.addTab(browser, "New Tab")
        self.setCurrentIndex(index)
        self.setTabText(index, "Loading...")  # Set initial title as "Loading..."
        browser.titleChanged.connect(lambda title: self.setTabText(index, title))

    def close_tab(self, index):
        self.removeTab(index)

class MyWebBrowser(QMainWindow):
    def __init__(self):
        self.default_page = "https://www.mojeek.com/?qsba=1&hp=minimal&theme=dark&autocomp=0&qss=Bing,Brave,DuckDuckGo,Ecosia,Google,Lilo,Metager,Qwant,Startpage,Swisscows,Yandex,Yep,You"
        monospaced_font = QFont("Courier New", 12)
        button_font = QFont("Courier New", 24)
        monospaced_font.setBold(True)

        super().__init__()

        self.tabs = TabWidget()
        self.add_tab(self.default_page)

        self.url_bar = QTextEdit()
        self.url_bar.setMaximumHeight(30)
        self.url_bar.setFont(monospaced_font)
        self.url_bar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.url_bar.setWordWrapMode(False)

        self.url_bar.grabShortcut(QKeySequence(Qt.Key_Return))
        self.url_bar.grabShortcut(QKeySequence(Qt.Key_Enter))
        self.url_bar.installEventFilter(self)

        self.go_btn = QPushButton("  ↺  ")
        self.go_btn.setMinimumHeight(30)
        self.go_btn.clicked.connect(self.navigate)
        self.go_btn.setFont(button_font)

        self.back_btn = QPushButton("  ↤  ")
        self.back_btn.setMinimumHeight(30)
        self.back_btn.setFont(button_font)
        self.back_btn.clicked.connect(self.back)

        self.forward_btn = QPushButton("  ↦  ")
        self.forward_btn.setMinimumHeight(30)
        self.forward_btn.setFont(button_font)
        self.forward_btn.clicked.connect(self.forward)

        self.add_tab_btn = QPushButton("  ↻  ")
        self.add_tab_btn.setMinimumHeight(30)
        self.add_tab_btn.clicked.connect(lambda: self.add_tab(self.default_page))
        self.add_tab_btn.setFont(button_font)

        self.instance_display = QPushButton("  0  ")
        self.instance_display.setMinimumHeight(30)
        self.instance_display.setFont(button_font)
        self.instance_display.clicked.connect(self.reset)

        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.url_bar)
        self.horizontal_layout.addWidget(self.go_btn)
        self.horizontal_layout.addWidget(self.back_btn)
        self.horizontal_layout.addWidget(self.forward_btn)
        self.horizontal_layout.addWidget(self.add_tab_btn)
        self.horizontal_layout.addWidget(self.instance_display)

        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addLayout(self.horizontal_layout)
        self.central_layout.addWidget(self.tabs)

        self.cookie_instances = {}

        self.setCentralWidget(self.central_widget)
        self.show()

    def eventFilter(self, obj, event):
        if obj == self.url_bar and event.type() == QEvent.KeyPress:
            if event.key() in [Qt.Key_Return, Qt.Key_Enter]:
                self.navigate()
                return True
        return super().eventFilter(obj, event)

    def add_tab(self, url):
        self.tabs.add_tab(url)
    
    def reset(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            instance_id = "0"
            if not self.goto_instance(instance_id):
                self.clear_instance(instance_id)
                self.instance_display.setText("  0  ")
            else:
                self.clear_instance(instance_id)
    
    def back(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.back()

    def forward(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.forward()

    def navigate(self):
        current_tab = self.tabs.currentWidget()
        
        if current_tab:
            url = self.url_bar.toPlainText()
            if url == "~dark":
                self.default_page = "https://www.mojeek.com/?qsba=1&hp=minimal&theme=dark&autocomp=0&qss=Bing,Brave,DuckDuckGo,Ecosia,Google,Lilo,Metager,Qwant,Startpage,Swisscows,Yandex,Yep,You"
                self.url_bar.setText(self.default_page)
                current_tab.setUrl(QUrl(self.default_page))
                app.setStyleSheet(load_stylesheet_pyqt5())
                return
            if url == "~lite":
                self.default_page = "https://www.mojeek.com/?qsba=1&hp=minimal&theme=lite&autocomp=0&qss=Bing,Brave,DuckDuckGo,Ecosia,Google,Lilo,Metager,Qwant,Startpage,Swisscows,Yandex,Yep,You"
                self.url_bar.setText(self.default_page)
                current_tab.setUrl(QUrl(self.default_page))
                app.setStyleSheet("")
                return
            if url.startswith("~inst "):
                instance_id = url[6:]
                instance_num = int(instance_id)  # Initialize instance_num
                if not self.goto_instance(instance_id):
                    self.new_instance(instance_id)
                if instance_num < 10:
                    self.instance_display.setText("  " + str(instance_num) + "  ")
                elif instance_num < 100:
                    self.instance_display.setText(" " + str(instance_num) + "  ")
                else:
                    self.instance_display.setText(" " + str(instance_num) + " ")
                return
            if not url.startswith("https://"):
                if not url.startswith("http://"):
                    url = "https://" + url
            self.url_bar.setText(url)
            current_tab.setUrl(QUrl(url))

    def new_instance(self, instance_id):
        new_cookie_jar = CookieJar()
        self.cookie_instances[instance_id] = {'jar': new_cookie_jar}

    def goto_instance(self, instance_id):
        if instance_id in self.cookie_instances:
            self.cookie_jar = self.cookie_instances[instance_id]['jar']
            return True
        else:
            return False


    def clear_instance(self, instance_id):
        if instance_id in self.cookie_instances:
            self.cookie_instances[instance_id]['jar'].clear()

if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(load_stylesheet_pyqt5())
    window = MyWebBrowser()
    app.exec_()

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFrame, QSlider, QWidget, QLabel, QPushButton, QSizePolicy, QHBoxLayout, QTextBrowser
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor
from data import data

references = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        .container {
            text-align: left;
            padding: 20px;
        }
        img {
            max-width: 100%;
            height: auto;
        }
        .content {
            margin-top: 20px;
            font-size: 18px;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="image-container">
        </div>
        <h1>References</h1>
        <br>
        <div class="content" align="left">
            <p>Astronomy Trek. (n.d.). Important dates in the timeline of astronomy. Python.org. 
                <br><a href=https://www.astronomytrek.com/important-dates-in-the-timeline-of-astronomy>https://www.astronomytrek.com/important-dates-in-the-timeline-of-astronomy/</a>
                <br>
                Encyclopaedia Britannica. (n.d.). Tycho's Nova. Python.org. 
                <br><a href=https://www.britannica.com/place/Tychos-Nova>https://www.britannica.com/place/Tychos-Nova</a>
                <br>
                Moskowitz, C. (2010). Einstein’s ‘biggest blunder’ turns out to be right. Python.org. 
                <br><a href=https://www.space.com/9593-einstein-biggest-blunder-turns.html>https://www.space.com/9593-einstein-biggest-blunder-turns.html</a>
                <br>
                NASA. (2021). 240 years ago: Astronomer William Herschel identifies Uranus as the seventh planet. Python.org. 
                <br><a href=https://www.nasa.gov/history/240-years-ago-astronomer-william-herschel-identifies-uranus-as-the-seventh-planet>https://www.nasa.gov/history/240-years-ago-astronomer-william-herschel-identifies-uranus-as-the-seventh-planet/</a>
                <br>
                NASA. (n.d.). Hubble gravitational lenses. Python.org. 
                <br><a href=https://science.nasa.gov/mission/hubble/science/science-behind-the-discoveries/hubble-gravitational-lenses>https://science.nasa.gov/mission/hubble/science/science-behind-the-discoveries/hubble-gravitational-lenses/</a>
                <br>
                Oxford Reference. (n.d.). Timeline of astronomy. Python.org. 
                <br><a href=https://www.oxfordreference.com/display/10.1093/acref/9780191737305.timeline.0001>https://www.oxfordreference.com/display/10.1093/acref/9780191737305.timeline.0001</a>
                <br>
                The Schools' Observatory. (n.d.). History of astronomy timeline. Python.org. 
                <br><a href=https://www.schoolsobservatory.org/things-to-do/history-astro-timeline>https://www.schoolsobservatory.org/things-to-do/history-astro-timeline</a>
                <br>
                Williams College. (n.d.). Astronomy timeline. Python.org. 
                <br><a href=https://web.williams.edu/Astronomy/Course-Pages/334/timeline.html>https://web.williams.edu/Astronomy/Course-Pages/334/timeline.html</a></p>
        </div>
    </div>
</body>
</html>'''

htmls = {0: '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        .container {
            text-align: left;
            padding: 20px;
        }
        img {
            max-width: 100%;
            height: auto;
        }
        .content {
            margin-top: 20px;
            font-size: 18px;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="image-container">
        </div>
        <h1>{title}</h1>
        <div class="content" align="left">
            {content}
        </div>
    </div>
</body>
</html>''', 1: '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        .container {
            text-align: left;
            padding: 20px;
        }
        img {
            max-width: 100%;
            height: auto;
        }
        .content {
            margin-top: 20px;
            font-size: 18px;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="image-container">
        <img src="{image_src_1}" alt="Image 1" />
        </div>
        <h1>{title}</h1>
        <div class="content" align="left">
            {content}
        </div>
    </div>
</body>
</html>''',
         2: '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        .container {
            text-align: left;
            padding: 20px;
        }
        img {
            max-width: 30px;
            height: auto;
        }
        .content {
            margin-top: 20px;
            font-size: 18px;
            line-height: 1.6;
        }
        .image-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="image-container">
        <img src="{image_src_1}" alt="Image 1" />
        <img src="{image_src_2}" alt="Image 2" />
        </div>  
        <h1>{title}</h1>
        <div class="content" align="left">
            {content}
        </div>
    </div>
</body>
</html>'''}

def get_html(title, content, images):
    format_ = htmls[len(images)]
    for i in range(len(images)):
        format_ = format_.replace('{image_src_' + str(i + 1) + '}', images[i])

    format_ = format_.replace('{title}', title)
    format_ = format_.replace('{content}', content)
    return format_

class TimelineApp(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("PyQt Timeline Window")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)
        frame_layout = QVBoxLayout(self.frame)  # Added layout for QFrame
        layout.addWidget(self.frame)
        
        self.text_browser = QTextBrowser()  # Added QTextBrowser
        
        self.text_browser.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.text_browser.setOpenExternalLinks(True)
        
        frame_layout.addWidget(self.text_browser)
        
        self.label = QLabel("Seeing events for 1543 A.D.")
        
        self.label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        layout.addWidget(self.label)
        self.range = (1530, 2020)

        self.timeline = QSlider(Qt.Orientation.Horizontal)
        
        self.timeline.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        
        self.timeline.setRange(*self.range)
        self.timeline.valueChanged.connect(self.update_label)
        layout.addWidget(self.timeline)
        
        button_layout = QHBoxLayout()
        self.back_button = QPushButton("\u2190 Back")
        self.next_button = QPushButton("Next \u2192")
        self.back_button.clicked.connect(self.go_back)
        self.next_button.clicked.connect(self.go_next)
        
        self.back_button.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        self.next_button.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.next_button)
        layout.addLayout(button_layout)

        self.refs_button = QPushButton("References")
        self.refs_button.clicked.connect(self.show_refs)

        self.refs_button.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)

        layout.addWidget(self.refs_button)
        self.data = data
        self.markers = list(self.data.data.keys())
        
        self.show()

    def show_refs(self):
        self.text_browser.setHtml(references)
    
    def update_label(self, value):
        self.label.setText(f"Seeing events for {value} A.D.")
    
    def add_marker(self, position):
        if self.range[0] <= position <= self.range[1]:
            self.markers.append(position)
            self.markers.sort()
            self.update()
    
    def go_back(self):
        if self.markers:
            current_value = self.timeline.value()
            previous_markers = [m for m in self.markers if m < current_value]
            if previous_markers:
                self.timeline.setValue(previous_markers[-1])
                self.text_browser.setHtml(get_html(**self.data.get_data(previous_markers[-1])))
    
    def go_next(self):
        if self.markers:
            current_value = self.timeline.value()
            next_markers = [m for m in self.markers if m > current_value]
            if next_markers:
                self.timeline.setValue(next_markers[0])
                self.text_browser.setHtml(get_html(**self.data.get_data(next_markers[0])))
    
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QColor("red"))
        
        slider_geometry = self.timeline.geometry()
        slider_x = slider_geometry.x()
        slider_width = slider_geometry.width()
        slider_height = slider_geometry.height()
        min_year, max_year = self.range

        for marker in self.markers:
            relative_position = (marker - min_year) / (max_year - min_year)
            x_pos = int(slider_x + relative_position * slider_width)
            painter.drawLine(x_pos, slider_geometry.y() + slider_height // 2, x_pos, slider_geometry.y() - 5)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimelineApp(data)
    sys.exit(app.exec())

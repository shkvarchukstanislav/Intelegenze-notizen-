from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QHBoxLayout, \
    QVBoxLayout, QInputDialog
import json

notes = {"Willkommen": {"text": "Test text",
                             "tags": ["welcome", "start"]}}


def update_database():
    with open("database.json", "w", encoding="utf-8") as f:
        json.dump(notes, f)


try:
    with open("database.json", "r", encoding="utf-8") as f:
        notes = json.load(f)
except:
    update_database()

app = QApplication([])

window = QWidget()
window.setWindowTitle("Intelligente Notizen")

window.resize(800, 600)

main_layout = QHBoxLayout()

note_text = QTextEdit()
main_layout.addWidget(note_text)

right_layout = QVBoxLayout()

notes_list: QListWidget | QListWidget = QListWidget()
right_layout.addWidget(QLabel("Liste der Anmerkungen"))
right_layout.addWidget(notes_list)

buttons_layout = QHBoxLayout()

create_note_btn = QPushButton("Eine Notiz erstellen")
buttons_layout.addWidget(create_note_btn)

delete_note_btn = QPushButton("Notiz löschen")
buttons_layout.addWidget(delete_note_btn)

right_layout.addLayout(buttons_layout)

save_note_btn = QPushButton("Speichern Sie die Notiz")
right_layout.addWidget(save_note_btn)

tags_list = QListWidget()
right_layout.addWidget(QLabel("Liste der Tags"))
right_layout.addWidget(tags_list)

tag_input = QLineEdit()
right_layout.addWidget(QLabel("Geben Sie den Tag ein"))
right_layout.addWidget(tag_input)

tag_buttons_layout = QHBoxLayout()

add_tag_btn = QPushButton("Zur Notiz hinzufügen")
tag_buttons_layout.addWidget(add_tag_btn)

remove_tag_btn = QPushButton("Lösen Sie sich von der Notiz")
tag_buttons_layout.addWidget(remove_tag_btn)

right_layout.addLayout(tag_buttons_layout)

search_tag_btn = QPushButton("Suche nach Notizen nach Tag")
right_layout.addWidget(search_tag_btn)

main_layout.addLayout(right_layout)

window.setLayout(main_layout)


def update_note_list():
    notes_list.clear()
    notes_list.addItems(notes.keys())


def show_note():
    note_name = notes_list.currentItem().text()
    text = notes[note_name]["text"]
    note_text.setText(text)
    tags = notes[note_name]["tags"]
    tags_list.clear()
    tags_list.addItems(tags)


def add_note():
    note_name, ok = QInputDialog.getText(window, "Eine Notiz erstellen", "Titel der Notiz:")
    if ok:
        notes[note_name] = {"text": "",
                            "tags": []}
        update_note_list()
        update_database()


def save_note():
    note_name = notes_list.currentItem().text()
    if note_name in notes:
        text = note_text.toPlainText()
        notes[note_name]["text"] = text
        update_database()


def del_note():
    note_name = notes_list.currentItem().text()
    if note_name in notes:
        del notes[note_name]
        update_note_list()
        note_text.setText("")
        update_database()


def add_tag():
    tag_name = tag_input.text()
    if tag_name != "":
        note_name = notes_list.currentItem().text()
        if note_name in notes:
            notes[note_name]["tags"].append(tag_name)
            tags_list.addItem(tag_name)
            tag_input.setText("")
            update_database()

def del_tag():
    note_name = notes_list.currentItem().text()
    if note_name in notes:
        tag_name = tags_list.currentItem().text()
        notes[note_name]["tags"].remove(tag_name)
        update_database()
        tags = notes[note_name]["tags"]
        tags_list.clear()
        tags_list.addItems(tags)
def find_tag():
    tag_name = tag_input.text()
    notes_list.clear()
    for note in notes:
        if tag_name in notes[note]["tags"]:
            notes_list.addItem(note)
notes_list.itemClicked.connect(show_note)
create_note_btn.clicked.connect(add_note)
save_note_btn.clicked.connect(save_note)
delete_note_btn.clicked.connect(del_note)
add_tag_btn.clicked.connect(add_tag)
remove_tag_btn.clicked.connect(del_tag)
search_tag_btn.clicked.connect(find_tag)

update_note_list()
window.show()

app.exec_()

import feedparser
from tkinter import *
import webview

window = Tk()
window.title('Haber Bot Programi')
window.geometry('1000x600')

fr_haberler = Frame(window, height=600)
fr_buttons = Frame(window, relief=RAISED, bg='pink', bd=2)


def open_url(event):
    webview.create_window(event.widget.cget("text"), event.widget.cget("text"))
    webview.start()




# bunlar asagidakiler hata vermesin diye normalde jic kullanmayacagiz
def son_dakika_command():
    url = 'https://www.cnnturk.com/feed/rss/all/news'
    haberler = feedparser.parse(url)
    for haber in haberler.entries:
        Label(fr_haberler, text=haber.title, anchor='w', font=('Helveticabold', 14)).pack(side=TOP, fill='x')
        lbl_link = Label(fr_haberler, text=haber.link, anchor='w', font=('Helveticabold', 14), fg='blue', cursor='hand2')
        lbl_link.pack(side=TOP, fill='x')
        lbl_link.bind("<Button-1>", open_url)
        Label(fr_haberler, text='-', anchor='c', font=('Helveticabold', 1), bg='pink').pack(side=TOP, fill='x')


def dunya_command():
    print('dunya_command')

def ekonomi_command():
    print('ekonomi_command')

def saglik_command():
    print('saglik_command')


btn_son_dakika = Button(fr_buttons, text="Son Dakika", font=('Helveticabold', 14), bg='lightblue', command=son_dakika_command)
btn_dunya = Button(fr_buttons, text="Dünya", font=('Helveticabold', 14), bg='lightblue', command=dunya_command)
btn_ekonomi = Button(fr_buttons, text="Ekonomi", font=('Helveticabold', 14), bg='lightblue', command=ekonomi_command)
btn_saglik = Button(fr_buttons, text="Saglik", font=('Helveticabold', 14), bg='lightblue', command=saglik_command)



btn_son_dakika.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_dunya.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
btn_ekonomi.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
btn_saglik.grid(row=3, column=0, sticky='ew', padx=5, pady=5)


# butonlara pencere ekleme

fr_buttons.grid(row=0, column=0, sticky='ns')
fr_haberler.grid(row=0, column=1, sticky='nsew')

window.mainloop()


from tkinter import *
import time
import requests
import json

root=Tk()

root.geometry("900x250")

match_data=requests.get('https://cricapi.com/api/cricketScore?unique_id=1235285&apikey=L2Mo6arGxySgl56Kb5EqL7L6fcW2')
json_data=match_data.json()
def times():
    try:
        if(json_data["description"]):
            current_score=json_data["description"]
            score.configure(text="current score : "+ current_score)
            score.after(200,times)
    except(KeyError):
        score.configure(text="NO LIVE MATCHES NOW")
        score.after(200,times)

score=Label(root, font=("time",15,"bold"),bg="white")
score.grid(row=2,column=2,pady=25,padx=100)
times()
root.mainloop()
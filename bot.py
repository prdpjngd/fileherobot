#!/usr/bin/env python3
import pyrogram
from pyrogram import Client, Filters, MessageHandler, CallbackQueryHandler,CallbackQuery
from creds import config
import math
import time
import requests
import os


def download_link(link,file_name,prev_message):
  time1=time.time()
  direction="Download"
  num_list=[str(i)+".000" for i in range(0,101,5)]
  with open(file_name, "wb") as f:
          response = requests.get(link, stream=True)
          total_length = response.headers.get('content-length')
          if total_length is None: # no content length header
              f.write(response.content)
          else:
              dl = 0
              total_length = int(total_length)
              for data in response.iter_content(chunk_size=4096):
                  dl += len(data)
                  f.write(data)
                  n="{:.3f}".format((dl/total_length)*100)
                  if n in num_list:
                      progress_bar_f(dl,total_length,prev_message,time1,direction)

def msg_handler_f(client, message):
        msg_txt=message.text
        txt_pattern="[FILE_LINK] | [FILE_NAME_WITH_EXTENSION]"
        txt_to_send="Send Me Link in this Pattern :- \n"+txt_pattern
        if "http" in msg_txt and ' | ' in msg_txt :
            prev_message=app.send_message(
                text="Starting Download file .. ",
                chat_id=message.chat.id,
                reply_to_message_id=message.message_id
            )
            tmp_list=msg_txt.split(" | ")
            file_url=tmp_list[0].replace(" ","")
            file_name=tmp_list[1].replace(" ","")
            download_link(file_url,file_name,prev_message)
            upload_video(client,message,file_name)
        else:
            prev_message=app.send_message(
                text=txt_to_send,
                chat_id=message.chat.id,
                reply_to_message_id=message.message_id
            )


def human_size(bytes, units=[' bytes','KB','MB','GB','TB', 'PB']):
    return str(bytes) + units[0] if bytes < 1024 else human_size(bytes>>10, units[1:])

def upload_video(client, message,file_path):
    file_path_thumb="downloads/"+str(message.chat.id)+".jpeg"
    if not os.path.exists(file_path_thumb):
        file_path_thumb="downloads/demo.jpeg"
    prev_message=app.send_message(
        text="Starting Upload.....",
        chat_id=message.chat.id,
        reply_to_message_id=message.message_id
    )
    direction="upload"
    time1 = time.time()
    client.send_video(
        chat_id=message.chat.id,
        video=file_path,
        reply_to_message_id=message.message_id,
        caption="Uploaded by @fileherobot",
        progress=progress_bar_f,
        progress_args=(prev_message,time1,direction),
        thumb=file_path_thumb
    )

def progress_bar_f(current,total,prev_message,time1,direction):
    time2 = time.time()
    diff=time2-time1
    #progress bar Generator... string
    pro_bar_str="".join(["●" for i in range(1,math.floor(current/total*10)+1)])
    pro_bar_str=pro_bar_str+"".join(["○" for i in range(1,9-math.floor(current/total*10))])
    # k1 is current downloaded bytes
    k1=human_size(current)
    # where k2 is total byte length of file
    k2=human_size(total)
    #percntage is k3
    tmp="{:.2f}".format(current/total*100)
    k3="[ "+tmp+"% ]  "
    #transfer speed is k4
    k4=human_size(math.floor(current/diff))
    #this case when file is downloaded completly... 
    if total==current: 
        txt_to_send=direction+"ed : complete 100% ["+k2+"]\n"+k3+pro_bar_str
        txt_to_send=txt_to_send+"\nAvg. Transfer Speed :"+k4
        prev_message=app.edit_message_text(
            chat_id=prev_message.chat.id,
            message_id=prev_message.message_id,
            text=txt_to_send,
            parse_mode="html"
        )
    #this else case is when file is currently in downloading state
    else:
        txt_to_send=direction+"ing : "+k1+"/"+k2+"\n"+k3+pro_bar_str
        txt_to_send=txt_to_send+"\nTransfer Speed :"+k4
        prev_message=app.edit_message_text(
            chat_id=prev_message.chat.id, 
            message_id=prev_message.message_id,
            text=txt_to_send,
            parse_mode="html"
        )

def start_msg_handler_f(client,message):
    msg="hii.. I am FileHerobot \n"
    msg=msg+"> Can send Send Video \n"
    msg=msg+"> Can Send Files to telegram using Direct Links"
    message.reply_text(msg)

def button(bot, update):
    data = update.data.split("|")[0]
    if data=="y":
        src="downloads/"+update.data.split("|")[1]
        dst=src+".jpeg"
        os.rename(src,dst)
        update.edit_message_text("Thumbnail Set Done")
        
def file_handler(client,message):
    prev_message=app.send_message(
        text="Starting Download file .. ",
        chat_id=message.chat.id,
        reply_to_message_id=message.message_id
    )
    direction="Download"
    time1=time.time()
    k=client.download_media(
        message.video,
        progress=progress_bar_f,
        progress_args=(prev_message,time1,direction)
    )
    upload_video(client,message,k) 

def img_handler_f(client,message):
    k=message.download(str(message.chat.id))
    dst=str(message.chat.id)
    os.rename(k,"/app/downloads/"+dst)
    inline_keyboard = []
    inline_keyboard.append([
        pyrogram.InlineKeyboardButton(
            text="Set Thumbnail",
            callback_data="y|"+dst
        )
    ])
    reply_markup = pyrogram.InlineKeyboardMarkup(inline_keyboard)
    message.reply_text(
        "Want to Set This as Thumbnail..",
        quote=True,
        reply_markup=reply_markup
    )
    pyrogram.InputMessageContent

#application configration functions and declaration... ---->

app = Client("LeechBot",
        bot_token=config.TG_BOT_TOKEN,
        api_id=config.API_ID,
        api_hash=config.API_HASH
    )


#this text message handler
msg_handler = MessageHandler(msg_handler_f,Filters.text & ~Filters.command(["start","help"]))
app.add_handler(msg_handler)

# /start & /help command handler 
start_msg_handler = MessageHandler(start_msg_handler_f,Filters.command(["start","help"]))
app.add_handler(start_msg_handler)

# Image & thumbnail Handler 
app.add_handler(MessageHandler(img_handler_f,Filters.photo))

#Set_thumbnail_inline_answer_handler
call_back_button_handler = CallbackQueryHandler(button)
app.add_handler(call_back_button_handler)

#for video & file 
app.add_handler(MessageHandler(file_handler, Filters.document | Filters.video))

# service Start function
app.run()

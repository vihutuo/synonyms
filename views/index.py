import flet as ft
import random
from  mymodules import utils
import time
import  threading 
import mymodules.analytics
import os
from dotenv import load_dotenv

def CreateSynonymBoxes(synonyms,lst_text):
  #Return a column with all the synonyms
  col = ft.Column()
  for word,point in synonyms:
    row = ft.Row(spacing=3)
    lst_r = []
   
    hint_positions = []
    hint_positions.append(0)
    hint_positions.append(random.randrange(1,len(word))) 
    if len(word) > 3:
        hint_positions.append(random.randrange(1,len(word))) 
    count = 0 
    for c in word:
      if count in hint_positions :
        txt = c
      else:
        txt = ""
        
        
      txt = ft.Text(txt,text_align=ft.TextAlign.CENTER,size=20)
    
      box = ft.Container(content = txt, 
                         border=ft.border.all(1, ft.colors.BLACK),
                         width=30,height=30,
                         bgcolor=ft.colors.SURFACE ,
                         animate=ft.animation.Animation(1000),

                        )
      row.controls.append(box)
      lst_r.append(box)
      count+=1
    pt = ft.Text("+" + str(point),color=ft.colors.SECONDARY )
    
    row.controls.append(pt)
    col.controls.append(row)
    lst_text.append(lst_r)
  return col

def IndexView(page,params):
  
        
  def restart_clicked(e):
    nonlocal is_game_over
    is_game_over = False
   
    NewGame()
  def NewGame():
    nonlocal chosen_word
    nonlocal synonyms
    nonlocal score
    nonlocal time_remaining
    nonlocal is_game_over
    is_game_over = True
    score =0 
    time_remaining = 90
    lst_text.clear()
    
    file_name = "data/syns.txt"
    chosen_word,synonyms= utils.GetRandomSyn(file_name)
    fld_user_word.value = ""
    txt_score.value = score
    txt_chosen_word.value = chosen_word 
    col_right.controls.clear()
    
    col_right.controls.append(CreateSynonymBoxes(synonyms,lst_text))

    
    page.update()
 
    time.sleep(1)
    is_game_over = False
    t=threading.Timer(1,update_time)
    t.start()
    analytics.StartMatch(chosen_word)



  def GameOver():
    print("GameOver","Score",score)
    analytics.UpdateMatch(score)
    nonlocal  is_game_over
    is_game_over = True
    #lst_text[0][0].content.value="P"
    i=0
    for word,point in synonyms:
      j=0
      for c in word:
        lst_text[i][j].content.value=c
        j+=1
      i+=1
      
    def close_dlg(e):
        dlg_modal.open = False
        page.update()
      
    
    col = ft.Column(controls= 
                    [ ft.Text("Score : " + str(score),size=25),
                      ft.Text("Created by:\nTemjenlemla\nLoino\nSir Vihutuo(Teacher)")],height=250)
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("GAME OVER"),
        content= col,
        actions=[
            ft.TextButton("OK",on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )
    page.dialog = dlg_modal
    dlg_modal.open = True
    page.update()
  
  def check_user_word(e):
    nonlocal score
    user_word = fld_user_word.value
    user_word = user_word.upper()
    nonlocal first_word
    if first_word== "":
      first_word = user_word
      anly.SaveKeyValue("first word",0,first_word)  
      
    found = False
    count = 0
    for word,point in synonyms:
      if word==user_word:
        found = True
        break
      count+=1
    if found:
     score+= point 
     txt_score.value = score
     txt_score.update() 
     fld_user_word.value = ""  
 
      
     i=0
     for c in user_word:
       lst_text[count][i].content.value = c
       lst_text[count][i].bgcolor="#ffe6ff"
       lst_text[count][i].update()
       
       i+=1
       
    fld_user_word.focus()
    fld_user_word.update()
    #print(user_word)
  def update_time():
    nonlocal time_remaining
    nonlocal is_game_over
    while not is_game_over:
          #print(time_remaining)
          if time_remaining >= 0  :
              txt_timer.value=time_remaining
              txt_timer.update()
              time.sleep(1)  
              time_remaining-=1           
             # print(time_remaining)
          else:
            is_game_over = True
            GameOver()
            
    print("End thread")    
  def CreateAppBar():
      app_bar = ft.AppBar(
        leading=ft.Icon(ft.icons.FAVORITE_OUTLINE,color="#e45678"),
        leading_width=40,
        title=ft.Text("SYNONYMS"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(ft.icons.RESTART_ALT,on_click=restart_clicked),
            #ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
            
        ],
      )
      return app_bar

  ###########Game variables#################
  time_remaining = 90
  score = 0
  lst_text = []
  is_game_over = False
  chosen_word = ""
  synonyms = []
  first_word = "" #for analytics
  load_dotenv()
  analytics = mymodules.analytics.Analytics(2,
                                            os.getenv('salt'),
                                            os.getenv('pepper'),
                                            os.getenv('analytics_domain'),
                                            os.getenv('this_domain')
                                            )
  player_name = analytics.generate_random_name()
  #######################################
 
  appbar = CreateAppBar()
  txt_chosen_word = ft.Text("",size=20)
  fld_user_word = ft.TextField(label="Enter a synonym",on_submit =check_user_word)
  sc= ft.Text("Score :",size=20, color=ft.colors.SECONDARY)
  txt_score = ft.Text(score,size=20,width=80,color=ft.colors.SECONDARY)
  tm = ft.Text("Time:", size=20)
  line_1 = ft.Divider(height=1, color=ft.colors.SECONDARY_CONTAINER)

  txt_timer = ft.Text(time_remaining,size=20,color=ft.colors.SECONDARY)
  icon_timer = ft.Icon(name=ft.icons.SCHEDULE,color=ft.colors.SECONDARY)
  row_score = ft.Row(controls= [sc,txt_score,line_1,icon_timer,txt_timer])
  txt_syn = ft.Text("Synonyms : ")
  col_left = ft.Column(controls=[txt_chosen_word,fld_user_word])
  col_right = ft.Column()
  
  row_1 = ft.Column(controls=[col_left],scroll=ft.ScrollMode.AUTO,
                )
  page.views.append(ft.View(
                            "/",
                            [
                             appbar,
                             row_score, 
                             line_1,
                             row_1,
                              
                             txt_syn,
                             col_right
                            ],
                            
    
                           )
                  )
  page.update()
  analytics.StartSession(page.client_ip, page.client_user_agent, player_name, page.platform, page.session_id)
  print(page)
  NewGame()
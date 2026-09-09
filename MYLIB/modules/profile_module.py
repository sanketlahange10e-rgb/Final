import customtkinter as ctk
from MYLIB.modules.AccDetails_module import update_account_details
import MYLIB.modules.main_module
import MYLIB.modules.head_module
import MYLIB.modules.menu_module
import MYLIB.modules.save_profile_module
from MYLIB.modules.save_profile_module import profile_save
def show_profile(root,main_frame,head_frame,bottom_frame,details,role,relogin,themecolor):
    print(role)
    if role == "Student":
            
        print("DEBUG: details =", details)  # Debug print
        user = details.get('data', {})
        head_frame.pack_forget()
        main_frame.pack_forget()
        bottom_frame.pack_forget()
        
        
        
        def profile_close():
            profile_window_frame.destroy()
            Profile_page_Frame.destroy()
            head_frame.pack(side=ctk.TOP,fill=ctk.X)
            main_frame.pack(fill=ctk.BOTH,expand=True)
            bottom_frame.pack(side=ctk.BOTTOM,fill=ctk.X)
        
            
            
        profile_window_frame=ctk.CTkFrame(root,fg_color=themecolor,border_color="black",border_width=1)
        profile_close_button=ctk.CTkButton(profile_window_frame,text="⇐",fg_color=themecolor,hover_color="#333333",text_color="white",border_width=0.4,font=("Times New Roman",28),command=profile_close)
        profile_close_button.pack(side=ctk.LEFT,pady=5)  
        profile_window_frame.pack(side=ctk.TOP,fill=ctk.X)
        profile_window_frame.pack_propagate(False)
        profile_window_frame.configure(height=50)


        title_label=ctk.CTkLabel(profile_window_frame,text="Profile",fg_color=themecolor,text_color="white",font=("Times New Roman",32))
        title_label.place(relx=0.5, rely=0.5, anchor="center")
        Profile_page_Frame=ctk.CTkFrame(root,fg_color=themecolor,width=350,height=400,corner_radius=10,border_width=2,border_color="black")
        

        # Try both possible keys for PRN number
        prn_value = user.get('prn_no') or user.get('prnno') or details.get('prn_no') or details.get('prnno', '')
        prn_entry_width = max(len(str(prn_value)), 1) * 15  # 15 pixels per character (approx)
        Label0=ctk.CTkLabel(Profile_page_Frame,text="PRNno:",font=("Arial",20),fg_color=themecolor,text_color="white")
        Label0.place(relx=0.1,rely=0.2)
        text_PRNno=ctk.CTkEntry(Profile_page_Frame,font=("Arial",20),fg_color="#2a2a2a",text_color="white",placeholder_text=prn_value, width=prn_entry_width)
        text_PRNno.insert(0,prn_value)
        text_PRNno.configure(state='readonly')
        text_PRNno.place(relx=0.1,rely=0.3)

        Label1=ctk.CTkLabel(Profile_page_Frame,text="Username:",font=("Arial",20),fg_color=themecolor,text_color="white")
        Label1.place(relx=0.1,rely=0.4)
        username_value = user.get('username', '')
        username_entry_width = max(len(str(username_value)), 1) * 15
        text_Username=ctk.CTkEntry(Profile_page_Frame,font=("Arial",20),fg_color="#2a2a2a",text_color="white",placeholder_text=username_value, width=username_entry_width)
        text_Username.insert(0,username_value)
        text_Username.configure(state='readonly')
        text_Username.place(relx=0.1,rely=0.5)

        Label2=ctk.CTkLabel(Profile_page_Frame,text="Password:",font=("Arial",20),fg_color=themecolor,text_color="white")
        Label2.place(relx=0.1,rely=0.6)
        password_value = user.get('password', '')
        password_entry_width = 7 * 15  # Always 7 asterisks
        text_Password=ctk.CTkEntry(Profile_page_Frame,font=("Arial",20),fg_color="#2a2a2a",text_color="white",placeholder_text='*******', show='*', width=password_entry_width)
        text_Password.insert(0, '*******')
        text_Password.configure(state='readonly')
        text_Password.place(relx=0.1,rely=0.7)
        Edit_button=ctk.CTkButton(Profile_page_Frame,text="Edit Profile",fg_color="#5216c2",font=("Arial",20),width=150,height=50,command=lambda: profile_save(root,Profile_page_Frame,details,update_account_details,relogin,profile_close_button))
        Edit_button.place(relx=0.5,rely=0.85,anchor="center")
        Profile_page_Frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand=True)


    elif role == "Admin" :
        print("DEBUG: details =", details)  # Debug print
        user = details.get('data', {})
        head_frame.pack_forget()
        main_frame.pack_forget()
        bottom_frame.pack_forget()
        
        
        
        def profile_close():
            profile_window_frame.destroy()
            Profile_page_Frame.destroy()
            head_frame.pack(side=ctk.TOP,fill=ctk.X)
            main_frame.pack(fill=ctk.BOTH,expand=True)
            bottom_frame.pack(side=ctk.BOTTOM,fill=ctk.X)
        
            
            
        profile_window_frame=ctk.CTkFrame(root,fg_color=themecolor,border_color="black",border_width=1)
        profile_close_button=ctk.CTkButton(profile_window_frame,text="⇐",fg_color=themecolor,hover_color="#333333",text_color="white",border_width=0.4,font=("Times New Roman",28),command=profile_close)
        profile_close_button.pack(side=ctk.LEFT,pady=5)  
        profile_window_frame.pack(side=ctk.TOP,fill=ctk.X)
        profile_window_frame.pack_propagate(False)
        profile_window_frame.configure(height=50)


        title_label=ctk.CTkLabel(profile_window_frame,text="Profile",fg_color=themecolor,text_color="white",font=("Times New Roman",32))
        title_label.place(relx=0.5, rely=0.5, anchor="center")
        Profile_page_Frame=ctk.CTkFrame(root,fg_color=themecolor,width=350,height=400,corner_radius=10,border_width=2,border_color="black")
        
       
        Label1=ctk.CTkLabel(Profile_page_Frame,text="Username:",font=("Arial",20),fg_color=themecolor,text_color="white")
        Label1.place(relx=0.1,rely=0.4)
        username_value = user.get('username', '')
        username_entry_width = max(len(str(username_value)), 1) * 15
        text_Username=ctk.CTkEntry(Profile_page_Frame,font=("Arial",20),fg_color="#2a2a2a",text_color="white",placeholder_text=username_value, width=username_entry_width)
        text_Username.insert(0,username_value)
        text_Username.configure(state='readonly')
        text_Username.place(relx=0.1,rely=0.5)

        Label2=ctk.CTkLabel(Profile_page_Frame,text="Password:",font=("Arial",20),fg_color=themecolor,text_color="white")
        Label2.place(relx=0.1,rely=0.6)
        password_value = user.get('password', '')
        password_entry_width = max(len(str(password_value)), 1) * 15
        text_Password=ctk.CTkEntry(Profile_page_Frame,font=("Arial",20),fg_color="#2a2a2a",text_color="white",placeholder_text=password_value, show='*', width=password_entry_width)
        text_Password.insert(0,password_value)
        text_Password.configure(state='readonly')
        text_Password.place(relx=0.1,rely=0.7)
        Edit_button=ctk.CTkButton(Profile_page_Frame,text="Edit Profile",fg_color="#5216c2",font=("Arial",20),width=150,height=50,command=lambda: profile_save(root,Profile_page_Frame,details,update_account_details,relogin,profile_close_button))
        Edit_button.place(relx=0.5,rely=0.85,anchor="center")
        Profile_page_Frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand=True)

    elif role == "Driver":
        print("DEBUG: details =", details)  # Debug print
        user = details.get('data', {})
        head_frame.pack_forget()
        main_frame.pack_forget()
        bottom_frame.pack_forget()
        
        
        
        def profile_close():
            profile_window_frame.destroy()
            Profile_page_Frame.destroy()
            head_frame.pack(side=ctk.TOP,fill=ctk.X)
            main_frame.pack(fill=ctk.BOTH,expand=True)
            bottom_frame.pack(side=ctk.BOTTOM,fill=ctk.X)
        
            
            
        profile_window_frame=ctk.CTkFrame(root,fg_color=themecolor,border_color="black",border_width=1)
        profile_close_button=ctk.CTkButton(profile_window_frame,text="⇐",fg_color=themecolor,hover_color="#333333",text_color="white",border_width=0.4,font=("Times New Roman",28),command=profile_close)
        profile_close_button.pack(side=ctk.LEFT,pady=5)  
        profile_window_frame.pack(side=ctk.TOP,fill=ctk.X)
        profile_window_frame.pack_propagate(False)
        profile_window_frame.configure(height=50)


        title_label=ctk.CTkLabel(profile_window_frame,text="Profile",fg_color=themecolor,text_color="white",font=("Times New Roman",32))
        title_label.place(relx=0.5, rely=0.5, anchor="center")
        Profile_page_Frame=ctk.CTkFrame(root,fg_color=themecolor,width=350,height=400,corner_radius=10,border_width=2,border_color="black")
        
        Label0=ctk.CTkLabel(Profile_page_Frame,text="PRNno:",font=("Arial",20),fg_color=themecolor,text_color="white")
        Label0.place(relx=0.1,rely=0.2)
        text_PRNno=ctk.CTkEntry(Profile_page_Frame,font=("Arial",20),fg_color="#2a2a2a",text_color="white",placeholder_text=details.get('prnno', ''))
        text_PRNno.insert(0,details.get('prnno', ''))
        text_PRNno.configure(state='readonly')
        text_PRNno.place(relx=0.1,rely=0.3) 


        Label0=ctk.CTkLabel(Profile_page_Frame,text="DriverID:",font=("Arial",20),fg_color=themecolor,text_color="white")
        Label0.place(relx=0.1,rely=0.2)
        driver_no_value = user.get('driver_no', '')
        driver_no_entry_width = max(len(str(driver_no_value)), 1) * 15
        text_DriverNo=ctk.CTkEntry(Profile_page_Frame,font=("Arial",20),fg_color="#2a2a2a",text_color="white",placeholder_text=driver_no_value, width=driver_no_entry_width)
        text_DriverNo.insert(0,driver_no_value)
        text_DriverNo.configure(state='readonly')
        text_DriverNo.place(relx=0.1,rely=0.3)

        Label1=ctk.CTkLabel(Profile_page_Frame,text="Username:",font=("Arial",20),fg_color=themecolor,text_color="white")
        Label1.place(relx=0.1,rely=0.4)
        text_Username=ctk.CTkEntry(Profile_page_Frame,font=("Arial",20),fg_color="#2a2a2a",text_color="white",placeholder_text=user.get('username', ''))
        text_Username.insert(0,user.get('username', ''))
        text_Username.configure(state='readonly')
        text_Username.place(relx=0.1,rely=0.5)

        Label2=ctk.CTkLabel(Profile_page_Frame,text="Password:",font=("Arial",20),fg_color=themecolor,text_color="white")
        Label2.place(relx=0.1,rely=0.6)
        text_Password=ctk.CTkEntry(Profile_page_Frame,font=("Arial",20),fg_color="#2a2a2a",text_color="white",placeholder_text=user.get('password', ''), show='*')
        text_Password.insert(0,user.get('password', ''))
        text_Password.configure(state='readonly')
        text_Password.place(relx=0.1,rely=0.7)
        Edit_button=ctk.CTkButton(Profile_page_Frame,text="Edit Profile",fg_color="#5216c2",font=("Arial",20),width=150,height=50,command=lambda: profile_save(root,Profile_page_Frame,details,update_account_details,relogin,profile_close_button))
        Edit_button.place(relx=0.5,rely=0.85,anchor="center")
        Profile_page_Frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand=True)

from pathlib import Path
import customtkinter as ctk
import tkinter.messagebox as messagebox
def profile_save(root,Profile_page_Frame,details,update_account_details,relogin,profile_close_button):
    Profile_page_Frame.pack_forget()
    profile_close_button.configure(state='disabled')
    save_profile_frame=ctk.CTkFrame(root,width=600,height=400,corner_radius=10)
    def close_save():
        Profile_page_Frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand=True,pady=20)
        save_profile_frame.pack_forget()
        profile_close_button.configure(state='normal')
       
    
    def profile_close():
        if profile_close_button.cget("state") == "disabled":
            save_profile_frame.after(100,lambda: save_profile_frame.configure(fg_color="#ffffff"))
            save_profile_frame.after(200,lambda: save_profile_frame.configure(fg_color="#1e1e1e"))
            save_profile_frame.after(300,lambda: save_profile_frame.configure(fg_color="#ffffff"))
            save_profile_frame.after(400,lambda: save_profile_frame.configure(fg_color="#1e1e1e"))
    
    
    def save_changes():
            update_account_details(details.get('PrnNo', ''),text_Username.get(),text_Password.get(),text_Newpassword.get())
            messagebox.showinfo(title="Success",message="Profile updated successfully!")
            root.after(100,relogin())
            close_save()
    profile_close_button.bind("<Button-1>", lambda e: profile_close())
    Label1=ctk.CTkLabel(save_profile_frame,text="Username:",font=("Arial",20),fg_color="#1e1e1e",text_color="white")
    Label1.place(relx=0.1,rely=0.2)
    text_Username=ctk.CTkEntry(save_profile_frame,font=("Arial",20),fg_color="#2a2a2a",text_color="white",placeholder_text=details.get('username', ''))
    text_Username.insert(0,details.get('username', ''))
    text_Username.place(relx=0.1,rely=0.3)

    Label2=ctk.CTkLabel(save_profile_frame,text=" old Password:",font=("Arial",20),fg_color="#1e1e1e",text_color="white")    
    Label2.place(relx=0.1,rely=0.4)
    text_Password=ctk.CTkEntry(save_profile_frame,font=("Arial",20),fg_color="#2a2a2a",text_color="white",placeholder_text="enter old password")
    text_Password.place(relx=0.1,rely=0.5)

    Label3=ctk.CTkLabel(save_profile_frame,text="New Password:",font=("Arial",20),fg_color="#1e1e1e",text_color="white")    
    Label3.place(relx=0.1,rely=0.6)
    text_Newpassword=ctk.CTkEntry(save_profile_frame,font=("Arial",20),fg_color="#2a2a2a",text_color="white",placeholder_text="enter new password")
    text_Newpassword.place(relx=0.1,rely=0.7)

    cancle_button=ctk.CTkButton(save_profile_frame,text="Cancel",fg_color="#333333",font=("Arial",20),width=150,height=50,command=close_save)
    cancle_button.place(relx=0.3,rely=0.9,anchor="center")
    Save_button=ctk.CTkButton(save_profile_frame,text="Save Changes",fg_color="#5216c2",font=("Arial",20),width=150,height=50,command=save_changes)
    Save_button.place(relx=0.7,rely=0.9,anchor="center")
    
    save_profile_frame.pack_propagate(False)
    save_profile_frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand=True)
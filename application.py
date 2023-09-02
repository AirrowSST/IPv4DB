from tkinter import IntVar
import customtkinter as ctk
from model import Database, IPAddress, IPAddressBlock, Organization

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class LeftSideBarFrame(ctk.CTkFrame):  # Actions to modify database
    def __init__(self, master, **kwargs):
        super().__init__(master, width=140, corner_radius=0, **kwargs)
        self.app: App = master
        
        self.logo_label = ctk.CTkLabel(self, text="ctk", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = ctk.CTkButton(self, command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = ctk.CTkButton(self, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = ctk.CTkButton(self, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        
        self.grid_rowconfigure(4, weight=1)
        
        self.appearance_mode_label = ctk.CTkLabel(self, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = ctk.CTkLabel(self, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

    def sidebar_button_event(self):
        print("sidebar_button click")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

class RightSideBarFrame(ctk.CTkFrame):  # Shows information on selected item
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=0, **kwargs)
        self.app: App = master

        # create textbox
        self.textbox = ctk.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 1)
        
class BottomFrame(ctk.CTkFrame):  # Allows Searching
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=0, **kwargs)
        self.app: App = master
        
        self.entry = ctk.CTkEntry(self, 
                                  placeholder_text="Search IP Address, Network or Orgnization")
        self.grid_columnconfigure(0, weight=1)
        self.entry.grid(row=0, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = ctk.CTkButton(master=self, 
                                           fg_color="transparent", 
                                           border_width=2, 
                                           text_color=("gray10", "#DCE4EE"),
                                           command=self.search_input)
        self.main_button_1.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def search_input(self):  # handles search input action
        print(self.app.database.search_all(self.entry.get()))

class NetworkFrame(ctk.CTkFrame):  # Acts as a card displaying information on a network
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

class CenterFrame(ctk.CTkScrollableFrame):  # Shows database
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", corner_radius=0, **kwargs)
        self.app: App = master

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.database = Database()
        
        # --------------------------- SAMPLE DATA ---------------------------
        ip1 = IPAddress("155.153.45.23/24")
        ip1Block = IPAddressBlock(ip1)
        ip2 = IPAddress("00001111010101011110000110100101/24")
        ip2Block = IPAddressBlock(ip2)
        ip3 = IPAddress("96.85.162.16/22")
        ip3Block = IPAddressBlock(ip3)
        ip4 = IPAddress("18.1.0.0/20")
        ip4Block = IPAddressBlock(ip4)

        o1 = Organization("Google", (ip1Block, ip2Block))
        o2 = Organization("Amazon", ip3Block)
        o3 = Organization("SpaceX", (ip4Block,))
        
        self.database.add_organization(o1)
        self.database.add_organization(o2)
        self.database.add_organization(o3)
        # --------------------------- SAMPLE DATA ---------------------------
        

        # configure window
        self.title("IPv4DB")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # left sidebar frame
        self.left_sidebar_frame = LeftSideBarFrame(self)
        self.left_sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

        # right sidebar frame
        self.left_sidebar_frame = RightSideBarFrame(self)
        self.left_sidebar_frame.grid(row=0, column=2, rowspan=2, sticky="nsew")
        
        # center frame
        self.center_frame = CenterFrame(self)
        self.center_frame.grid(row=0, column=1, sticky="nsew")

        # bottom frame
        self.bottom_frame = BottomFrame(self)
        self.bottom_frame.grid(row=1, column=1, sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.mainloop()
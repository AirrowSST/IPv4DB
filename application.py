from tkinter import IntVar
import customtkinter as ctk
from model import Database, IPAddress, IPAddressBlock, Organization

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class LeftSideBarFrame(ctk.CTkFrame):  # Actions to modify database
    def __init__(self, master, **kwargs):
        super().__init__(master, width=140, corner_radius=0, **kwargs)
        self.app: App = master
        
        # App Name
        self.logo_label = ctk.CTkLabel(self, text="IPv4DB", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Database Actions
        self.add_organization_button = ctk.CTkButton(self, 
                                              text="Add Organization",
                                              command=self.add_organiazation_input)
        self.add_organization_button.grid(row=1, column=0, padx=20, pady=10)
        self.remove_organization_button = ctk.CTkButton(self, 
                                                        text="Remove Organization",
                                                        command=self.remove_organiazation_input)
        self.remove_organization_button.grid(row=2, column=0, padx=20, pady=10)
        
        # Gap
        gap_row = 3
        self.grid_rowconfigure(gap_row, weight=1)
        
        # Appearance Mode/Theme
        self.appearance_mode_label = ctk.CTkLabel(self, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=gap_row + 1, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=gap_row + 2, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_optionemenu.set("System")
        
        # Scaling (UI)
        self.scaling_label = ctk.CTkLabel(self, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=gap_row + 3, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self, values=["60%", "80%", "100%", "120%", "140%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=gap_row + 4, column=0, padx=20, pady=(10, 20))
        self.scaling_optionemenu.set("100%")

    def add_organiazation_input(self):
        dialog = ctk.CTkInputDialog(text="Organization Name: ", title="Adding Organization")
        self.app.database.add_organization(Organization(dialog.get_input()))
        self.app.reset_search_results()
        
    def remove_organiazation_input(self):
        dialog = ctk.CTkInputDialog(text="Organization Name: ", title="Removing Organization")
        self.app.database.remove_organization(self.app.database.get_organization_by_name(dialog.get_input()))
        self.app.reset_search_results()

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
        self.textbox = ctk.CTkTextbox(self, 
                                      width=250)
        self.update_textbox()
        self.textbox.configure(state="disabled")
        self.grid_rowconfigure(0, weight=1)
        self.textbox.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
    
    def update_textbox(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        if self.app.info_display is None:
            self.textbox.insert("0.0", "No item selected")
        else:
            if isinstance(self.app.info_display, IPAddress):
                ip_address = self.app.info_display
                ip_address_block = IPAddressBlock(ip_address.get_network_address())
                print(ip_address_block.ip_address)
                display_str = (f"IP Address\n\n{ip_address}\n"
                               + ("\n\nThis is not a network address, no information about a network can be inferred\n" 
                                  if ip_address.subnet_mask_length == 0 else ""
                                  + f"\n\nNetwork Address: {ip_address.get_network_address()} \n\nHost Address: {ip_address.get_host_address()}"
                                  + f"\n\nSubnet Mask: {ip_address.get_subnet_mask()}"
                                  + f"\n\nTotal Addresses in Network: {ip_address_block.get_num_usable_addresses()}"
                                  + f"\n\nUsable Host Addresses in Network: {ip_address_block.get_num_usable_addresses() - 2}"
                                  + f"\n\nUsable Host Address Range: \n{ip_address_block.get_lower_bound_address()} - {ip_address_block.get_upper_bound_address()}"
                                  + f"\n\nBroadcast Address: {ip_address_block.get_broadcast_address()}"
                               ))
                self.textbox.insert("0.0", display_str)
            elif isinstance(self.app.info_display, IPAddressBlock):
                self.textbox.insert("0.0", "IP Address Block\n\n"
                                    + str(self.app.info_display))
            elif isinstance(self.app.info_display, Organization):
                self.textbox.insert("0.0", "Organization\n\n"
                                    + str(self.app.info_display))
        self.textbox.configure(state="disabled")
        
class BottomFrame(ctk.CTkFrame):  # Allows Searching
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=0, **kwargs)
        self.app: App = master
        
        # Search bar
        self.search_entry = ctk.CTkEntry(self, 
                                  placeholder_text="Search IP Address, Network or Orgnization")
        self.grid_columnconfigure(0, weight=1)
        self.search_entry.grid(row=0, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # Search button
        self.search_button = ctk.CTkButton(master=self,
                                           text_color=("gray10", "#DCE4EE"),
                                           command=self.search_input,
                                           text="Search")
        self.search_button.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def search_input(self):  # handles search input action
        ip_address, owner, owner_block, organizations = self.app.database.search_all(self.search_entry.get())
        if ip_address is not None:
            self.app.set_info_display(ip_address)
        elif owner is not None:
            self.app.set_info_display(owner)
        self.app.set_search_results(organizations)

class NetworkCardFrame(ctk.CTkFrame):  # Acts as a card displaying information on a network
    def __init__(self, master, app, network, **kwargs):
        super().__init__(master, **kwargs)
        self.app: App = app
        self.master = master
        self.network = network
        
        # Network Address
        self.label = ctk.CTkLabel(self, 
                                  text=network.get_identity_address())
        self.grid_columnconfigure(0, weight=1)
        self.label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsw")
        
        # Select Button
        self.select_button = ctk.CTkButton(master=self,
                                           text_color=("gray10", "#DCE4EE"),
                                           command=self.select_input,
                                           text="Select")
        self.select_button.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nse")
    
    def select_input(self):
        self.app.set_info_display(self.network)

class OrganizationCardFrame(ctk.CTkFrame):  # Acts as a card displaying information on an organization
    def __init__(self, master, app, organization: Organization, **kwargs):
        super().__init__(master, **kwargs)
        self.app: App = app
        self.master = master
        self.organization: Organization = organization
        self.grid_columnconfigure(0, weight=1)
        
        # Organization Name
        self.label = ctk.CTkLabel(self,
                                  text=organization.name)
        self.label.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsw")
        
        # Network Cards
        self.network_card_frames: list[NetworkCardFrame] = []
        self.row_start = 1
        self.update_network_frames()
        
        # Select Button
        self.select_button = ctk.CTkButton(master=self,
                                           text_color=("gray10", "#DCE4EE"),
                                           command=self.select_input,
                                           text="Select")
        self.select_button.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nse")
    
    def select_input(self):
        self.app.set_info_display(self.organization)

    def update_network_frames(self):
        for frame in self.network_card_frames:
            frame.grid_forget()
            frame.destroy()
        self.network_card_frames.clear()
        
        for ip_address_block in self.organization.ip_address_blocks:
            frame = NetworkCardFrame(self, self.app, ip_address_block)
            self.network_card_frames.append(frame)
        
        for index, frame in enumerate(self.network_card_frames):
            frame.grid(row=self.row_start + index, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="nsew")

class CenterFrame(ctk.CTkScrollableFrame):  # Shows database
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", corner_radius=0, **kwargs)
        self.app: App = master
        self.organization_card_frames = []
        self.grid_columnconfigure(0, weight=1)
        self.update_all()

    def update_all(self, organizations=None):
        for frame in self.organization_card_frames:
            frame.grid_forget()
            frame.destroy()
        self.organization_card_frames.clear()
        
        organizations = self.app.database.organizations if organizations is None else organizations 
        for organization in organizations:
            frame = OrganizationCardFrame(self, self.app, organization)
            self.organization_card_frames.append(frame)
        
        for index, frame in enumerate(self.organization_card_frames):
            frame.grid(row=index, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.database = Database()
        self.info_display = None  # value holding the object whose info is to be shown
        
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
        o4 = Organization("Bala's Chicken Store")
        o5 = Organization("SpaceY")
        
        
        self.database.add_organization(o1)
        self.database.add_organization(o2)
        self.database.add_organization(o3)
        self.database.add_organization(o4)
        self.database.add_organization(o5)
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
        self.right_sidebar_frame = RightSideBarFrame(self)
        self.right_sidebar_frame.grid(row=0, column=2, rowspan=2, sticky="nsew")
        
        # center frame
        self.center_frame = CenterFrame(self)
        self.center_frame.grid(row=0, column=1, sticky="nsew")

        # bottom frame
        self.bottom_frame = BottomFrame(self)
        self.bottom_frame.grid(row=1, column=1, sticky="nsew")
        self.bind("<KeyPress>", lambda event: self.bottom_frame.search_input() if event.char == "\r" else None)

    def set_info_display(self, item):
        self.info_display = item
        self.right_sidebar_frame.update_textbox()
    
    def remove_info_display(self):
        self.info_display = None
        self.right_sidebar_frame.update_textbox()
    
    def set_search_results(self, organizations):
        self.center_frame.update_all(organizations)
        
    def reset_search_results(self):
        self.center_frame.update_all()

if __name__ == "__main__":
    app = App()
    app.mainloop()
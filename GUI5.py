import tkinter
import tkinter.messagebox
import customtkinter
import subprocess
import os
import pandas as pd
import plotly_express as px
import json
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import csv
import threading
from PIL import Image
import webbrowser
import tempfile

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mosqutio Sim v1.0")
        self.geometry(f"{1000}x{700}")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3, 4), weight=0)
        self.grid_rowconfigure((1, 2), weight=1)

        image_path = os.path.join(os.getcwd(), "assets", "Squito.png")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path)), size =(20,20))


        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=90, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Mosqutio Sim v1.0",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Please type your output folder name")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,
                                                     text="Start Simulation", text_color=("gray10", "#DCE4EE"),
                                                     command=self.run_r_script)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.textbox = customtkinter.CTkTextbox(self, width=300)
        self.textbox.grid(row=0, column=2, padx=(20, 20), rowspan=2, pady=(20, 20), sticky="nsew")

        self.tabview = customtkinter.CTkTabview(self, width=200)
        self.tabview.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Release Values")
        self.tabview.tab("Release Values").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs

        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("Release Values"), text="Release Start",
                                                           command=lambda: self.open_input_dialog_event(
                                                               "Release Start"))
        self.string_input_button.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button2 = customtkinter.CTkButton(self.tabview.tab("Release Values"), text="Release Number",
                                                            command=lambda: self.open_input_dialog_event(
                                                                "Release Number"))
        self.string_input_button2.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.string_input_button3 = customtkinter.CTkButton(self.tabview.tab("Release Values"), text="Release Interval",
                                                            command=lambda: self.open_input_dialog_event(
                                                                "Release Interval"))
        self.string_input_button3.grid(row=3, column=0, padx=20, pady=(10, 10))
        self.string_input_button4 = customtkinter.CTkButton(self.tabview.tab("Release Values"),
                                                            text="Release Proportion",
                                                            command=lambda: self.open_input_dialog_event(
                                                                "Release Proportion"))
        self.string_input_button4.grid(row=4, column=0, padx=20, pady=(10, 10))
        ##########################################

        self.tabview = customtkinter.CTkTabview(self, width=200)
        self.tabview.grid(row=1, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.tabview.add("Simulation Settings")
        self.tabview.tab("Simulation Settings").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs

        self.string_input_button5 = customtkinter.CTkButton(self.tabview.tab("Simulation Settings"), text="nRep",
                                                            command=lambda: self.open_input_dialog_event("nRep"))
        self.string_input_button5.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button6 = customtkinter.CTkButton(self.tabview.tab("Simulation Settings"), text="Max Time",
                                                            command=lambda: self.open_input_dialog_event("Max Time"))
        self.string_input_button6.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.string_input_button7 = customtkinter.CTkButton(self.tabview.tab("Simulation Settings"),
                                                            text="Adult Pop Equilibrium",
                                                            command=lambda: self.open_input_dialog_event(
                                                                "Adult Pop Equilibrium"))
        self.string_input_button7.grid(row=3, column=0, padx=20, pady=(10, 10))
        self.string_input_button8 = customtkinter.CTkButton(self.tabview.tab("Simulation Settings"), text="Mating Comp",
                                                            command=lambda: self.open_input_dialog_event("Mating Comp"))
        self.string_input_button8.grid(row=5, column=0, padx=20, pady=(10, 10))

        self.string_input_button17 = customtkinter.CTkButton(self.tabview.tab("Simulation Settings"),
                                                             text="Lifespan Reduction",
                                                             command=lambda: self.open_input_dialog_event(
                                                                 "Lifespan Reduction"))
        self.string_input_button17.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.tabview = customtkinter.CTkTabview(self, width=150)
        self.tabview.grid(row=1, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.tabview.add("BioParameters")
        self.tabview.tab("BioParameters").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.string_input_button9 = customtkinter.CTkButton(self.tabview.tab("BioParameters"), text="Days Egg",
                                                            command=lambda: self.open_input_dialog_event("Days Egg"))
        self.string_input_button9.grid(row=1, column=0, padx=20, pady=(8, 8))
        self.string_input_button10 = customtkinter.CTkButton(self.tabview.tab("BioParameters"),
                                                             text="Days Larvae",
                                                             command=lambda: self.open_input_dialog_event(
                                                                 "Days Larvae"))
        self.string_input_button10.grid(row=2, column=0, padx=20, pady=(8, 8))
        self.string_input_button11 = customtkinter.CTkButton(self.tabview.tab("BioParameters"), text="Days Pupae",
                                                             command=lambda: self.open_input_dialog_event("Days Pupae"))
        self.string_input_button11.grid(row=3, column=0, padx=20, pady=(8, 8))
        self.string_input_button12 = customtkinter.CTkButton(self.tabview.tab("BioParameters"),
                                                             text="Eggs Per Mother",
                                                             command=lambda: self.open_input_dialog_event(
                                                                 "Eggs Per Mother"))
        self.string_input_button12.grid(row=4, column=0, padx=20, pady=(8, 8))
        self.string_input_button13 = customtkinter.CTkButton(self.tabview.tab("BioParameters"),
                                                             text="Pop Growth Rate",
                                                             command=lambda: self.open_input_dialog_event(
                                                                 "Pop Growth Rate"))
        self.string_input_button13.grid(row=5, column=0, padx=20, pady=(8, 8))
        self.string_input_button18 = customtkinter.CTkButton(self.tabview.tab("BioParameters"),
                                                             text="Rate of death",
                                                             command=lambda: self.open_input_dialog_event(
                                                                 "Rate of death"))
        self.string_input_button18.grid(row=6, column=0, padx=20, pady=(8, 8))

        ####################################
        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, width =1000, label_text="Settings")
        self.scrollable_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []

        switch1 = customtkinter.CTkSwitch(master=self.scrollable_frame, text="Batch Migration")
        switch1.grid(row=1, column=0, padx=10, pady=(0, 20))
        switch2 = customtkinter.CTkSwitch(master=self.scrollable_frame, text="MultiCore Processing")
        switch2.grid(row=2, column=0, padx=10, pady=(0, 20))
        switch3 = customtkinter.CTkSwitch(master=self.scrollable_frame, text="Default Bioparameters")
        switch3.grid(row=3, column=0, padx=10, pady=(0, 20))
        switch4 = customtkinter.CTkSwitch(master=self.scrollable_frame, text="Default Sim Parameters")
        switch4.grid(row=4, column=0, padx=10, pady=(0, 20))

        self.scrollable_frame_switches.append(switch1)
        self.scrollable_frame_switches.append(switch2)
        self.scrollable_frame_switches.append(switch3)
        self.scrollable_frame_switches.append(switch4)

        # set default values
        self.scrollable_frame_switches[0].select()
        self.scrollable_frame_switches[2].select()

        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.textbox.insert("0.0", "Version 1.0 Mosqutio Simulation \n\n Created by Ryan D'Onofrio - Craig Montell Lab \n\n"
                                   "MgDrivE developed by John Marshall Lab")


    def open_input_dialog_event(self, button_text):
        dialog = customtkinter.CTkInputDialog(text="Type in a value:", title="CTkInputDialog")
        input_value = dialog.get_input()
        try:
            float(input_value)
        except ValueError:
            dialog = customtkinter.CTkInputDialog(text="Invalid input. Please enter a numeric value:",
                                                  title="CTkInputDialog")
            input_value = dialog.get_input()
        variable_names = {
            "Days Egg": "days_egg",
            "Days Larvae": "days_larvae",
            "Days Pupae": "days_pupae",
            "Eggs Per Mother": "eggs_per_mother",
            "Pop Growth Rate": "pop_growth_rate",
            "Rate of death": "rate_of_death_per_day",
            "nRep": "nRep",
            "Max Time": "tMax",
            "Adult Pop Equilibrium": "ad_pop_eq",
            "Mating Comp": "mate_comp",
            "Lifespan Reduction": "lifespan_red",
            "Release Start": "rel_srt",
            "Release Number": "rel_num",
            "Release Interval": "rel_int",
            "Release Proportion": "rel_val",

        }
        variable_name = variable_names[button_text]
        setattr(self, variable_name, input_value)
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    def sidebar_button_event(self):
        print("sidebar_button click")

    def run_dashboard(self):
        subprocess.run(
            ["python", "Dash3.py"],
            capture_output=True, text=True
        )

    def run_r_script(self):
        days_egg = self.days_egg if hasattr(self, 'days_egg') else 5
        days_larvae = self.days_larvae if hasattr(self, 'days_larvae') else 6
        days_pupae = self.days_pupae if hasattr(self, 'days_pupae') else 4
        eggs_per_mother = self.eggs_per_mother if hasattr(self, 'eggs_per_mother') else 20
        pop_growth_rate = self.pop_growth_rate if hasattr(self, 'pop_growth_rate') else 1.175
        rate_of_death_per_day = self.rate_of_death_per_day if hasattr(self, 'rate_of_death_per_day') else .09
        nRep = self.nRep if hasattr(self, 'nRep') else 1
        tMax = self.tMax if hasattr(self, 'tMax') else 1000
        ad_pop_eq = self.ad_pop_eq if hasattr(self, 'ad_pop_eq') else 2000
        mate_comp = self.mate_comp if hasattr(self, 'mate_comp') else .75
        lifespan_red = self.lifespan_red if hasattr(self, 'lifespan_red') else .75
        batch_mig = self.scrollable_frame_switches[0].get()
        multicore = self.scrollable_frame_switches[1].get()
        default_bioparm = self.scrollable_frame_switches[2].get()
        default_sim = self.scrollable_frame_switches[3].get()

        rel_srt = self.rel_srt if hasattr(self, 'rel_srt') else 50
        rel_num = self.rel_num if hasattr(self, 'rel_num') else 12
        rel_int = self.rel_int if hasattr(self, 'rel_int') else 20
        rel_val = self.rel_val if hasattr(self, 'rel_val') else 55
        File_path = self.entry.get()
        wd = os.getcwd()
        new_path = wd.replace(os.sep, "/")
        new_path = os.path.join(new_path, File_path)
        new_path = new_path.replace(os.sep, "/")
        final_path = os.path.join(new_path, "001")
        final_path = final_path.replace(os.sep, "/")


        result = subprocess.run(
            ["Rscript", "A5.R", str(days_egg), str(days_larvae), str(days_pupae), str(eggs_per_mother),
             str(pop_growth_rate), str(rate_of_death_per_day),
             str(nRep), str(tMax), str(ad_pop_eq), str(mate_comp), str(lifespan_red), str(batch_mig), str(multicore),
             str(default_bioparm),str(default_sim), str(rel_srt), str(rel_num), str(rel_int), str(rel_val), str(File_path),
             str(wd)],
            capture_output=True, text=True)


        with open(os.path.join(os.getcwd(), 'variables2.txt'), 'w') as f:
            f.write(f"nRep={nRep}\n")
            f.write(f"ad_pop_eq={ad_pop_eq}\n")
            f.write(f"rel_num={rel_num}\n")
            f.write(f"rel_val={rel_val}\n")
            f.write(f"File_path={File_path}\n")
            f.write(f"wd={wd}\n")
            f.write(f"new_path={new_path}\n")
            f.write(f"final_path={final_path}\n")
            f.write(f"rel_int={rel_int}\n")
            f.write(f"rel_srt={rel_srt}\n")



        if result.returncode != 0:
            print("The R script has failed with exit code", result.returncode)
        else:
            print(result.stdout)
            #subprocess.run(["python", "Dash3.py"])
            url = 'http://127.0.0.1:8050/'
            #webbrowser.open_new(url)
            thread = threading.Thread(target=self.run_dashboard)
            thread.start()
            print("Access your Dashboard at: ", url)




if __name__ == "__main__":
    app = App()
    app.mainloop()
